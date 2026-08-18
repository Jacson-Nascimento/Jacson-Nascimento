#!/usr/bin/env python3
"""Estabilidade longitudinal dos sinais de risco entre jan-fev e jan-mar/2025.

Compara apenas compradores elegíveis em ambas as janelas. Mede persistência de
ranking, sobreposição dos quartis superiores e transições do quadrante de
'exposição estrutural oculta' (HHI abaixo do Q75 e exposição Strength >= Q75).
Resultados são condicionais às coortes de publicação e não representam o ano.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = RES / "estabilidade_sinais_risco_jan_mar_2025"
OUT.mkdir(parents=True, exist_ok=True)

P12 = RES / "carteira_jan_fev_2025_diagnostico" / "compradores_elegiveis_jan_fev.csv"
P123 = RES / "carteira_acumulada_2025_03_diagnostico" / "compradores_elegiveis.csv"


def add_norm(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    n = pd.to_numeric(x["n_fornecedores"], errors="coerce")
    h = pd.to_numeric(x["portfolio_hhi"], errors="coerce")
    hc = pd.to_numeric(x["count_hhi"], errors="coerce")
    floor = 1 / n
    denom = 1 - floor
    x["portfolio_hhi_norm"] = np.where(n > 1, (h - floor) / denom, np.nan)
    x["count_hhi_norm"] = np.where(n > 1, (hc - floor) / denom, np.nan)
    return x


def rho(a: pd.Series, b: pd.Series) -> dict:
    z = pd.DataFrame({"a": a, "b": b}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(z) < 3:
        return {"rho": None, "p": None, "n": int(len(z))}
    r, p = spearmanr(z["a"], z["b"])
    return {"rho": float(r), "p": float(p), "n": int(len(z))}


def jaccard(a: set[str], b: set[str]) -> float | None:
    u = a | b
    return None if not u else len(a & b) / len(u)


def classify(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    x = df.copy()
    qh = float(x["portfolio_hhi"].quantile(.75))
    qe = float(x["exposicao_strength"].quantile(.75))
    x["hhi_alto"] = x["portfolio_hhi"].ge(qh)
    x["exposicao_alta"] = x["exposicao_strength"].ge(qe)
    x["exposicao_oculta"] = (~x["hhi_alto"]) & x["exposicao_alta"]
    x["quadrante"] = np.select(
        [
            (~x["hhi_alto"]) & (~x["exposicao_alta"]),
            (~x["hhi_alto"]) & x["exposicao_alta"],
            x["hhi_alto"] & (~x["exposicao_alta"]),
            x["hhi_alto"] & x["exposicao_alta"],
        ],
        ["baixo_baixo", "oculta", "hhi_alto", "critico"],
        default="indefinido",
    )
    return x, {"q75_hhi": qh, "q75_exposicao_strength": qe}


def main() -> None:
    a = add_norm(pd.read_csv(P12, dtype={"orgao_cnpj": "string"}, low_memory=False))
    b = add_norm(pd.read_csv(P123, dtype={"orgao_cnpj": "string"}, low_memory=False))

    for d in [a, b]:
        for c in ["portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4", "count_hhi", "count_hhi_norm", "exposicao_strength", "exposicao_degree", "n_fornecedores", "n_instrumentos"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")

    common_ids = set(a["orgao_cnpj"].astype(str)) & set(b["orgao_cnpj"].astype(str))
    aa = a[a["orgao_cnpj"].astype(str).isin(common_ids)].copy()
    bb = b[b["orgao_cnpj"].astype(str).isin(common_ids)].copy()

    aa, cut_a = classify(aa)
    bb, cut_b = classify(bb)
    keep = [
        "orgao_cnpj", "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
        "count_hhi", "count_hhi_norm", "exposicao_strength", "exposicao_degree",
        "n_fornecedores", "n_instrumentos", "quadrante", "exposicao_oculta"
    ]
    m = aa[keep].merge(bb[keep], on="orgao_cnpj", suffixes=("_jan_fev", "_jan_mar"), validate="one_to_one")

    metrics = ["portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4", "count_hhi", "count_hhi_norm", "exposicao_strength", "exposicao_degree"]
    correlations = {
        k: rho(m[f"{k}_jan_fev"], m[f"{k}_jan_mar"])
        for k in metrics
    }

    # Top quartile membership, calculated within the common sample for each window.
    overlaps = {}
    for k in ["portfolio_hhi", "portfolio_hhi_norm", "exposicao_strength", "exposicao_degree"]:
        qa = float(m[f"{k}_jan_fev"].quantile(.75))
        qb = float(m[f"{k}_jan_mar"].quantile(.75))
        sa = set(m.loc[m[f"{k}_jan_fev"].ge(qa), "orgao_cnpj"].astype(str))
        sb = set(m.loc[m[f"{k}_jan_mar"].ge(qb), "orgao_cnpj"].astype(str))
        overlaps[k] = {
            "n_top_jan_fev": len(sa),
            "n_top_jan_mar": len(sb),
            "n_intersecao": len(sa & sb),
            "jaccard": jaccard(sa, sb),
            "retencao_jan_fev_pct": None if not sa else len(sa & sb) / len(sa) * 100,
        }

    hidden_a = set(m.loc[m["exposicao_oculta_jan_fev"], "orgao_cnpj"].astype(str))
    hidden_b = set(m.loc[m["exposicao_oculta_jan_mar"], "orgao_cnpj"].astype(str))
    hidden = {
        "n_jan_fev": len(hidden_a),
        "n_jan_mar": len(hidden_b),
        "n_persistentes": len(hidden_a & hidden_b),
        "jaccard": jaccard(hidden_a, hidden_b),
        "retencao_jan_fev_pct": None if not hidden_a else len(hidden_a & hidden_b) / len(hidden_a) * 100,
        "novos_em_jan_mar": len(hidden_b - hidden_a),
        "saidas_em_jan_mar": len(hidden_a - hidden_b),
    }

    transition = pd.crosstab(
        m["quadrante_jan_fev"],
        m["quadrante_jan_mar"],
        margins=True,
        dropna=False,
    )
    transition.to_csv(OUT / "matriz_transicao_quadrantes.csv", encoding="utf-8-sig")

    m["delta_hhi"] = m["portfolio_hhi_jan_mar"] - m["portfolio_hhi_jan_fev"]
    m["delta_hhi_norm"] = m["portfolio_hhi_norm_jan_mar"] - m["portfolio_hhi_norm_jan_fev"]
    m["delta_exposicao_strength"] = m["exposicao_strength_jan_mar"] - m["exposicao_strength_jan_fev"]
    m["quadrante_estavel"] = m["quadrante_jan_fev"].eq(m["quadrante_jan_mar"])
    m.to_csv(OUT / "comparacao_compradores_comuns.csv", index=False, encoding="utf-8-sig")

    summary = {
        "elegiveis_jan_fev": int(len(a)),
        "elegiveis_jan_mar": int(len(b)),
        "compradores_comuns": int(len(m)),
        "retencao_elegiveis_jan_fev_pct": float(len(m) / max(len(a), 1) * 100),
        "cortes_common_sample": {"jan_fev": cut_a, "jan_mar": cut_b},
        "spearman_estabilidade": correlations,
        "sobreposicao_top_quartil": overlaps,
        "exposicao_oculta": hidden,
        "quadrante_estavel_pct": float(m["quadrante_estavel"].mean() * 100),
        "delta_hhi_mediana": float(m["delta_hhi"].median()),
        "delta_hhi_norm_mediana": float(m["delta_hhi_norm"].median()),
        "delta_exposicao_strength_mediana": float(m["delta_exposicao_strength"].median()),
        "nota": "Comparação condicionada aos compradores elegíveis em ambas as janelas. Não mede estabilidade anual nem corrige mudança de cobertura do PNCP.",
    }
    (OUT / "resumo_estabilidade_risco.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
