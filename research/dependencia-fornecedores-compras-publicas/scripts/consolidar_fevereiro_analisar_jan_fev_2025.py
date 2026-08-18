#!/usr/bin/env python3
"""Consolida fevereiro/2025 e calcula diagnóstico acumulado janeiro-fevereiro.

Escopo: publicações PNCP de 01/01/2025 a 28/02/2025, esfera municipal,
Poder Executivo, fornecedores PJ na base pública. Para as métricas econômicas,
consideram-se instrumentos assinados em 2025 e valorInicial > 0.

IMPORTANTE: janeiro-fevereiro ainda é uma coorte parcial de publicação e não
representa o estoque anual completo de contratos assinados em 2025.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results"
OUT_FEB = RES / "carteira_fevereiro_2025_diagnostico"
OUT_ACC = RES / "carteira_jan_fev_2025_diagnostico"
OUT_FEB.mkdir(parents=True, exist_ok=True)
OUT_ACC.mkdir(parents=True, exist_ok=True)

FEB_PARTS = [
    "2025-02-d01-d07",
    "2025-02-d08-d14",
    "2025-02-d15-d21",
    "2025-02-d22-d28",
]
SEED = 20260818
RANDOM_DRAWS = 1000


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_mixed(s: pd.Series) -> pd.Series:
    try:
        return pd.to_datetime(s, errors="coerce", format="mixed")
    except TypeError:
        return pd.to_datetime(s, errors="coerce")


def entropy_norm(shares: pd.Series) -> float:
    x = pd.to_numeric(shares, errors="coerce").dropna()
    x = x[x > 0]
    if len(x) <= 1:
        return 0.0 if len(x) == 1 else float("nan")
    return float(-(x * np.log(x)).sum() / math.log(len(x)))


def load_public(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        dtype={
            "id_contrato": "string",
            "id_compra": "string",
            "orgao_cnpj": "string",
            "orgao_compra_cnpj": "string",
            "municipio_ibge": "string",
            "fornecedor_id_limpo": "string",
        },
        low_memory=False,
    )


def consolidate_february() -> tuple[pd.DataFrame, Path, list[dict]]:
    frames, manifests, summaries = [], [], []
    for label in FEB_PARTS:
        p = DATA / f"pncp_{label}_municipal_pj.csv.gz"
        if not p.exists():
            raise FileNotFoundError(p)
        d = load_public(p)
        d["particao"] = label
        frames.append(d)
        manifests.append({"particao": label, "linhas": len(d), "sha256": sha256(p)})
        sp = RES / "pncp_mensal" / f"{label}_resumo.json"
        summaries.append(json.loads(sp.read_text(encoding="utf-8")))

    x = pd.concat(frames, ignore_index=True)
    x["data_publicacao"] = parse_mixed(x["data_publicacao"])
    x["data_assinatura"] = parse_mixed(x["data_assinatura"])
    x["valorInicial"] = pd.to_numeric(x["valorInicial"], errors="coerce")
    x["ano_assinatura"] = pd.to_numeric(x["ano_assinatura"], errors="coerce").astype("Int64")
    x["lag_publicacao_dias"] = pd.to_numeric(x["lag_publicacao_dias"], errors="coerce")

    dup = x.duplicated("id_contrato", keep=False)
    if dup.any():
        x.loc[dup, ["id_contrato", "particao"]].to_csv(
            OUT_FEB / "duplicidades_entre_particoes.csv", index=False, encoding="utf-8-sig"
        )
        raise RuntimeError(f"Duplicidades entre partições de fevereiro: {x.loc[dup, 'id_contrato'].nunique()}")

    invalid = x["data_publicacao"].isna()
    if invalid.any():
        raise RuntimeError(f"Datas de publicação não parseáveis em fevereiro: {int(invalid.sum())}")

    start, end = pd.Timestamp("2025-02-01"), pd.Timestamp("2025-03-01")
    outside = ~((x["data_publicacao"] >= start) & (x["data_publicacao"] < end))
    if outside.any():
        x.loc[outside, ["id_contrato", "data_publicacao", "particao"]].to_csv(
            OUT_FEB / "publicacoes_fora_fevereiro.csv", index=False, encoding="utf-8-sig"
        )
        raise RuntimeError(f"Publicações fora de fevereiro: {int(outside.sum())}")

    out_path = DATA / "pncp_2025-02_publicacoes_municipal_pj.csv.gz"
    x.drop(columns=["particao"]).to_csv(out_path, index=False, compression="gzip", encoding="utf-8")
    pd.DataFrame(manifests).to_csv(OUT_FEB / "manifesto_particoes.csv", index=False, encoding="utf-8-sig")

    summary = {
        "escopo": "Publicações PNCP de fevereiro de 2025; fornecedores PJ; esfera municipal; Poder Executivo.",
        "registros_pj": int(len(x)),
        "instrumentos_unicos": int(x["id_contrato"].nunique()),
        "duplicidades_id_contrato": int(x.duplicated("id_contrato").sum()),
        "compradores_unicos": int(x["orgao_cnpj"].nunique()),
        "fornecedores_pj_unicos": int(x["fornecedor_id_limpo"].nunique()),
        "municipios_unicos": int(x["municipio_ibge"].nunique()),
        "assinados_2025": int(x["ano_assinatura"].eq(2025).sum()),
        "assinados_antes_2025": int(x["ano_assinatura"].lt(2025).sum()),
        "lag_mediana": float(x["lag_publicacao_dias"].median()),
        "lag_p90": float(x["lag_publicacao_dias"].quantile(.90)),
        "lag_p95": float(x["lag_publicacao_dias"].quantile(.95)),
        "lag_negativo_n": int((x["lag_publicacao_dias"] < 0).sum()),
        "registros_brutos_particoes_soma": int(sum(s["registros_brutos"] for s in summaries)),
        "registros_municipais_validos_todos_tipos_soma": int(sum(s["registros_municipais_validos"] for s in summaries)),
        "registros_pf_soma": int(sum(s["registros_pf"] for s in summaries)),
        "registros_pe_soma": int(sum(s["registros_pe"] for s in summaries)),
        "janela_publicacao": {"min": x["data_publicacao"].min().isoformat(), "max": x["data_publicacao"].max().isoformat()},
        "sha256_base_pj_consolidada": sha256(out_path),
    }
    (OUT_FEB / "resumo_fevereiro.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return x.drop(columns=["particao"]), out_path, summaries


def calculate_metrics(df: pd.DataFrame):
    x = df[df["ano_assinatura"].eq(2025) & df["valorInicial"].gt(0)].copy()
    rel = (
        x.groupby(["orgao_cnpj", "fornecedor_id_limpo"], dropna=False)
        .agg(valor_relacao=("valorInicial", "sum"), n_instrumentos=("id_contrato", "nunique"))
        .reset_index()
    )
    rel["share_valor"] = rel["valor_relacao"] / rel.groupby("orgao_cnpj")["valor_relacao"].transform("sum")
    rel["share_contagem"] = rel["n_instrumentos"] / rel.groupby("orgao_cnpj")["n_instrumentos"].transform("sum")

    rows = []
    for buyer, g in rel.groupby("orgao_cnpj", sort=False):
        sv = g["share_valor"].sort_values(ascending=False)
        sc = g["share_contagem"].sort_values(ascending=False)
        hv, hc = float((sv**2).sum()), float((sc**2).sum())
        rows.append({
            "orgao_cnpj": buyer,
            "valor_total": float(g["valor_relacao"].sum()),
            "n_instrumentos": int(g["n_instrumentos"].sum()),
            "n_fornecedores": int(g["fornecedor_id_limpo"].nunique()),
            "portfolio_hhi": hv,
            "portfolio_cr1": float(sv.iloc[0]),
            "portfolio_cr4": float(sv.iloc[:4].sum()),
            "portfolio_neff": 1/hv if hv > 0 else np.nan,
            "portfolio_entropy_norm": entropy_norm(sv),
            "count_hhi": hc,
            "count_neff": 1/hc if hc > 0 else np.nan,
            "hhi_gap_value_minus_count": hv-hc,
        })
    buyers = pd.DataFrame(rows)

    suppliers = rel.groupby("fornecedor_id_limpo").agg(
        degree=("orgao_cnpj", "nunique"), strength=("valor_relacao", "sum")
    ).reset_index()
    nb = max(int(rel["orgao_cnpj"].nunique()), 1)
    suppliers["reach"] = suppliers["degree"] / nb
    suppliers["system_share"] = suppliers["strength"] / suppliers["strength"].sum()
    suppliers["pct_degree"] = suppliers["degree"].rank(pct=True, method="average")
    suppliers["pct_strength"] = suppliers["strength"].rank(pct=True, method="average")

    z = rel.merge(suppliers[["fornecedor_id_limpo", "pct_degree", "pct_strength"]], on="fornecedor_id_limpo", how="left")
    z["ed"] = z["share_valor"] * z["pct_degree"]
    z["es"] = z["share_valor"] * z["pct_strength"]
    exp = z.groupby("orgao_cnpj").agg(exposicao_degree=("ed", "sum"), exposicao_strength=("es", "sum")).reset_index()
    buyers = buyers.merge(exp, on="orgao_cnpj", how="left")
    return x, rel, buyers, suppliers


def spearman(a: pd.Series, b: pd.Series) -> dict:
    rho, p = spearmanr(a, b, nan_policy="omit")
    return {"rho": None if pd.isna(rho) else float(rho), "p": None if pd.isna(p) else float(p)}


def simulate(rel: pd.DataFrame, eligible_buyers: pd.Series) -> pd.DataFrame:
    r = rel[rel["orgao_cnpj"].isin(set(eligible_buyers.astype(str)))].copy()
    r["orgao_cnpj"] = r["orgao_cnpj"].astype(str)
    r["fornecedor_id_limpo"] = r["fornecedor_id_limpo"].astype(str)
    blist = sorted(r["orgao_cnpj"].unique())
    slist = sorted(r["fornecedor_id_limpo"].unique())
    bi = {v:i for i,v in enumerate(blist)}
    si = {v:i for i,v in enumerate(slist)}
    A = np.zeros((len(blist), len(slist)), dtype=float)
    for row in r.itertuples(index=False):
        A[bi[str(row.orgao_cnpj)], si[str(row.fornecedor_id_limpo)]] += float(row.share_valor)

    sup = r.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"), strength=("valor_relacao","sum")).reset_index()
    sup["idx"] = sup["fornecedor_id_limpo"].map(si)
    rng = np.random.default_rng(SEED)
    rows = []
    thresholds = [0.25, 0.50, 0.75]
    for pct in [0.01, 0.05, 0.10]:
        k = max(1, int(math.ceil(len(slist) * pct)))
        random_severe = {t: [] for t in thresholds}
        random_loss = []
        for _ in range(RANDOM_DRAWS):
            idx = rng.choice(len(slist), size=k, replace=False)
            loss = A[:, idx].sum(axis=1)
            random_loss.append(float(loss.mean()))
            for t in thresholds:
                random_severe[t].append(float((loss >= t).mean()))
        for strategy in ["degree", "strength"]:
            target = sup.nlargest(k, strategy)["idx"].astype(int).to_numpy()
            loss = A[:, target].sum(axis=1)
            for t in thresholds:
                rnd = np.array(random_severe[t])
                rows.append({
                    "estrategia": strategy,
                    "pct_fornecedores_removidos": pct,
                    "k": k,
                    "limiar_perda": t,
                    "share_severos_direcionado": float((loss >= t).mean()),
                    "share_severos_aleatorio_media": float(rnd.mean()),
                    "share_severos_aleatorio_p025": float(np.quantile(rnd, .025)),
                    "share_severos_aleatorio_p975": float(np.quantile(rnd, .975)),
                    "perda_media_direcionada": float(loss.mean()),
                    "perda_media_aleatoria_media": float(np.mean(random_loss)),
                    "perda_media_aleatoria_p025": float(np.quantile(random_loss,.025)),
                    "perda_media_aleatoria_p975": float(np.quantile(random_loss,.975)),
                })
    return pd.DataFrame(rows)


def main():
    feb, feb_path, _ = consolidate_february()
    jan_path = DATA / "pncp_2025-01_publicacoes_municipal_pj.csv.gz"
    jan = load_public(jan_path)
    for d in (jan, feb):
        d["data_publicacao"] = parse_mixed(d["data_publicacao"])
        d["data_assinatura"] = parse_mixed(d["data_assinatura"])
        d["valorInicial"] = pd.to_numeric(d["valorInicial"], errors="coerce")
        d["ano_assinatura"] = pd.to_numeric(d["ano_assinatura"], errors="coerce").astype("Int64")
        d["lag_publicacao_dias"] = pd.to_numeric(d["lag_publicacao_dias"], errors="coerce")

    acc = pd.concat([jan, feb], ignore_index=True)
    dup = acc.duplicated("id_contrato", keep=False)
    if dup.any():
        acc.loc[dup, ["id_contrato", "data_publicacao"]].to_csv(OUT_ACC/"duplicidades_jan_fev.csv", index=False, encoding="utf-8-sig")
        raise RuntimeError(f"IDs repetidos entre janeiro e fevereiro: {acc.loc[dup,'id_contrato'].nunique()}")

    cohort, rel, buyers, suppliers = calculate_metrics(acc)
    eligible = buyers[(buyers["n_fornecedores"] >= 3) & (buyers["n_instrumentos"] >= 5)].copy()
    sims = simulate(rel, eligible["orgao_cnpj"])

    rel.to_csv(OUT_ACC/"relacoes_jan_fev_assinados_2025.csv.gz", index=False, compression="gzip")
    buyers.to_csv(OUT_ACC/"metricas_compradores_jan_fev.csv", index=False, encoding="utf-8-sig")
    suppliers.to_csv(OUT_ACC/"metricas_fornecedores_jan_fev.csv", index=False, encoding="utf-8-sig")
    eligible.to_csv(OUT_ACC/"compradores_elegiveis_jan_fev.csv", index=False, encoding="utf-8-sig")
    sims.to_csv(OUT_ACC/"simulacoes_remocao_jan_fev.csv", index=False, encoding="utf-8-sig")

    qh = float(eligible["portfolio_hhi"].quantile(.75))
    qe = float(eligible["exposicao_strength"].quantile(.75))
    hidden = int(((eligible["portfolio_hhi"] < qh) & (eligible["exposicao_strength"] >= qe)).sum())
    both = int(((eligible["portfolio_hhi"] >= qh) & (eligible["exposicao_strength"] >= qe)).sum())

    summary = {
        "escopo": "Publicações PNCP janeiro-fevereiro de 2025; métricas sobre instrumentos assinados em 2025; fornecedores PJ.",
        "advertencia": "Coorte parcial de publicação. Não interpretar como resultado anual de 2025.",
        "registros_pj_jan_fev": int(len(acc)),
        "instrumentos_unicos": int(acc["id_contrato"].nunique()),
        "duplicidades": int(acc.duplicated("id_contrato").sum()),
        "assinados_2025": int(acc["ano_assinatura"].eq(2025).sum()),
        "compradores_metricas": int(len(buyers)),
        "compradores_elegiveis": int(len(eligible)),
        "fornecedores_rede_total": int(suppliers["fornecedor_id_limpo"].nunique()),
        "portfolio_hhi_mediana_elegiveis": float(eligible["portfolio_hhi"].median()),
        "count_hhi_mediana_elegiveis": float(eligible["count_hhi"].median()),
        "portfolio_neff_mediana_elegiveis": float(eligible["portfolio_neff"].median()),
        "portfolio_cr1_mediana_elegiveis": float(eligible["portfolio_cr1"].median()),
        "portfolio_cr4_mediana_elegiveis": float(eligible["portfolio_cr4"].median()),
        "spearman_portfolio_count": spearman(eligible["portfolio_hhi"], eligible["count_hhi"]),
        "spearman_portfolio_exposicao_strength": spearman(eligible["portfolio_hhi"], eligible["exposicao_strength"]),
        "q75_portfolio_hhi": qh,
        "q75_exposicao_strength": qe,
        "hhi_baixo_exposicao_alta_n": hidden,
        "hhi_alto_exposicao_alta_n": both,
        "portfolio_hhi_maior_count_hhi_n": int((eligible["portfolio_hhi"] > eligible["count_hhi"]).sum()),
        "portfolio_hhi_maior_count_hhi_pct": float((eligible["portfolio_hhi"] > eligible["count_hhi"]).mean()*100),
        "lag_negativo_n_jan_fev": int((acc["lag_publicacao_dias"] < 0).sum()),
        "random_draws_por_cenario": RANDOM_DRAWS,
        "seed": SEED,
        "sha256_janeiro": sha256(jan_path),
        "sha256_fevereiro": sha256(feb_path),
    }

    jan_buyers_path = RES / "carteira_janeiro_2025_diagnostico" / "metricas_compradores_assinados_2025_publicados_janeiro.csv"
    if jan_buyers_path.exists():
        jb = pd.read_csv(jan_buyers_path)
        je = jb[(jb["n_fornecedores"] >= 3) & (jb["n_instrumentos"] >= 5)].copy()
        stability = pd.DataFrame([
            {"periodo":"jan", "n_elegiveis":len(je), "hhi_mediana":je["portfolio_hhi"].median(), "neff_mediana":je["portfolio_neff"].median(), "cr1_mediana":je["portfolio_cr1"].median(), "cr4_mediana":je["portfolio_cr4"].median()},
            {"periodo":"jan_fev", "n_elegiveis":len(eligible), "hhi_mediana":eligible["portfolio_hhi"].median(), "neff_mediana":eligible["portfolio_neff"].median(), "cr1_mediana":eligible["portfolio_cr1"].median(), "cr4_mediana":eligible["portfolio_cr4"].median()},
        ])
        stability.to_csv(OUT_ACC/"estabilidade_jan_vs_jan_fev.csv", index=False, encoding="utf-8-sig")

    (OUT_ACC/"resumo_jan_fev.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\nSimulações, limiar 50%:")
    print(sims[sims["limiar_perda"].eq(.5)].to_string(index=False))


if __name__ == "__main__":
    main()
