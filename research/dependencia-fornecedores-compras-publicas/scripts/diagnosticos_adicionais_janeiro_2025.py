#!/usr/bin/env python3
"""Diagnósticos adicionais para a coorte parcial PNCP de janeiro de 2025.

Não produz inferência anual. Usa apenas compradores institucionais com contratos
assinados em 2025 já publicados em janeiro, e mantém o comprador definido por
CNPJ do órgão.

Saídas:
- quadrantes HHI monetário x exposição à força sistêmica;
- divergência concentração por valor x por frequência;
- controle dos lags negativos;
- concentração/alcance da rede de fornecedores;
- simulações de remoção direcionada versus aleatória.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "results" / "carteira_janeiro_2025_diagnostico"
DATA_DIR = ROOT / "data" / "processed" / "pncp_mensal"
OUT = ROOT / "results" / "diagnosticos_adicionais_janeiro_2025"
OUT.mkdir(parents=True, exist_ok=True)

BUYERS_FILE = BASE_DIR / "metricas_compradores_assinados_2025_publicados_janeiro.csv"
SUPPLIERS_FILE = BASE_DIR / "metricas_fornecedores_assinados_2025_publicados_janeiro.csv"
REL_FILE = BASE_DIR / "relacoes_assinados_2025_publicados_janeiro.csv.gz"
CONSOLIDATED_FILE = DATA_DIR / "pncp_2025-01_publicacoes_municipal_pj.csv.gz"

RANDOM_DRAWS = 1000
SEED = 20260818
REMOVAL_PCTS = [0.01, 0.05, 0.10]
SEVERE_THRESHOLDS = [0.25, 0.50, 0.75]


def read_inputs():
    buyers = pd.read_csv(BUYERS_FILE, dtype={"orgao_cnpj": "string"})
    suppliers = pd.read_csv(
        SUPPLIERS_FILE, dtype={"fornecedor_id_limpo": "string"}
    )
    rel = pd.read_csv(
        REL_FILE,
        dtype={"orgao_cnpj": "string", "fornecedor_id_limpo": "string"},
    )
    base = pd.read_csv(
        CONSOLIDATED_FILE,
        dtype={
            "id_contrato": "string",
            "id_compra": "string",
            "orgao_cnpj": "string",
            "municipio_ibge": "string",
        },
        low_memory=False,
    )
    return buyers, suppliers, rel, base


def eligible_buyers(buyers: pd.DataFrame) -> pd.DataFrame:
    return buyers[
        (pd.to_numeric(buyers["n_fornecedores"], errors="coerce") >= 3)
        & (pd.to_numeric(buyers["n_instrumentos"], errors="coerce") >= 5)
    ].copy()


def quadrant_analysis(eligible: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    q_hhi = float(eligible["portfolio_hhi"].quantile(0.75))
    q_exp = float(eligible["exposicao_strength"].quantile(0.75))
    z = eligible[["orgao_cnpj", "portfolio_hhi", "exposicao_strength"]].copy()
    z["hhi_alto_q4"] = z["portfolio_hhi"] >= q_hhi
    z["exposicao_alta_q4"] = z["exposicao_strength"] >= q_exp

    z["quadrante"] = np.select(
        [
            (~z["hhi_alto_q4"]) & (~z["exposicao_alta_q4"]),
            z["hhi_alto_q4"] & (~z["exposicao_alta_q4"]),
            (~z["hhi_alto_q4"]) & z["exposicao_alta_q4"],
            z["hhi_alto_q4"] & z["exposicao_alta_q4"],
        ],
        [
            "HHI baixo / exposição baixa",
            "HHI alto / exposição baixa",
            "HHI baixo / exposição alta",
            "HHI alto / exposição alta",
        ],
        default="não classificado",
    )
    counts = (
        z["quadrante"]
        .value_counts()
        .rename_axis("quadrante")
        .reset_index(name="n")
    )
    counts["pct"] = counts["n"] / len(z) * 100
    counts.to_csv(OUT / "quadrantes_hhi_exposicao.csv", index=False, encoding="utf-8-sig")
    z.to_csv(
        OUT / "classificacao_compradores_quadrantes.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary = {
        "q75_portfolio_hhi": q_hhi,
        "q75_exposicao_strength": q_exp,
        "n_elegiveis": int(len(z)),
        "hhi_baixo_exposicao_alta_n": int(
            ((~z["hhi_alto_q4"]) & z["exposicao_alta_q4"]).sum()
        ),
        "hhi_alto_exposicao_alta_n": int(
            (z["hhi_alto_q4"] & z["exposicao_alta_q4"]).sum()
        ),
    }
    return z, summary


def divergence_analysis(eligible: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    z = eligible[
        [
            "orgao_cnpj",
            "portfolio_hhi",
            "count_hhi",
            "portfolio_neff",
            "count_neff",
            "portfolio_cr1",
            "portfolio_cr4",
        ]
    ].copy()
    diff = z["portfolio_hhi"] - z["count_hhi"]
    close = np.isclose(diff, 0.0, rtol=0.0, atol=1e-12)
    z["relacao_hhi"] = np.select(
        [diff > 1e-12, diff < -1e-12, close],
        [
            "HHI monetário > HHI frequência",
            "HHI monetário < HHI frequência",
            "HHI monetário = HHI frequência",
        ],
        default="indefinido",
    )
    z["razao_neff_valor_frequencia"] = (
        z["portfolio_neff"] / z["count_neff"]
    )
    counts = (
        z["relacao_hhi"]
        .value_counts(dropna=False)
        .rename_axis("relacao_hhi")
        .reset_index(name="n")
    )
    counts["pct"] = counts["n"] / len(z) * 100
    counts.to_csv(
        OUT / "divergencia_hhi_valor_frequencia.csv",
        index=False,
        encoding="utf-8-sig",
    )
    z.to_csv(
        OUT / "comparacao_hhi_por_comprador.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary = {
        "portfolio_hhi_maior_count_hhi_n": int((diff > 1e-12).sum()),
        "portfolio_hhi_maior_count_hhi_pct": float((diff > 1e-12).mean() * 100),
        "portfolio_hhi_menor_count_hhi_n": int((diff < -1e-12).sum()),
        "portfolio_hhi_igual_count_hhi_n": int(close.sum()),
        "mediana_gap_hhi": float(diff.median()),
        "mediana_razao_neff_valor_frequencia": float(
            z["razao_neff_valor_frequencia"].median()
        ),
    }
    return z, summary


def lag_diagnostics(base: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    z = base.copy()
    z["lag_publicacao_dias"] = pd.to_numeric(
        z["lag_publicacao_dias"], errors="coerce"
    )
    neg = z[z["lag_publicacao_dias"] < 0].copy()
    keep = [
        "id_contrato",
        "id_compra",
        "orgao_cnpj",
        "municipio_ibge",
        "municipio",
        "uf",
        "categoria",
        "tipo_contrato",
        "data_assinatura",
        "data_publicacao",
        "lag_publicacao_dias",
    ]
    keep = [c for c in keep if c in neg.columns]
    neg[keep].to_csv(
        OUT / "lags_negativos_instrumentos_pj.csv",
        index=False,
        encoding="utf-8-sig",
    )
    dist = (
        neg["lag_publicacao_dias"]
        .value_counts()
        .sort_index()
        .rename_axis("lag_publicacao_dias")
        .reset_index(name="n")
    )
    dist.to_csv(
        OUT / "lags_negativos_distribuicao.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary = {
        "lags_negativos_n": int(len(neg)),
        "lag_negativo_min": float(neg["lag_publicacao_dias"].min())
        if len(neg)
        else None,
        "lag_negativo_max": float(neg["lag_publicacao_dias"].max())
        if len(neg)
        else None,
    }
    return neg, summary


def structural_diagnostics(
    buyers: pd.DataFrame, eligible: pd.DataFrame, rel: pd.DataFrame, suppliers: pd.DataFrame
) -> dict:
    all_multi = pd.to_numeric(
        buyers.get("n_municipios_unidade"), errors="coerce"
    ).fillna(0) > 1
    elig_multi = pd.to_numeric(
        eligible.get("n_municipios_unidade"), errors="coerce"
    ).fillna(0) > 1
    one_category = pd.to_numeric(
        eligible.get("n_categorias"), errors="coerce"
    ).fillna(0) == 1

    rel_e = rel[rel["orgao_cnpj"].isin(set(eligible["orgao_cnpj"]))].copy()
    supplier_ids = rel_e["fornecedor_id_limpo"].dropna().unique().tolist()
    _ = suppliers[suppliers["fornecedor_id_limpo"].isin(supplier_ids)].copy()

    strength_elig = (
        rel_e.groupby("fornecedor_id_limpo")["valor_relacao"]
        .sum()
        .sort_values(ascending=False)
    )
    total_strength = float(strength_elig.sum())

    def top_share(s: pd.Series, pct: float) -> float:
        if s.empty or s.sum() <= 0:
            return float("nan")
        k = max(1, math.ceil(len(s) * pct))
        return float(s.iloc[:k].sum() / s.sum())

    degree_elig = (
        rel_e.groupby("fornecedor_id_limpo")["orgao_cnpj"]
        .nunique()
        .sort_values(ascending=False)
    )
    n_edges = max(len(rel_e), 1)

    def edge_coverage_top_degree(pct: float) -> float:
        if degree_elig.empty:
            return float("nan")
        k = max(1, math.ceil(len(degree_elig) * pct))
        top = set(degree_elig.iloc[:k].index)
        return float(rel_e["fornecedor_id_limpo"].isin(top).sum() / n_edges)

    summary = {
        "compradores_total_metricas": int(len(buyers)),
        "compradores_multi_municipio_total_n": int(all_multi.sum()),
        "compradores_multi_municipio_total_pct": float(all_multi.mean() * 100)
        if len(buyers)
        else None,
        "compradores_elegiveis": int(len(eligible)),
        "compradores_multi_municipio_elegiveis_n": int(elig_multi.sum()),
        "compradores_multi_municipio_elegiveis_pct": float(elig_multi.mean() * 100)
        if len(eligible)
        else None,
        "compradores_elegiveis_uma_categoria_n": int(one_category.sum()),
        "compradores_elegiveis_uma_categoria_pct": float(one_category.mean() * 100)
        if len(eligible)
        else None,
        "fornecedores_rede_elegivel": int(len(strength_elig)),
        "relacoes_comprador_fornecedor_rede_elegivel": int(len(rel_e)),
        "top_1pct_fornecedores_strength_share": top_share(strength_elig, 0.01),
        "top_5pct_fornecedores_strength_share": top_share(strength_elig, 0.05),
        "top_10pct_fornecedores_strength_share": top_share(strength_elig, 0.10),
        "top_1pct_degree_edge_coverage": edge_coverage_top_degree(0.01),
        "top_5pct_degree_edge_coverage": edge_coverage_top_degree(0.05),
        "top_10pct_degree_edge_coverage": edge_coverage_top_degree(0.10),
        "degree_mediana_rede_elegivel": float(degree_elig.median())
        if len(degree_elig)
        else None,
        "degree_p95_rede_elegivel": float(degree_elig.quantile(0.95))
        if len(degree_elig)
        else None,
        "degree_max_rede_elegivel": int(degree_elig.max())
        if len(degree_elig)
        else None,
        "valor_total_relacoes_rede_elegivel": total_strength,
    }
    pd.DataFrame(
        [
            {
                "metrica": k,
                "valor": v,
            }
            for k, v in summary.items()
        ]
    ).to_csv(
        OUT / "diagnosticos_estruturais.csv",
        index=False,
        encoding="utf-8-sig",
    )
    return summary


def simulate_removals(
    eligible: pd.DataFrame, rel: pd.DataFrame, suppliers: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:
    buyers_order = eligible["orgao_cnpj"].astype("string").tolist()
    rel_e = rel[rel["orgao_cnpj"].isin(set(buyers_order))].copy()

    matrix = rel_e.pivot_table(
        index="orgao_cnpj",
        columns="fornecedor_id_limpo",
        values="share_valor",
        aggfunc="sum",
        fill_value=0.0,
    )
    matrix = matrix.reindex(buyers_order, fill_value=0.0)
    candidate_ids = matrix.columns.astype("string").tolist()
    n_sup = len(candidate_ids)
    if n_sup == 0:
        return pd.DataFrame(), {"fornecedores_candidatos_simulacao": 0}

    sup = suppliers.set_index("fornecedor_id_limpo").reindex(candidate_ids)
    rng = np.random.default_rng(SEED)
    A = matrix.to_numpy(dtype=float)

    rows = []
    random_cache = {}

    for pct in REMOVAL_PCTS:
        k = max(1, math.ceil(n_sup * pct))

        random_severe = {tau: [] for tau in SEVERE_THRESHOLDS}
        random_mean_loss = []
        for _ in range(RANDOM_DRAWS):
            idx = rng.choice(n_sup, size=k, replace=False)
            losses = A[:, idx].sum(axis=1)
            random_mean_loss.append(float(losses.mean()))
            for tau in SEVERE_THRESHOLDS:
                random_severe[tau].append(float((losses >= tau).mean()))
        random_cache[pct] = {
            "mean_loss": np.asarray(random_mean_loss),
            "severe": {
                tau: np.asarray(vals) for tau, vals in random_severe.items()
            },
        }

        for metric in ["degree", "strength"]:
            ranking = (
                pd.to_numeric(sup[metric], errors="coerce")
                .fillna(-np.inf)
                .sort_values(ascending=False)
            )
            removed_ids = ranking.iloc[:k].index.tolist()
            idx_map = {sid: i for i, sid in enumerate(candidate_ids)}
            idx = [idx_map[sid] for sid in removed_ids]
            losses_target = A[:, idx].sum(axis=1)

            rand_loss = random_cache[pct]["mean_loss"]
            for tau in SEVERE_THRESHOLDS:
                rand = random_cache[pct]["severe"][tau]
                severe_target = float((losses_target >= tau).mean())
                rows.append(
                    {
                        "estrategia_direcionada": metric,
                        "pct_fornecedores_removidos": pct,
                        "k_fornecedores_removidos": k,
                        "limiar_perda": tau,
                        "share_compradores_severos_direcionado": severe_target,
                        "share_compradores_severos_aleatorio_media": float(rand.mean()),
                        "share_compradores_severos_aleatorio_p025": float(
                            np.quantile(rand, 0.025)
                        ),
                        "share_compradores_severos_aleatorio_p975": float(
                            np.quantile(rand, 0.975)
                        ),
                        "excesso_vulnerabilidade": severe_target
                        - float(rand.mean()),
                        "perda_media_direcionada": float(losses_target.mean()),
                        "perda_media_aleatoria_media": float(rand_loss.mean()),
                        "perda_media_aleatoria_p025": float(
                            np.quantile(rand_loss, 0.025)
                        ),
                        "perda_media_aleatoria_p975": float(
                            np.quantile(rand_loss, 0.975)
                        ),
                    }
                )

    out = pd.DataFrame(rows)
    out.to_csv(
        OUT / "simulacoes_remocao_fornecedores.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary = {
        "random_draws": RANDOM_DRAWS,
        "seed": SEED,
        "fornecedores_candidatos_simulacao": int(n_sup),
        "compradores_elegiveis_simulacao": int(len(buyers_order)),
    }
    return out, summary


def summarize_key_simulations(sim: pd.DataFrame) -> list[dict]:
    if sim.empty:
        return []
    z = sim[sim["limiar_perda"].eq(0.50)].copy()
    cols = [
        "estrategia_direcionada",
        "pct_fornecedores_removidos",
        "k_fornecedores_removidos",
        "share_compradores_severos_direcionado",
        "share_compradores_severos_aleatorio_media",
        "excesso_vulnerabilidade",
        "perda_media_direcionada",
        "perda_media_aleatoria_media",
    ]
    return z[cols].to_dict(orient="records")


def main():
    buyers, suppliers, rel, base = read_inputs()
    eligible = eligible_buyers(buyers)

    _, quad = quadrant_analysis(eligible)
    _, div = divergence_analysis(eligible)
    _, lag = lag_diagnostics(base)
    structural = structural_diagnostics(buyers, eligible, rel, suppliers)
    sim, sim_meta = simulate_removals(eligible, rel, suppliers)

    summary = {
        "escopo": (
            "Diagnóstico da coorte parcial: contratos assinados em 2025 e publicados "
            "em janeiro de 2025; fornecedores PJ; comprador institucional por CNPJ."
        ),
        "advertencia": (
            "Não interpretar como resultado anual. A rede e os HHI são parciais e "
            "serão recalculados após a coleta completa de 2025."
        ),
        "quadrantes": quad,
        "divergencia_valor_frequencia": div,
        "qualidade_lag": lag,
        "estrutura": structural,
        "simulacao": sim_meta,
        "simulacoes_limiar_50pct": summarize_key_simulations(sim),
    }
    (OUT / "resumo_diagnosticos_adicionais.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
