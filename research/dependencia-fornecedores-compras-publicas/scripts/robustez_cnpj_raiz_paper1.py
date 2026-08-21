#!/usr/bin/env python3
"""Robustez do Paper 1 à agregação de fornecedores por CNPJ raiz.

Objetivo
--------
Recalcular concentração, exposição externa LOO e stress tests do recorte
jan-jun/2025 tratando estabelecimentos com o mesmo CNPJ raiz (8 primeiros
dígitos) como um único fornecedor econômico observável.

A análise reporta duas comparações:
1. amostra fixa dos 1.347 compradores elegíveis na especificação principal,
   para isolar o efeito da mudança de unidade do fornecedor;
2. elegibilidade recalculada após a agregação por CNPJ raiz.

Esta robustez não identifica grupos econômicos além do CNPJ raiz e, portanto,
não substitui uma consolidação societária com dados de controle corporativo.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results"
OUT = RES / "robustez_cnpj_raiz_2025_06"
SEED = 20260821
DRAWS = 1000


def spearman(a, b):
    z = pd.DataFrame({"a": a, "b": b}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(z) < 3:
        return {"rho": None, "p": None, "n": int(len(z))}
    rho, p = spearmanr(z.a, z.b)
    return {"rho": float(rho), "p": float(p), "n": int(len(z))}


def hhi_norm(hhi, n):
    h = pd.to_numeric(hhi, errors="coerce")
    nn = pd.to_numeric(n, errors="coerce")
    floor = 1.0 / nn
    return ((h - floor) / (1.0 - floor)).where(nn > 1).clip(0, 1)


def cnpj_root(x: pd.Series) -> tuple[pd.Series, pd.Series]:
    s = x.astype("string").str.replace(r"\D", "", regex=True)
    valid = s.str.len().eq(14)
    # IDs fora do padrão são mantidos individualizados, nunca agrupados entre si.
    root = s.where(valid, "INVALID_" + s.fillna("NA"))
    root = root.where(~valid, s.str.slice(0, 8))
    return root, valid


def load_cohort() -> pd.DataFrame:
    frames = []
    for m in range(1, 7):
        p = DATA / f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        if not p.exists():
            raise FileNotFoundError(p)
        d = pd.read_csv(
            p,
            dtype={
                "id_contrato": "string",
                "orgao_cnpj": "string",
                "fornecedor_id_limpo": "string",
                "municipio_ibge": "string",
            },
            low_memory=False,
        )
        d["ano_assinatura"] = pd.to_numeric(d["ano_assinatura"], errors="coerce")
        d["valorInicial"] = pd.to_numeric(d["valorInicial"], errors="coerce")
        frames.append(d)
    acc = pd.concat(frames, ignore_index=True)
    if acc.duplicated("id_contrato").any():
        raise RuntimeError("Duplicidade de id_contrato detectada no acumulado jan-jun.")
    x = acc[acc.ano_assinatura.eq(2025) & acc.valorInicial.gt(0)].copy()
    x["fornecedor_raiz"], x["cnpj_14_valido"] = cnpj_root(x.fornecedor_id_limpo)
    return x


def build_root_metrics(x: pd.DataFrame):
    rel = (
        x.groupby(["orgao_cnpj", "fornecedor_raiz"], dropna=False)
        .agg(
            valor_relacao=("valorInicial", "sum"),
            n_instrumentos=("id_contrato", "nunique"),
        )
        .reset_index()
    )
    rel["share_valor"] = rel.valor_relacao / rel.groupby("orgao_cnpj").valor_relacao.transform("sum")
    rel["share_contagem"] = rel.n_instrumentos / rel.groupby("orgao_cnpj").n_instrumentos.transform("sum")

    rows = []
    for buyer, g in rel.groupby("orgao_cnpj", sort=False):
        sv = g.share_valor.sort_values(ascending=False)
        sc = g.share_contagem.sort_values(ascending=False)
        hv = float((sv ** 2).sum())
        hc = float((sc ** 2).sum())
        n = int(len(g))
        rows.append({
            "orgao_cnpj": str(buyer),
            "valor_total_raiz": float(g.valor_relacao.sum()),
            "n_instrumentos_raiz": int(g.n_instrumentos.sum()),
            "n_fornecedores_raiz": n,
            "portfolio_hhi_raiz": hv,
            "count_hhi_raiz": hc,
            "portfolio_cr1_raiz": float(sv.iloc[0]),
            "portfolio_cr4_raiz": float(sv.iloc[:4].sum()),
            "portfolio_neff_raiz": float(1.0 / hv) if hv > 0 else np.nan,
        })
    buyers = pd.DataFrame(rows)
    buyers["portfolio_hhi_norm_raiz"] = hhi_norm(buyers.portfolio_hhi_raiz, buyers.n_fornecedores_raiz)
    buyers["count_hhi_norm_raiz"] = hhi_norm(buyers.count_hhi_raiz, buyers.n_fornecedores_raiz)

    suppliers = (
        rel.groupby("fornecedor_raiz")
        .agg(degree_raiz=("orgao_cnpj", "nunique"), strength_raiz=("valor_relacao", "sum"))
        .reset_index()
    )
    suppliers["pct_degree_global_raiz"] = suppliers.degree_raiz.rank(pct=True, method="average")
    suppliers["pct_strength_global_raiz"] = suppliers.strength_raiz.rank(pct=True, method="average")

    z = rel.merge(
        suppliers[["fornecedor_raiz", "pct_degree_global_raiz", "pct_strength_global_raiz"]],
        on="fornecedor_raiz",
        how="left",
    )
    z["ed_piece"] = z.share_valor * z.pct_degree_global_raiz
    z["es_piece"] = z.share_valor * z.pct_strength_global_raiz
    exp = (
        z.groupby("orgao_cnpj")
        .agg(
            exposicao_degree_global_raiz=("ed_piece", "sum"),
            exposicao_strength_global_raiz=("es_piece", "sum"),
        )
        .reset_index()
    )
    buyers = buyers.merge(exp, on="orgao_cnpj", how="left")
    return rel, buyers, suppliers


def exact_loo_percentiles(base_values: np.ndarray, portfolio_base: np.ndarray, portfolio_adj: np.ndarray) -> np.ndarray:
    global_sorted = np.sort(base_values)
    pb = np.sort(portfolio_base)
    pa = np.sort(portfolio_adj)
    n = len(global_sorted)
    out = []
    for x in portfolio_adj:
        left = (
            np.searchsorted(global_sorted, x, side="left")
            - np.searchsorted(pb, x, side="left")
            + np.searchsorted(pa, x, side="left")
        )
        right = (
            np.searchsorted(global_sorted, x, side="right")
            - np.searchsorted(pb, x, side="right")
            + np.searchsorted(pa, x, side="right")
        )
        rank_mid = ((left + 1) + right) / 2.0
        out.append(rank_mid / n)
    return np.asarray(out, dtype=float)


def build_loo_root(rel: pd.DataFrame, buyer_ids: pd.Series, suppliers: pd.DataFrame) -> pd.DataFrame:
    ids_keep = set(buyer_ids.astype(str))
    r = rel[rel.orgao_cnpj.astype(str).isin(ids_keep)].copy()
    sup = suppliers.set_index("fornecedor_raiz")
    base_strength = sup.strength_raiz.astype(float).to_dict()
    base_degree = sup.degree_raiz.astype(float).to_dict()
    all_strength = suppliers.strength_raiz.astype(float).to_numpy()
    all_degree = suppliers.degree_raiz.astype(float).to_numpy()

    rows = []
    for buyer, g in r.groupby("orgao_cnpj", sort=False):
        sids = g.fornecedor_raiz.astype(str).to_numpy()
        shares = g.share_valor.astype(float).to_numpy()
        values = g.valor_relacao.astype(float).to_numpy()
        bs = np.asarray([base_strength[x] for x in sids], dtype=float)
        bd = np.asarray([base_degree[x] for x in sids], dtype=float)
        adj_s = np.maximum(bs - values, 0.0)
        adj_d = np.maximum(bd - 1.0, 0.0)
        pct_s = exact_loo_percentiles(all_strength, bs, adj_s)
        pct_d = exact_loo_percentiles(all_degree, bd, adj_d)
        rows.append({
            "orgao_cnpj": str(buyer),
            "exposicao_strength_loo_raiz": float(np.sum(shares * pct_s)),
            "exposicao_degree_loo_raiz": float(np.sum(shares * pct_d)),
        })
    return pd.DataFrame(rows)


def classify(d: pd.DataFrame, hhi: str, exp: str, name: str):
    qh = float(d[hhi].quantile(.75))
    qe = float(d[exp].quantile(.75))
    flag = d[hhi].lt(qh) & d[exp].ge(qe)
    return flag, {
        "name": name,
        "q75_hhi": qh,
        "q75_exposure": qe,
        "n": int(flag.sum()),
        "pct": float(flag.mean() * 100),
    }


def overlap_flags(a: pd.Series, b: pd.Series) -> float:
    aa = set(a.index[a].astype(str))
    bb = set(b.index[b].astype(str))
    return float(len(aa & bb) / len(aa)) if aa else np.nan


def stress_root(rel: pd.DataFrame, buyer_ids: pd.Series, suppliers: pd.DataFrame) -> pd.DataFrame:
    bids = sorted(set(buyer_ids.astype(str)))
    sids = sorted(suppliers.fornecedor_raiz.astype(str).unique())
    bi = {v: i for i, v in enumerate(bids)}
    si = {v: i for i, v in enumerate(sids)}
    r = rel[rel.orgao_cnpj.astype(str).isin(set(bids))].copy()
    rows_idx = r.orgao_cnpj.astype(str).map(bi).to_numpy()
    cols_idx = r.fornecedor_raiz.astype(str).map(si).to_numpy()
    vals = r.share_valor.astype(float).to_numpy()
    A = sparse.csr_matrix((vals, (rows_idx, cols_idx)), shape=(len(bids), len(sids)), dtype=np.float64)

    sup = suppliers.set_index("fornecedor_raiz").loc[sids].reset_index()
    strength = sup.strength_raiz.astype(float).to_numpy()
    p_weight = strength / strength.sum()
    rng = np.random.default_rng(SEED)
    out = []
    for pct in [.01, .05, .10]:
        k = max(1, int(math.ceil(len(sids) * pct)))
        target_idx = np.argpartition(strength, -k)[-k:]
        target_loss = np.asarray(A[:, target_idx].sum(axis=1)).ravel()
        severe = []
        for _ in range(DRAWS):
            idx = rng.choice(len(sids), size=k, replace=False, p=p_weight)
            loss = np.asarray(A[:, idx].sum(axis=1)).ravel()
            severe.append(float((loss >= .5).mean()))
        out.append({
            "pct_fornecedores": pct,
            "k": k,
            "massa_strength_topk": float(strength[target_idx].sum() / strength.sum()),
            "share_severos_target_50": float((target_loss >= .5).mean()),
            "weighted_random_share_severos_media": float(np.mean(severe)),
            "weighted_random_share_severos_p025": float(np.quantile(severe, .025)),
            "weighted_random_share_severos_p975": float(np.quantile(severe, .975)),
            "draws": DRAWS,
            "seed": SEED,
        })
    return pd.DataFrame(out)


def main():
    x = load_cohort()
    rel, root_buyers, root_suppliers = build_root_metrics(x)

    orig_dir = RES / "carteira_acumulada_2025_06_global"
    orig_buyers = pd.read_csv(orig_dir / "metricas_compradores.csv", dtype={"orgao_cnpj": "string"}, low_memory=False)
    orig_suppliers = pd.read_csv(orig_dir / "metricas_fornecedores_global.csv", low_memory=False)
    orig_eligible = orig_buyers[(orig_buyers.n_fornecedores >= 3) & (orig_buyers.n_instrumentos >= 5)].copy()
    orig_loo = pd.read_csv(
        RES / "robustez_estrutural_2025_06" / "leave_one_buyer_out.csv",
        dtype={"orgao_cnpj": "string"},
        low_memory=False,
    )

    fixed = (
        orig_eligible[[
            "orgao_cnpj", "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
            "n_fornecedores", "n_instrumentos"
        ]]
        .merge(root_buyers, on="orgao_cnpj", how="left", validate="one_to_one")
        .merge(
            orig_loo[["orgao_cnpj", "exposicao_strength_loo", "exposicao_degree_loo"]],
            on="orgao_cnpj", how="left", validate="one_to_one"
        )
    )
    root_loo_fixed = build_loo_root(rel, fixed.orgao_cnpj, root_suppliers)
    fixed = fixed.merge(root_loo_fixed, on="orgao_cnpj", how="left", validate="one_to_one")

    root_eligible = root_buyers[
        (root_buyers.n_fornecedores_raiz >= 3) & (root_buyers.n_instrumentos_raiz >= 5)
    ].copy()
    root_loo_eligible = build_loo_root(rel, root_eligible.orgao_cnpj, root_suppliers)
    root_eligible = root_eligible.merge(root_loo_eligible, on="orgao_cnpj", how="left", validate="one_to_one")

    fixed = fixed.set_index("orgao_cnpj", drop=False)
    f_orig_s, c_orig_s = classify(fixed, "portfolio_hhi", "exposicao_strength_loo", "original_strength_loo")
    f_root_s, c_root_s = classify(fixed, "portfolio_hhi_raiz", "exposicao_strength_loo_raiz", "root_strength_loo")
    f_orig_d, c_orig_d = classify(fixed, "portfolio_hhi", "exposicao_degree_loo", "original_degree_loo")
    f_root_d, c_root_d = classify(fixed, "portfolio_hhi_raiz", "exposicao_degree_loo_raiz", "root_degree_loo")

    mapping = (
        x[["fornecedor_id_limpo", "fornecedor_raiz"]]
        .drop_duplicates()
        .groupby("fornecedor_raiz")
        .agg(estabelecimentos=("fornecedor_id_limpo", "nunique"))
        .reset_index()
    )
    stress = stress_root(rel, fixed.orgao_cnpj, root_suppliers)

    summary = {
        "periodo": "publicacoes 2025-01-01 a 2025-06-30; instrumentos assinados em 2025",
        "unidade_robustez": "CNPJ raiz = 8 primeiros digitos do CNPJ de fornecedor PJ",
        "validacao_identificadores": {
            "registros_economicos": int(len(x)),
            "cnpj_14_valido_n": int(x.cnpj_14_valido.sum()),
            "cnpj_14_valido_pct": float(x.cnpj_14_valido.mean() * 100),
        },
        "estrutura_fornecedores": {
            "cnpjs_completos_rede_original": int(len(orig_suppliers)),
            "cnpj_raizes_rede": int(len(root_suppliers)),
            "raizes_com_multiplos_estabelecimentos_n": int((mapping.estabelecimentos > 1).sum()),
            "raizes_com_multiplos_estabelecimentos_pct": float((mapping.estabelecimentos > 1).mean() * 100),
            "max_estabelecimentos_mesma_raiz": int(mapping.estabelecimentos.max()),
        },
        "amostra_fixa_original": {
            "n_compradores": int(len(fixed)),
            "compradores_que_ficam_abaixo_3_fornecedores_raiz_n": int((fixed.n_fornecedores_raiz < 3).sum()),
            "medianas": {
                "hhi_original": float(fixed.portfolio_hhi.median()),
                "hhi_raiz": float(fixed.portfolio_hhi_raiz.median()),
                "hhi_norm_original": float(fixed.portfolio_hhi_norm.median()),
                "hhi_norm_raiz": float(fixed.portfolio_hhi_norm_raiz.median()),
                "cr1_original": float(fixed.portfolio_cr1.median()),
                "cr1_raiz": float(fixed.portfolio_cr1_raiz.median()),
                "n_fornecedores_original": float(fixed.n_fornecedores.median()),
                "n_fornecedores_raiz": float(fixed.n_fornecedores_raiz.median()),
                "strength_loo_original": float(fixed.exposicao_strength_loo.median()),
                "strength_loo_raiz": float(fixed.exposicao_strength_loo_raiz.median()),
                "degree_loo_original": float(fixed.exposicao_degree_loo.median()),
                "degree_loo_raiz": float(fixed.exposicao_degree_loo_raiz.median()),
            },
            "correlacoes_original_raiz": {
                "hhi_norm": spearman(fixed.portfolio_hhi_norm, fixed.portfolio_hhi_norm_raiz),
                "cr1": spearman(fixed.portfolio_cr1, fixed.portfolio_cr1_raiz),
                "n_fornecedores": spearman(fixed.n_fornecedores, fixed.n_fornecedores_raiz),
                "strength_loo": spearman(fixed.exposicao_strength_loo, fixed.exposicao_strength_loo_raiz),
                "degree_loo": spearman(fixed.exposicao_degree_loo, fixed.exposicao_degree_loo_raiz),
                "strength_loo_raiz_vs_degree_loo_raiz": spearman(fixed.exposicao_strength_loo_raiz, fixed.exposicao_degree_loo_raiz),
                "hhi_norm_raiz_vs_strength_loo_raiz": spearman(fixed.portfolio_hhi_norm_raiz, fixed.exposicao_strength_loo_raiz),
                "hhi_norm_raiz_vs_degree_loo_raiz": spearman(fixed.portfolio_hhi_norm_raiz, fixed.exposicao_degree_loo_raiz),
            },
            "discordancia": {
                "original_strength_loo": c_orig_s,
                "raiz_strength_loo": c_root_s,
                "retencao_original_para_raiz_strength": overlap_flags(f_orig_s, f_root_s),
                "original_degree_loo": c_orig_d,
                "raiz_degree_loo": c_root_d,
                "retencao_original_para_raiz_degree": overlap_flags(f_orig_d, f_root_d),
                "sobreposicao_strength_degree_na_raiz": overlap_flags(f_root_s, f_root_d),
            },
        },
        "elegibilidade_recalculada_raiz": {
            "n_compradores": int(len(root_eligible)),
            "diferenca_vs_original": int(len(root_eligible) - len(orig_eligible)),
        },
        "stress_test_raiz_amostra_fixa": stress.to_dict(orient="records"),
        "interpretacao": [
            "A comparacao em amostra fixa isola o efeito de agregar estabelecimentos pela raiz do CNPJ.",
            "A elegibilidade recalculada mostra se a agregacao altera o criterio minimo de fornecedores.",
            "CNPJ raiz nao equivale necessariamente a grupo economico; estruturas societarias com multiplas raizes permanecem separadas.",
        ],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    fixed.reset_index(drop=True).to_csv(OUT / "comparacao_amostra_fixa.csv", index=False, encoding="utf-8-sig")
    root_eligible.to_csv(OUT / "compradores_elegiveis_cnpj_raiz.csv", index=False, encoding="utf-8-sig")
    root_suppliers.to_csv(OUT / "fornecedores_cnpj_raiz.csv", index=False, encoding="utf-8-sig")
    mapping.to_csv(OUT / "mapeamento_estabelecimentos_por_raiz.csv", index=False, encoding="utf-8-sig")
    stress.to_csv(OUT / "stress_test_cnpj_raiz.csv", index=False, encoding="utf-8-sig")
    (OUT / "resumo_robustez_cnpj_raiz.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
