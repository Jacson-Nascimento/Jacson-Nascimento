#!/usr/bin/env python3
"""Robustezes estruturais para os papers de dependência de fornecedores.

A especificação principal permanece preservada. Este script produz testes
separados para responder a objeções de mensuração:

1. centralidade Strength e Degree leave-one-buyer-out (LOO), retirando a
   contribuição do próprio comprador da posição global de cada fornecedor;
2. discordância HHI-exposição com medidas originais e externalizadas LOO;
3. alternativas contínuas à classificação em quadrantes;
4. stress test adicional com sorteio aleatório ponderado por Strength;
5. diagnóstico de quantos fornecedores aleatórios seriam necessários para
   remover massa sistêmica de Strength semelhante à dos maiores fornecedores.

Uso:
    python scripts/robustez_estrutural_generica.py --month 6

Comprador = CNPJ institucional. A chave de instrumento permanece
numeroControlePNCP, já materializada como id_contrato nas bases processadas.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import spearmanr
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
SEED = 20260820
DRAWS = 1000


def spearman(a, b):
    z = pd.DataFrame({"a": a, "b": b}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(z) < 3:
        return {"rho": None, "p": None, "n": int(len(z))}
    rho, p = spearmanr(z.a, z.b)
    return {"rho": float(rho), "p": float(p), "n": int(len(z))}


def exact_loo_percentiles(base_values: np.ndarray, portfolio_base: np.ndarray, portfolio_adj: np.ndarray) -> np.ndarray:
    """Midrank percentual após substituir valores dos fornecedores do comprador."""
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


def build_loo(rel: pd.DataFrame, eligible: pd.DataFrame, suppliers: pd.DataFrame) -> pd.DataFrame:
    rel = rel.copy()
    suppliers = suppliers.copy()
    rel["orgao_cnpj"] = rel.orgao_cnpj.astype("string")
    rel["fornecedor_id_limpo"] = rel.fornecedor_id_limpo.astype("string")
    suppliers["fornecedor_id_limpo"] = suppliers.fornecedor_id_limpo.astype("string")

    eligible_ids = set(eligible.orgao_cnpj.astype(str))
    rel_eligible = rel[rel.orgao_cnpj.astype(str).isin(eligible_ids)].copy()

    sup = suppliers.set_index("fornecedor_id_limpo")
    base_strength = sup.strength.astype(float).to_dict()
    base_degree = sup.degree.astype(float).to_dict()
    all_strength = suppliers.strength.astype(float).to_numpy()
    all_degree = suppliers.degree.astype(float).to_numpy()

    rows = []
    for buyer, g in rel_eligible.groupby("orgao_cnpj", sort=False):
        ids = g.fornecedor_id_limpo.astype(str).to_numpy()
        shares = g.share_valor.astype(float).to_numpy()
        values = g.valor_relacao.astype(float).to_numpy()
        bs = np.asarray([base_strength[x] for x in ids], dtype=float)
        bd = np.asarray([base_degree[x] for x in ids], dtype=float)

        # Externaliza a posição do fornecedor em relação ao comprador focal.
        adj_s = np.maximum(bs - values, 0.0)
        adj_d = np.maximum(bd - 1.0, 0.0)
        pct_s = exact_loo_percentiles(all_strength, bs, adj_s)
        pct_d = exact_loo_percentiles(all_degree, bd, adj_d)

        own_share_strength = np.divide(values, bs, out=np.zeros_like(values), where=bs > 0)
        rows.append({
            "orgao_cnpj": str(buyer),
            "exposicao_strength_loo": float(np.sum(shares * pct_s)),
            "exposicao_degree_loo": float(np.sum(shares * pct_d)),
            "contribuicao_propria_strength_media_ponderada": float(np.sum(shares * own_share_strength)),
        })

    out = pd.DataFrame(rows)
    keep = [
        "orgao_cnpj", "portfolio_hhi", "portfolio_hhi_norm", "n_fornecedores",
        "n_instrumentos", "exposicao_strength_global", "exposicao_degree_global"
    ]
    out = eligible[keep].merge(out, on="orgao_cnpj", how="left")
    out["delta_strength_loo"] = out.exposicao_strength_loo - out.exposicao_strength_global
    out["delta_degree_loo"] = out.exposicao_degree_loo - out.exposicao_degree_global
    return out


def classify_discordance(d: pd.DataFrame, exposure_col: str, prefix: str) -> tuple[pd.DataFrame, dict]:
    z = d.copy()
    qh = float(z.portfolio_hhi.quantile(.75))
    qe = float(z[exposure_col].quantile(.75))
    flag = (z.portfolio_hhi < qh) & (z[exposure_col] >= qe)
    z[f"discordancia_{prefix}"] = flag
    return z, {
        "exposure_col": exposure_col,
        "q75_hhi": qh,
        "q75_exposure": qe,
        "n": int(flag.sum()),
        "pct": float(flag.mean() * 100),
        "spearman_hhi_norm_exposure": spearman(z.portfolio_hhi_norm, z[exposure_col]),
    }


def hidden_alternatives(eligible: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    d = eligible.copy()
    d["pct_hhi_norm"] = d.portfolio_hhi_norm.rank(pct=True, method="average")
    d["pct_exposure_strength"] = d.exposicao_strength_global.rank(pct=True, method="average")
    d["gap_percentil_exposure_hhi"] = d.pct_exposure_strength - d.pct_hhi_norm

    X = sm.add_constant(d[["portfolio_hhi_norm"]].astype(float))
    m = sm.OLS(d.exposicao_strength_global.astype(float), X, missing="drop").fit()
    d["residuo_exposure_hhi"] = m.resid
    q_gap = float(d.gap_percentil_exposure_hhi.quantile(.75))
    q_resid = float(d.residuo_exposure_hhi.quantile(.75))
    d["sobreexposicao_gap_q75"] = d.gap_percentil_exposure_hhi >= q_gap
    d["sobreexposicao_resid_q75"] = d.residuo_exposure_hhi >= q_resid

    return d, {
        "benchmark_independencia_quadrante_pct": 18.75,
        "gap_percentil_q75": q_gap,
        "residuo_q75": q_resid,
        "ols_exposure_hhi_coef": float(m.params["portfolio_hhi_norm"]),
        "ols_exposure_hhi_r2": float(m.rsquared),
        "interpretacao": "Medidas contínuas de discordância; não representam fraude, favorecimento ou risco causal.",
    }


def matrix_for_stress(rel: pd.DataFrame, eligible_ids: pd.Series, suppliers: pd.DataFrame):
    bids = sorted(set(eligible_ids.astype(str)))
    sids = sorted(suppliers.fornecedor_id_limpo.astype(str).unique())
    bi = {v: i for i, v in enumerate(bids)}
    si = {v: i for i, v in enumerate(sids)}
    r = rel[rel.orgao_cnpj.astype(str).isin(set(bids))].copy()
    rows = r.orgao_cnpj.astype(str).map(bi).to_numpy()
    cols = r.fornecedor_id_limpo.astype(str).map(si).to_numpy()
    vals = r.share_valor.astype(float).to_numpy()
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(len(bids), len(sids)), dtype=np.float64)
    sup = suppliers.copy()
    sup["fornecedor_id_limpo"] = sup.fornecedor_id_limpo.astype(str)
    sup = sup.set_index("fornecedor_id_limpo").loc[sids].reset_index()
    return A, sup


def stress_robustness(rel: pd.DataFrame, eligible_ids: pd.Series, suppliers: pd.DataFrame) -> pd.DataFrame:
    A, sup = matrix_for_stress(rel, eligible_ids, suppliers)
    strength = sup.strength.astype(float).to_numpy()
    total_strength = float(strength.sum())
    n_sup = len(strength)
    rng = np.random.default_rng(SEED)
    p_weight = strength / total_strength
    rows = []

    for pct in [.01, .05, .10]:
        k = max(1, int(math.ceil(n_sup * pct)))
        target_idx = np.argpartition(strength, -k)[-k:]
        target_mass = float(strength[target_idx].sum() / total_strength)
        target_loss = np.asarray(A[:, target_idx].sum(axis=1)).ravel()

        weighted_severe, weighted_loss, weighted_mass = [], [], []
        mass_severe, mass_loss, mass_k, mass_actual = [], [], [], []

        for _ in range(DRAWS):
            # Nulo mais forte: mesmo k, mas fornecedores de maior Strength têm maior chance de sorteio.
            idx_w = rng.choice(n_sup, size=k, replace=False, p=p_weight)
            loss_w = np.asarray(A[:, idx_w].sum(axis=1)).ravel()
            weighted_loss.append(float(loss_w.mean()))
            weighted_severe.append(float((loss_w >= .5).mean()))
            weighted_mass.append(float(strength[idx_w].sum() / total_strength))

            # Diagnóstico, não contrafactual de desempenho: quantos fornecedores
            # de uma permutação uniforme são necessários para alcançar massa de
            # Strength semelhante à concentração dos top-k?
            perm = rng.permutation(n_sup)
            cs = np.cumsum(strength[perm]) / total_strength
            stop = int(np.searchsorted(cs, target_mass, side="left")) + 1
            idx_m = perm[:stop]
            loss_m = np.asarray(A[:, idx_m].sum(axis=1)).ravel()
            mass_loss.append(float(loss_m.mean()))
            mass_severe.append(float((loss_m >= .5).mean()))
            mass_k.append(stop)
            mass_actual.append(float(strength[idx_m].sum() / total_strength))

        rows.append({
            "pct_fornecedores_target": pct,
            "k_target": k,
            "massa_strength_target": target_mass,
            "share_severos_target_50": float((target_loss >= .5).mean()),
            "perda_media_target": float(target_loss.mean()),
            "weighted_random_share_severos_media": float(np.mean(weighted_severe)),
            "weighted_random_share_severos_p025": float(np.quantile(weighted_severe, .025)),
            "weighted_random_share_severos_p975": float(np.quantile(weighted_severe, .975)),
            "weighted_random_perda_media": float(np.mean(weighted_loss)),
            "weighted_random_massa_media": float(np.mean(weighted_mass)),
            "diagnostico_massa_k_mediana": float(np.median(mass_k)),
            "diagnostico_massa_k_p025": float(np.quantile(mass_k, .025)),
            "diagnostico_massa_k_p975": float(np.quantile(mass_k, .975)),
            "diagnostico_massa_strength_media": float(np.mean(mass_actual)),
            "diagnostico_massa_share_severos_media": float(np.mean(mass_severe)),
            "diagnostico_massa_perda_media": float(np.mean(mass_loss)),
            "draws": DRAWS,
            "seed": SEED,
        })
    return pd.DataFrame(rows)


def overlap_rate(a: pd.Series, b: pd.Series) -> float:
    aa = set(a.astype(str))
    bb = set(b.astype(str))
    return float(len(aa & bb) / len(aa)) if aa else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", type=int, required=True, choices=range(1, 13))
    a = ap.parse_args()
    m = a.month

    src = RES / f"carteira_acumulada_2025_{m:02d}_global"
    rel_path = src / "relacoes.csv.gz"
    buyers_path = src / "metricas_compradores.csv"
    sup_path = src / "metricas_fornecedores_global.csv"
    for p in [rel_path, buyers_path, sup_path]:
        if not p.exists():
            raise FileNotFoundError(p)

    rel = pd.read_csv(rel_path, dtype={"orgao_cnpj": "string", "fornecedor_id_limpo": "string"}, low_memory=False)
    buyers = pd.read_csv(buyers_path, dtype={"orgao_cnpj": "string"}, low_memory=False)
    suppliers = pd.read_csv(sup_path, dtype={"fornecedor_id_limpo": "string"}, low_memory=False)
    eligible = buyers[(buyers.n_fornecedores >= 3) & (buyers.n_instrumentos >= 5)].copy()

    loo = build_loo(rel, eligible, suppliers)
    alt, alt_summary = hidden_alternatives(eligible)
    stress = stress_robustness(rel, eligible.orgao_cnpj, suppliers)

    # Classificações com exposição original e externalizada.
    c_raw, raw_sum = classify_discordance(loo, "exposicao_strength_global", "strength_raw")
    c_sloo, sloo_sum = classify_discordance(c_raw, "exposicao_strength_loo", "strength_loo")
    c_dloo, dloo_sum = classify_discordance(c_sloo, "exposicao_degree_loo", "degree_loo")

    raw_ids = c_dloo.loc[c_dloo.discordancia_strength_raw, "orgao_cnpj"]
    sloo_ids = c_dloo.loc[c_dloo.discordancia_strength_loo, "orgao_cnpj"]
    dloo_ids = c_dloo.loc[c_dloo.discordancia_degree_loo, "orgao_cnpj"]

    q_raw_s = float(loo.exposicao_strength_global.quantile(.75))
    q_loo_s = float(loo.exposicao_strength_loo.quantile(.75))
    q_raw_d = float(loo.exposicao_degree_global.quantile(.75))
    q_loo_d = float(loo.exposicao_degree_loo.quantile(.75))

    old_top_s = loo.loc[loo.exposicao_strength_global >= q_raw_s, "orgao_cnpj"]
    loo_top_s = loo.loc[loo.exposicao_strength_loo >= q_loo_s, "orgao_cnpj"]
    old_top_d = loo.loc[loo.exposicao_degree_global >= q_raw_d, "orgao_cnpj"]
    loo_top_d = loo.loc[loo.exposicao_degree_loo >= q_loo_d, "orgao_cnpj"]

    out = RES / f"robustez_estrutural_2025_{m:02d}"
    out.mkdir(parents=True, exist_ok=True)
    c_dloo.to_csv(out / "leave_one_buyer_out.csv", index=False, encoding="utf-8-sig")
    alt.to_csv(out / "alternativas_exposicao_discordante.csv", index=False, encoding="utf-8-sig")
    stress.to_csv(out / "stress_tests_alternativos.csv", index=False, encoding="utf-8-sig")

    summary = {
        "mes_final": m,
        "natureza": "Robustezes; especificacao principal de coleta e choques preservada.",
        "distincao_conceitual": {
            "strength_raw": "Importancia sistemica monetaria do fornecedor; permanece ranking principal dos choques.",
            "exposicao_strength_loo": "Exposicao externa do comprador baseada em Strength após retirar sua propria contribuicao.",
            "exposicao_degree_loo": "Exposicao externa complementar baseada em alcance do fornecedor após retirar o comprador focal.",
        },
        "leave_one_buyer_out": {
            "n": int(len(loo)),
            "spearman_strength_original_loo": spearman(loo.exposicao_strength_global, loo.exposicao_strength_loo),
            "spearman_degree_original_loo": spearman(loo.exposicao_degree_global, loo.exposicao_degree_loo),
            "spearman_strength_loo_degree_loo": spearman(loo.exposicao_strength_loo, loo.exposicao_degree_loo),
            "delta_strength_mediana": float(loo.delta_strength_loo.median()),
            "delta_strength_p05": float(loo.delta_strength_loo.quantile(.05)),
            "delta_strength_p95": float(loo.delta_strength_loo.quantile(.95)),
            "delta_degree_mediana": float(loo.delta_degree_loo.median()),
            "retencao_top_quartil_strength": overlap_rate(old_top_s, loo_top_s),
            "retencao_top_quartil_degree": overlap_rate(old_top_d, loo_top_d),
            "contribuicao_propria_strength_mediana": float(loo.contribuicao_propria_strength_media_ponderada.median()),
        },
        "discordancia_concentracao_exposicao": {
            "benchmark_independencia_pct": 18.75,
            "strength_raw": raw_sum,
            "strength_loo": sloo_sum,
            "degree_loo": dloo_sum,
            "retencao_classificacao_raw_para_strength_loo": overlap_rate(raw_ids, sloo_ids),
            "retencao_classificacao_raw_para_degree_loo": overlap_rate(raw_ids, dloo_ids),
            "sobreposicao_strength_loo_degree_loo": overlap_rate(sloo_ids, dloo_ids),
            "regra_interpretacao": "Classificacao mede discordancia entre dimensoes; nao deve ser tratada como prevalencia anormal, fraude ou risco causal.",
        },
        "alternativas_continuas": alt_summary,
        "stress_tests_alternativos": stress.to_dict(orient="records"),
        "interpretacao": [
            "Strength bruto continua adequado para ordenar importancia sistemica monetaria nos choques, mas nao deve ser tratado como medida puramente externa da exposicao do comprador.",
            "Para screening de exposicao externa, reportar prioritariamente Strength LOO e Degree LOO.",
            "O weighted-random e o contrafactual adicional comparavel por k; o diagnostico de massa sistemica mostra quantos fornecedores aleatorios seriam necessarios para reproduzir a massa de Strength dos top-k e nao deve ser interpretado como teste de superioridade do ataque direcionado.",
        ],
    }
    (out / "resumo_robustez_estrutural.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
