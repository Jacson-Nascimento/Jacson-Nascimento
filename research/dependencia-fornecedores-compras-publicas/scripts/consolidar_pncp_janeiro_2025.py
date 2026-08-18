#!/usr/bin/env python3
"""Consolida as quatro partições de publicações PNCP de janeiro de 2025.

Saídas são diagnósticas. Janeiro de publicação NÃO representa o estoque anual de
contratos assinados em 2025, pois há defasagem entre assinatura e publicação.
A base identificada permanece restrita a fornecedores PJ.
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
DATA_DIR = ROOT / "data" / "processed" / "pncp_mensal"
RESULT_DIR = ROOT / "results" / "pncp_mensal"
OUT_DIR = ROOT / "results" / "carteira_janeiro_2025_diagnostico"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PARTS = [
    "2025-01-d01-d08",
    "2025-01-d09-d16",
    "2025-01-d17-d24",
    "2025-01-d25-d31",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def entropy_norm(shares: pd.Series) -> float:
    x = pd.to_numeric(shares, errors="coerce").dropna()
    x = x[x > 0]
    if len(x) == 0:
        return float("nan")
    if len(x) == 1:
        return 0.0
    return float(-(x * np.log(x)).sum() / math.log(len(x)))


def bool_series(s: pd.Series) -> pd.Series:
    return s.astype("string").str.lower().isin(["true", "1", "sim"])


def load_parts():
    frames = []
    manifests = []
    partition_summaries = []
    for label in PARTS:
        path = DATA_DIR / f"pncp_{label}_municipal_pj.csv.gz"
        if not path.exists():
            raise FileNotFoundError(path)
        d = pd.read_csv(
            path,
            dtype={
                "id_contrato": "string",
                "id_compra": "string",
                "orgao_cnpj": "string",
                "orgao_compra_cnpj": "string",
                "municipio_ibge": "string",
                "fornecedor_id_limpo": "string",
            },
        )
        d["particao"] = label
        frames.append(d)
        manifests.append({
            "particao": label,
            "arquivo": str(path.relative_to(ROOT)),
            "linhas_pj": int(len(d)),
            "sha256": sha256(path),
        })
        summary_path = RESULT_DIR / f"{label}_resumo.json"
        partition_summaries.append(json.loads(summary_path.read_text(encoding="utf-8")))
    return pd.concat(frames, ignore_index=True), pd.DataFrame(manifests), partition_summaries


def validate_and_consolidate(df: pd.DataFrame):
    x = df.copy()
    x["data_publicacao"] = pd.to_datetime(x["data_publicacao"], errors="coerce")
    x["data_assinatura"] = pd.to_datetime(x["data_assinatura"], errors="coerce")
    x["valorInicial"] = pd.to_numeric(x["valorInicial"], errors="coerce")
    x["ano_assinatura"] = pd.to_numeric(x["ano_assinatura"], errors="coerce").astype("Int64")
    x["lag_publicacao_dias"] = pd.to_numeric(x["lag_publicacao_dias"], errors="coerce")

    dup_mask = x.duplicated("id_contrato", keep=False)
    duplicates = x.loc[dup_mask].sort_values(["id_contrato", "particao"])
    duplicates.to_csv(OUT_DIR / "instrumentos_duplicados_entre_particoes.csv", index=False, encoding="utf-8-sig")

    # Não deduplicar silenciosamente. Se houver duplicidade entre intervalos não sobrepostos,
    # o problema precisa ser classificado antes da análise substantiva.
    if dup_mask.any():
        dup_ids = int(x.loc[dup_mask, "id_contrato"].nunique())
        raise RuntimeError(f"Foram encontrados {dup_ids} IDs de contrato repetidos entre partições.")

    min_pub = x["data_publicacao"].min()
    max_pub = x["data_publicacao"].max()
    outside = x[~x["data_publicacao"].between(pd.Timestamp("2025-01-01"), pd.Timestamp("2025-01-31"), inclusive="both")]
    if len(outside):
        outside.to_csv(OUT_DIR / "publicacoes_fora_janeiro.csv", index=False, encoding="utf-8-sig")
        raise RuntimeError(f"Há {len(outside)} registros com data de publicação fora de janeiro de 2025.")

    out_path = DATA_DIR / "pncp_2025-01_publicacoes_municipal_pj.csv.gz"
    x.drop(columns=["particao"]).to_csv(out_path, index=False, compression="gzip", encoding="utf-8")
    return x, out_path, min_pub, max_pub


def calculate_portfolio_metrics(df: pd.DataFrame):
    # Diagnóstico principal deste estágio: contratos assinados em 2025 que já tinham sido
    # publicados em janeiro. Isto é uma coorte parcial, não o ano completo.
    x = df[df["ano_assinatura"].eq(2025)].copy()
    x = x[x["valorInicial"].gt(0)].copy()

    rel = (
        x.groupby(["orgao_cnpj", "fornecedor_id_limpo"], dropna=False)
        .agg(
            valor_relacao=("valorInicial", "sum"),
            n_instrumentos=("id_contrato", "nunique"),
        )
        .reset_index()
    )
    rel["share_valor"] = rel["valor_relacao"] / rel.groupby("orgao_cnpj")["valor_relacao"].transform("sum")
    rel["share_contagem"] = rel["n_instrumentos"] / rel.groupby("orgao_cnpj")["n_instrumentos"].transform("sum")

    rows = []
    for buyer, g in rel.groupby("orgao_cnpj", sort=False):
        sv = g["share_valor"].sort_values(ascending=False)
        sc = g["share_contagem"].sort_values(ascending=False)
        hv = float((sv ** 2).sum())
        hc = float((sc ** 2).sum())
        rows.append({
            "orgao_cnpj": buyer,
            "valor_total_publicado_jan_assinado_2025": float(g["valor_relacao"].sum()),
            "n_instrumentos": int(g["n_instrumentos"].sum()),
            "n_fornecedores": int(g["fornecedor_id_limpo"].nunique()),
            "portfolio_hhi": hv,
            "portfolio_hhi_10000": hv * 10000,
            "portfolio_cr1": float(sv.iloc[0]),
            "portfolio_cr4": float(sv.iloc[:4].sum()),
            "portfolio_neff": 1 / hv if hv > 0 else float("nan"),
            "portfolio_entropy_norm": entropy_norm(sv),
            "count_hhi": hc,
            "count_hhi_10000": hc * 10000,
            "count_cr1": float(sc.iloc[0]),
            "count_cr4": float(sc.iloc[:4].sum()),
            "count_neff": 1 / hc if hc > 0 else float("nan"),
            "count_entropy_norm": entropy_norm(sc),
            "hhi_gap_value_minus_count": hv - hc,
        })
    buyers = pd.DataFrame(rows)

    if len(x):
        ext = bool_series(x["origem_externa"])
        z = x.assign(valor_externo=np.where(ext, x["valorInicial"], 0.0))
        shared = (
            z.groupby("orgao_cnpj")
            .agg(valor_total_aux=("valorInicial", "sum"), valor_externo=("valor_externo", "sum"))
            .reset_index()
        )
        shared["shared_procurement_share"] = shared["valor_externo"] / shared["valor_total_aux"]
        buyers = buyers.merge(shared[["orgao_cnpj", "shared_procurement_share"]], on="orgao_cnpj", how="left")

        cat = (
            x.groupby(["orgao_cnpj", "categoria"], dropna=False)["valorInicial"]
            .sum().rename("valor_categoria").reset_index()
        )
        cat["share_categoria"] = cat["valor_categoria"] / cat.groupby("orgao_cnpj")["valor_categoria"].transform("sum")
        cat["hhi_piece"] = cat["share_categoria"] ** 2
        catmix = (
            cat.groupby("orgao_cnpj")
            .agg(category_mix_hhi=("hhi_piece", "sum"), n_categorias=("categoria", "nunique"), categoria_cr1=("share_categoria", "max"))
            .reset_index()
        )
        buyers = buyers.merge(catmix, on="orgao_cnpj", how="left")

    # Rede fornecedor-comprador dentro da coorte parcial de janeiro.
    suppliers = (
        rel.groupby("fornecedor_id_limpo")
        .agg(degree=("orgao_cnpj", "nunique"), strength=("valor_relacao", "sum"))
        .reset_index()
    )
    nbuyers = max(int(rel["orgao_cnpj"].nunique()), 1)
    suppliers["reach"] = suppliers["degree"] / nbuyers
    suppliers["system_share"] = suppliers["strength"] / suppliers["strength"].sum()
    suppliers["pct_degree"] = suppliers["degree"].rank(pct=True, method="average")
    suppliers["pct_strength"] = suppliers["strength"].rank(pct=True, method="average")

    ez = rel.merge(suppliers[["fornecedor_id_limpo", "pct_degree", "pct_strength"]], on="fornecedor_id_limpo", how="left")
    ez["ed_piece"] = ez["share_valor"] * ez["pct_degree"]
    ez["es_piece"] = ez["share_valor"] * ez["pct_strength"]
    exposure = ez.groupby("orgao_cnpj").agg(exposicao_degree=("ed_piece", "sum"), exposicao_strength=("es_piece", "sum")).reset_index()
    buyers = buyers.merge(exposure, on="orgao_cnpj", how="left")

    return x, rel, buyers, suppliers


def diagnostics(df: pd.DataFrame, buyers: pd.DataFrame, partition_summaries: list[dict], consolidated_path: Path):
    signed_counts = df["ano_assinatura"].value_counts(dropna=False).sort_index().rename_axis("ano_assinatura").reset_index(name="n")
    signed_counts.to_csv(OUT_DIR / "distribuicao_ano_assinatura.csv", index=False, encoding="utf-8-sig")

    eligible = buyers[(buyers["n_fornecedores"] >= 3) & (buyers["n_instrumentos"] >= 5)].copy()
    if len(eligible) >= 3:
        rho, pval = spearmanr(eligible["portfolio_hhi"], eligible["count_hhi"], nan_policy="omit")
        qv = eligible["portfolio_hhi"].quantile(.75)
        qc = eligible["count_hhi"].quantile(.75)
        both_top = int(((eligible["portfolio_hhi"] >= qv) & (eligible["count_hhi"] >= qc)).sum())
    else:
        rho = pval = float("nan")
        qv = qc = float("nan")
        both_top = 0

    lag = df["lag_publicacao_dias"].dropna()
    summary = {
        "escopo": "Publicações de 01/01/2025 a 31/01/2025, fornecedores PJ, esfera municipal, Poder Executivo.",
        "advertencia": "Métricas de carteira para contratos assinados em 2025 são diagnósticas e incompletas. Contratos assinados em 2025 podem ser publicados após janeiro.",
        "registros_pj_consolidados": int(len(df)),
        "instrumentos_unicos": int(df["id_contrato"].nunique()),
        "duplicidades_id_contrato": int(df.duplicated("id_contrato").sum()),
        "compradores_unicos": int(df["orgao_cnpj"].nunique()),
        "fornecedores_pj_unicos": int(df["fornecedor_id_limpo"].nunique()),
        "municipios_unicos": int(df["municipio_ibge"].nunique()),
        "assinados_2025_publicados_janeiro": int(df["ano_assinatura"].eq(2025).sum()),
        "assinados_antes_2025_publicados_janeiro": int(df["ano_assinatura"].lt(2025).sum()),
        "lag_mediana_dias_pj": float(lag.median()) if len(lag) else None,
        "lag_p90_dias_pj": float(lag.quantile(.90)) if len(lag) else None,
        "lag_p95_dias_pj": float(lag.quantile(.95)) if len(lag) else None,
        "lag_negativo_n_pj": int((df["lag_publicacao_dias"] < 0).sum()),
        "compradores_metricas_assinados_2025": int(len(buyers)),
        "compradores_elegiveis_diag_n3_forn_n5_instr": int(len(eligible)),
        "spearman_portfolio_count_elegiveis": None if pd.isna(rho) else float(rho),
        "spearman_pvalue": None if pd.isna(pval) else float(pval),
        "portfolio_hhi_q75_elegiveis": None if pd.isna(qv) else float(qv),
        "count_hhi_q75_elegiveis": None if pd.isna(qc) else float(qc),
        "compradores_top_quartil_ambas_medidas": both_top,
        "registros_brutos_particoes_soma": int(sum(s["registros_brutos"] for s in partition_summaries)),
        "registros_municipais_validos_todos_tipos_soma": int(sum(s["registros_municipais_validos"] for s in partition_summaries)),
        "registros_pf_soma": int(sum(s["registros_pf"] for s in partition_summaries)),
        "registros_pe_soma": int(sum(s["registros_pe"] for s in partition_summaries)),
        "sha256_base_pj_consolidada": sha256(consolidated_path),
        "arquivo_base_pj_consolidada": str(consolidated_path.relative_to(ROOT)),
    }
    (OUT_DIR / "resumo_diagnostico.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main():
    df, manifest, partition_summaries = load_parts()
    manifest.to_csv(OUT_DIR / "manifesto_particoes.csv", index=False, encoding="utf-8-sig")
    df, consolidated_path, min_pub, max_pub = validate_and_consolidate(df)
    cohort, rel, buyers, suppliers = calculate_portfolio_metrics(df)
    rel.to_csv(OUT_DIR / "relacoes_assinados_2025_publicados_janeiro.csv.gz", index=False, compression="gzip")
    buyers.to_csv(OUT_DIR / "metricas_compradores_assinados_2025_publicados_janeiro.csv", index=False, encoding="utf-8-sig")
    suppliers.to_csv(OUT_DIR / "metricas_fornecedores_assinados_2025_publicados_janeiro.csv", index=False, encoding="utf-8-sig")
    summary = diagnostics(df, buyers, partition_summaries, consolidated_path)
    summary["data_publicacao_min"] = min_pub.date().isoformat() if pd.notna(min_pub) else None
    summary["data_publicacao_max"] = max_pub.date().isoformat() if pd.notna(max_pub) else None
    summary["registros_coorte_metricas"] = int(len(cohort))
    (OUT_DIR / "resumo_diagnostico.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
