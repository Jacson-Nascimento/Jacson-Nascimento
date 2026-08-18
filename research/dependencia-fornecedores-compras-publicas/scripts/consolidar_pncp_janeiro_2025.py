#!/usr/bin/env python3
"""Consolida as quatro partições PNCP de janeiro de 2025.

Saídas são diagnósticas. Janeiro de publicação NÃO representa o estoque anual de
contratos assinados em 2025, pois há defasagem entre assinatura e publicação.
A base identificada permanece restrita a fornecedores PJ.

Correções de validação:
- intervalo de publicação tratado como [2025-01-01, 2025-02-01);
- parsing explícito de formatos mistos;
- datas não parseáveis são diagnosticadas separadamente;
- duplicidades entre partições continuam bloqueando a execução.
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

JAN_START = pd.Timestamp("2025-01-01")
FEB_START = pd.Timestamp("2025-02-01")


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
    return s.astype("string").str.strip().str.lower().isin(["true", "1", "sim"])


def parse_datetime_mixed(s: pd.Series) -> pd.Series:
    """Parseia datas ISO/CSV com ou sem hora sem depender do formato da primeira linha."""
    try:
        return pd.to_datetime(s, format="mixed", errors="coerce")
    except TypeError:
        return pd.to_datetime(s, errors="coerce")


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
            low_memory=False,
        )
        d["particao"] = label
        frames.append(d)
        manifests.append(
            {
                "particao": label,
                "arquivo": str(path.relative_to(ROOT)),
                "linhas_pj": int(len(d)),
                "sha256": sha256(path),
            }
        )
        summary_path = RESULT_DIR / f"{label}_resumo.json"
        partition_summaries.append(
            json.loads(summary_path.read_text(encoding="utf-8"))
        )
    return (
        pd.concat(frames, ignore_index=True),
        pd.DataFrame(manifests),
        partition_summaries,
    )


def validate_and_consolidate(df: pd.DataFrame):
    x = df.copy()
    x["data_publicacao"] = parse_datetime_mixed(x["data_publicacao"])
    x["data_assinatura"] = parse_datetime_mixed(x["data_assinatura"])
    x["valorInicial"] = pd.to_numeric(x["valorInicial"], errors="coerce")
    x["ano_assinatura"] = (
        pd.to_numeric(x["ano_assinatura"], errors="coerce").astype("Int64")
    )
    x["lag_publicacao_dias"] = pd.to_numeric(
        x["lag_publicacao_dias"], errors="coerce"
    )

    dup_mask = x.duplicated("id_contrato", keep=False)
    dup_summary = (
        x.loc[dup_mask]
        .groupby("particao", dropna=False)
        .agg(
            linhas_duplicadas=("id_contrato", "size"),
            ids_duplicados=("id_contrato", "nunique"),
        )
        .reset_index()
    )
    dup_summary.to_csv(
        OUT_DIR / "resumo_duplicidades_entre_particoes.csv",
        index=False,
        encoding="utf-8-sig",
    )
    if dup_mask.any():
        dup_ids = int(x.loc[dup_mask, "id_contrato"].nunique())
        raise RuntimeError(
            f"Foram encontrados {dup_ids} IDs de contrato repetidos entre partições."
        )

    invalid_pub = x["data_publicacao"].isna()
    invalid_summary = (
        x.assign(data_publicacao_invalida=invalid_pub)
        .groupby("particao", dropna=False)["data_publicacao_invalida"]
        .agg(["size", "sum"])
        .reset_index()
        .rename(columns={"size": "linhas", "sum": "datas_publicacao_invalidas"})
    )
    invalid_summary.to_csv(
        OUT_DIR / "resumo_datas_publicacao_invalidas.csv",
        index=False,
        encoding="utf-8-sig",
    )
    if invalid_pub.any():
        raise RuntimeError(
            f"Há {int(invalid_pub.sum())} registros com data de publicação não parseável."
        )

    in_january = (x["data_publicacao"] >= JAN_START) & (
        x["data_publicacao"] < FEB_START
    )
    outside = x.loc[~in_january].copy()
    outside_summary = (
        outside.assign(
            data_publicacao_dia=outside["data_publicacao"].dt.strftime("%Y-%m-%d")
        )
        .groupby(["particao", "data_publicacao_dia"], dropna=False)
        .size()
        .reset_index(name="n")
    )
    outside_summary.to_csv(
        OUT_DIR / "resumo_publicacoes_fora_janeiro.csv",
        index=False,
        encoding="utf-8-sig",
    )
    if len(outside):
        raise RuntimeError(
            f"Há {len(outside)} registros com data de publicação fora de janeiro de 2025."
        )

    min_pub = x["data_publicacao"].min()
    max_pub = x["data_publicacao"].max()

    out_path = DATA_DIR / "pncp_2025-01_publicacoes_municipal_pj.csv.gz"
    x.drop(columns=["particao"]).to_csv(
        out_path, index=False, compression="gzip", encoding="utf-8"
    )
    return x, out_path, min_pub, max_pub


def calculate_portfolio_metrics(df: pd.DataFrame):
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

    if rel.empty:
        return x, rel, pd.DataFrame(), pd.DataFrame()

    rel["share_valor"] = rel["valor_relacao"] / rel.groupby("orgao_cnpj")[
        "valor_relacao"
    ].transform("sum")
    rel["share_contagem"] = rel["n_instrumentos"] / rel.groupby("orgao_cnpj")[
        "n_instrumentos"
    ].transform("sum")

    rows = []
    for buyer, g in rel.groupby("orgao_cnpj", sort=False):
        sv = g["share_valor"].astype(float).sort_values(ascending=False)
        sc = g["share_contagem"].astype(float).sort_values(ascending=False)
        hv = float((sv**2).sum())
        hc = float((sc**2).sum())
        rows.append(
            {
                "orgao_cnpj": buyer,
                "valor_total_publicado_jan_assinado_2025": float(
                    g["valor_relacao"].sum()
                ),
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
            }
        )

    buyers = pd.DataFrame(rows)

    buyer_geo = (
        x.groupby("orgao_cnpj", dropna=False)
        .agg(
            n_municipios_unidade=("municipio_ibge", "nunique"),
            n_ufs_unidade=("uf", "nunique"),
        )
        .reset_index()
    )
    buyers = buyers.merge(buyer_geo, on="orgao_cnpj", how="left")

    ext = bool_series(x["origem_externa"])
    z = x.assign(valor_externo=np.where(ext, x["valorInicial"], 0.0))
    shared = (
        z.groupby("orgao_cnpj")
        .agg(
            valor_total_aux=("valorInicial", "sum"),
            valor_externo=("valor_externo", "sum"),
        )
        .reset_index()
    )
    shared["shared_procurement_share"] = (
        shared["valor_externo"] / shared["valor_total_aux"]
    )
    buyers = buyers.merge(
        shared[["orgao_cnpj", "shared_procurement_share"]],
        on="orgao_cnpj",
        how="left",
    )

    cat = (
        x.groupby(["orgao_cnpj", "categoria"], dropna=False)["valorInicial"]
        .sum()
        .rename("valor_categoria")
        .reset_index()
    )
    cat["share_categoria"] = cat["valor_categoria"] / cat.groupby("orgao_cnpj")[
        "valor_categoria"
    ].transform("sum")
    cat["hhi_piece"] = cat["share_categoria"] ** 2
    catmix = (
        cat.groupby("orgao_cnpj")
        .agg(
            category_mix_hhi=("hhi_piece", "sum"),
            n_categorias=("categoria", "nunique"),
            categoria_cr1=("share_categoria", "max"),
        )
        .reset_index()
    )
    buyers = buyers.merge(catmix, on="orgao_cnpj", how="left")

    suppliers = (
        rel.groupby("fornecedor_id_limpo")
        .agg(
            degree=("orgao_cnpj", "nunique"),
            strength=("valor_relacao", "sum"),
        )
        .reset_index()
    )
    nbuyers = max(int(rel["orgao_cnpj"].nunique()), 1)
    suppliers["reach"] = suppliers["degree"] / nbuyers
    suppliers["system_share"] = suppliers["strength"] / suppliers["strength"].sum()
    suppliers["pct_degree"] = suppliers["degree"].rank(
        pct=True, method="average"
    )
    suppliers["pct_strength"] = suppliers["strength"].rank(
        pct=True, method="average"
    )

    ez = rel.merge(
        suppliers[
            ["fornecedor_id_limpo", "pct_degree", "pct_strength"]
        ],
        on="fornecedor_id_limpo",
        how="left",
    )
    ez["ed_piece"] = ez["share_valor"] * ez["pct_degree"]
    ez["es_piece"] = ez["share_valor"] * ez["pct_strength"]
    exposure = (
        ez.groupby("orgao_cnpj")
        .agg(
            exposicao_degree=("ed_piece", "sum"),
            exposicao_strength=("es_piece", "sum"),
        )
        .reset_index()
    )
    buyers = buyers.merge(exposure, on="orgao_cnpj", how="left")

    return x, rel, buyers, suppliers


def safe_spearman(df: pd.DataFrame, a: str, b: str):
    z = df[[a, b]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(z) < 3 or z[a].nunique() < 2 or z[b].nunique() < 2:
        return float("nan"), float("nan")
    rho, pval = spearmanr(z[a], z[b])
    return float(rho), float(pval)


def metric_stats(buyers: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "portfolio_hhi",
        "count_hhi",
        "portfolio_cr1",
        "portfolio_cr4",
        "portfolio_neff",
        "count_neff",
        "hhi_gap_value_minus_count",
        "shared_procurement_share",
        "category_mix_hhi",
        "exposicao_degree",
        "exposicao_strength",
    ]
    rows = []
    for col in cols:
        if col not in buyers.columns:
            continue
        s = pd.to_numeric(buyers[col], errors="coerce").replace(
            [np.inf, -np.inf], np.nan
        ).dropna()
        if s.empty:
            continue
        rows.append(
            {
                "metrica": col,
                "n": int(s.size),
                "media": float(s.mean()),
                "desvio_padrao": float(s.std(ddof=1)) if s.size > 1 else None,
                "min": float(s.min()),
                "p25": float(s.quantile(0.25)),
                "mediana": float(s.median()),
                "p75": float(s.quantile(0.75)),
                "p90": float(s.quantile(0.90)),
                "p95": float(s.quantile(0.95)),
                "max": float(s.max()),
            }
        )
    return pd.DataFrame(rows)


def correlation_table(eligible: pd.DataFrame) -> pd.DataFrame:
    pairs = [
        ("portfolio_hhi", "count_hhi"),
        ("portfolio_hhi", "exposicao_degree"),
        ("portfolio_hhi", "exposicao_strength"),
        ("count_hhi", "exposicao_degree"),
        ("count_hhi", "exposicao_strength"),
        ("exposicao_degree", "exposicao_strength"),
    ]
    rows = []
    for a, b in pairs:
        if a not in eligible.columns or b not in eligible.columns:
            continue
        rho, pval = safe_spearman(eligible, a, b)
        rows.append(
            {
                "variavel_a": a,
                "variavel_b": b,
                "spearman_rho": None if pd.isna(rho) else rho,
                "p_value": None if pd.isna(pval) else pval,
                "n": int(eligible[[a, b]].dropna().shape[0]),
            }
        )
    return pd.DataFrame(rows)


def diagnostics(
    df: pd.DataFrame,
    buyers: pd.DataFrame,
    partition_summaries: list[dict],
    consolidated_path: Path,
    min_pub: pd.Timestamp,
    max_pub: pd.Timestamp,
):
    signed_counts = (
        df["ano_assinatura"]
        .value_counts(dropna=False)
        .sort_index()
        .rename_axis("ano_assinatura")
        .reset_index(name="n")
    )
    signed_counts.to_csv(
        OUT_DIR / "distribuicao_ano_assinatura.csv",
        index=False,
        encoding="utf-8-sig",
    )

    eligible = buyers[
        (buyers["n_fornecedores"] >= 3) & (buyers["n_instrumentos"] >= 5)
    ].copy()

    stats = metric_stats(eligible)
    stats.to_csv(
        OUT_DIR / "estatisticas_metricas_compradores_elegiveis.csv",
        index=False,
        encoding="utf-8-sig",
    )
    corr = correlation_table(eligible)
    corr.to_csv(
        OUT_DIR / "correlacoes_spearman_compradores_elegiveis.csv",
        index=False,
        encoding="utf-8-sig",
    )

    if len(eligible):
        qv = float(eligible["portfolio_hhi"].quantile(0.75))
        qc = float(eligible["count_hhi"].quantile(0.75))
        qe = float(eligible["exposicao_strength"].quantile(0.75))
        both_top = int(
            (
                (eligible["portfolio_hhi"] >= qv)
                & (eligible["count_hhi"] >= qc)
            ).sum()
        )
        hidden_network = int(
            (
                (eligible["portfolio_hhi"] < qv)
                & (eligible["exposicao_strength"] >= qe)
            ).sum()
        )
    else:
        qv = qc = qe = float("nan")
        both_top = hidden_network = 0

    rho_pc, p_pc = safe_spearman(eligible, "portfolio_hhi", "count_hhi")
    rho_pe, p_pe = safe_spearman(
        eligible, "portfolio_hhi", "exposicao_strength"
    )

    lag = pd.to_numeric(
        df["lag_publicacao_dias"], errors="coerce"
    ).dropna()

    summary = {
        "escopo": (
            "Publicações de 01/01/2025 a 31/01/2025, fornecedores PJ, "
            "esfera municipal, Poder Executivo."
        ),
        "advertencia": (
            "Métricas de carteira para contratos assinados em 2025 são "
            "diagnósticas e incompletas. Contratos assinados em 2025 podem "
            "ser publicados após janeiro."
        ),
        "janela_publicacao_validada": {
            "min": min_pub.isoformat() if pd.notna(min_pub) else None,
            "max": max_pub.isoformat() if pd.notna(max_pub) else None,
            "regra": "[2025-01-01, 2025-02-01)",
        },
        "registros_pj_consolidados": int(len(df)),
        "instrumentos_unicos": int(df["id_contrato"].nunique()),
        "duplicidades_id_contrato": int(df.duplicated("id_contrato").sum()),
        "compradores_unicos": int(df["orgao_cnpj"].nunique()),
        "fornecedores_pj_unicos": int(df["fornecedor_id_limpo"].nunique()),
        "municipios_unicos": int(df["municipio_ibge"].nunique()),
        "assinados_2025_publicados_janeiro": int(
            df["ano_assinatura"].eq(2025).sum()
        ),
        "assinados_antes_2025_publicados_janeiro": int(
            df["ano_assinatura"].lt(2025).sum()
        ),
        "lag_mediana_dias_pj": float(lag.median()) if len(lag) else None,
        "lag_p90_dias_pj": float(lag.quantile(0.90)) if len(lag) else None,
        "lag_p95_dias_pj": float(lag.quantile(0.95)) if len(lag) else None,
        "lag_negativo_n_pj": int((lag < 0).sum()),
        "compradores_metricas_assinados_2025": int(len(buyers)),
        "compradores_elegiveis_diag_n3_forn_n5_instr": int(len(eligible)),
        "spearman_portfolio_count_elegiveis": (
            None if pd.isna(rho_pc) else rho_pc
        ),
        "spearman_portfolio_count_pvalue": (
            None if pd.isna(p_pc) else p_pc
        ),
        "spearman_portfolio_exposicao_strength_elegiveis": (
            None if pd.isna(rho_pe) else rho_pe
        ),
        "spearman_portfolio_exposicao_strength_pvalue": (
            None if pd.isna(p_pe) else p_pe
        ),
        "portfolio_hhi_q75_elegiveis": None if pd.isna(qv) else qv,
        "count_hhi_q75_elegiveis": None if pd.isna(qc) else qc,
        "exposicao_strength_q75_elegiveis": None if pd.isna(qe) else qe,
        "compradores_top_quartil_ambas_medidas": both_top,
        "compradores_alta_exposicao_sem_hhi_q4": hidden_network,
        "registros_brutos_particoes_soma": int(
            sum(s["registros_brutos"] for s in partition_summaries)
        ),
        "registros_municipais_validos_todos_tipos_soma": int(
            sum(
                s["registros_municipais_validos"]
                for s in partition_summaries
            )
        ),
        "registros_pf_soma": int(
            sum(s["registros_pf"] for s in partition_summaries)
        ),
        "registros_pe_soma": int(
            sum(s["registros_pe"] for s in partition_summaries)
        ),
        "sha256_base_pj_consolidada": sha256(consolidated_path),
        "arquivo_base_pj_consolidada": str(
            consolidated_path.relative_to(ROOT)
        ),
    }
    (OUT_DIR / "resumo_diagnostico.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def main():
    df, manifest, partition_summaries = load_parts()
    manifest.to_csv(
        OUT_DIR / "manifesto_particoes.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df, consolidated_path, min_pub, max_pub = validate_and_consolidate(df)
    cohort, rel, buyers, suppliers = calculate_portfolio_metrics(df)

    rel.to_csv(
        OUT_DIR / "relacoes_assinados_2025_publicados_janeiro.csv.gz",
        index=False,
        compression="gzip",
    )
    buyers.to_csv(
        OUT_DIR / "metricas_compradores_assinados_2025_publicados_janeiro.csv",
        index=False,
        encoding="utf-8-sig",
    )
    suppliers.to_csv(
        OUT_DIR
        / "metricas_fornecedores_assinados_2025_publicados_janeiro.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary = diagnostics(
        df,
        buyers,
        partition_summaries,
        consolidated_path,
        min_pub,
        max_pub,
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
