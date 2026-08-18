#!/usr/bin/env python3
"""Estabilidade longitudinal dos sinais de risco entre jan-abr e jan-mai/2025.

Compara somente compradores elegíveis em ambas as janelas, usando a mesma
especificação global: HHI bruto/normalizado, exposição por Strength/Degree
globais, quartis e quadrantes. Resultados são condicionais à coorte de
publicações acumuladas e não representam o ano completo.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = RES / "estabilidade_sinais_risco_abr_mai_2025"
OUT.mkdir(parents=True, exist_ok=True)

P4 = RES / "carteira_acumulada_2025_04_global" / "compradores_elegiveis_3_5.csv"
P5 = RES / "carteira_acumulada_2025_05_global" / "compradores_elegiveis_3_5.csv"


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
    qe = float(x["exposicao_strength_global"].quantile(.75))
    x["hhi_alto"] = x["portfolio_hhi"].ge(qh)
    x["exposicao_alta"] = x["exposicao_strength_global"].ge(qe)
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
    return x, {"q75_hhi": qh, "q75_exposicao_strength_global": qe}


def main() -> None:
    a = pd.read_csv(P4, dtype={"orgao_cnpj": "string"}, low_memory=False)
    b = pd.read_csv(P5, dtype={"orgao_cnpj": "string"}, low_memory=False)
    metrics = [
        "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
        "count_hhi", "count_hhi_norm", "exposicao_strength_global",
        "exposicao_degree_global", "n_fornecedores", "n_instrumentos"
    ]
    for d in [a, b]:
        for c in metrics:
            d[c] = pd.to_numeric(d[c], errors="coerce")

    common_ids = set(a["orgao_cnpj"].astype(str)) & set(b["orgao_cnpj"].astype(str))
    aa = a[a["orgao_cnpj"].astype(str).isin(common_ids)].copy()
    bb = b[b["orgao_cnpj"].astype(str).isin(common_ids)].copy()
    aa, cut_a = classify(aa)
    bb, cut_b = classify(bb)

    keep = ["orgao_cnpj"] + metrics + ["quadrante", "exposicao_oculta"]
    m = aa[keep].merge(bb[keep], on="orgao_cnpj", suffixes=("_abr", "_mai"), validate="one_to_one")

    corr_metrics = [
        "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
        "count_hhi", "count_hhi_norm", "exposicao_strength_global", "exposicao_degree_global"
    ]
    correlations = {k: rho(m[f"{k}_abr"], m[f"{k}_mai"]) for k in corr_metrics}

    overlaps = {}
    for k in ["portfolio_hhi", "portfolio_hhi_norm", "exposicao_strength_global", "exposicao_degree_global"]:
        qa = float(m[f"{k}_abr"].quantile(.75)); qb = float(m[f"{k}_mai"].quantile(.75))
        sa = set(m.loc[m[f"{k}_abr"].ge(qa), "orgao_cnpj"].astype(str))
        sb = set(m.loc[m[f"{k}_mai"].ge(qb), "orgao_cnpj"].astype(str))
        overlaps[k] = {
            "n_top_abr": len(sa), "n_top_mai": len(sb), "n_intersecao": len(sa & sb),
            "jaccard": jaccard(sa, sb),
            "retencao_abr_pct": None if not sa else len(sa & sb) / len(sa) * 100,
        }

    hidden_a = set(m.loc[m["exposicao_oculta_abr"], "orgao_cnpj"].astype(str))
    hidden_b = set(m.loc[m["exposicao_oculta_mai"], "orgao_cnpj"].astype(str))
    hidden = {
        "n_abr": len(hidden_a), "n_mai": len(hidden_b), "n_persistentes": len(hidden_a & hidden_b),
        "jaccard": jaccard(hidden_a, hidden_b),
        "retencao_abr_pct": None if not hidden_a else len(hidden_a & hidden_b) / len(hidden_a) * 100,
        "novos_em_mai": len(hidden_b - hidden_a), "saidas_em_mai": len(hidden_a - hidden_b),
    }

    transition = pd.crosstab(m["quadrante_abr"], m["quadrante_mai"], margins=True, dropna=False)
    transition.to_csv(OUT / "matriz_transicao_quadrantes.csv", encoding="utf-8-sig")

    m["delta_hhi"] = m["portfolio_hhi_mai"] - m["portfolio_hhi_abr"]
    m["delta_hhi_norm"] = m["portfolio_hhi_norm_mai"] - m["portfolio_hhi_norm_abr"]
    m["delta_exposicao_strength"] = m["exposicao_strength_global_mai"] - m["exposicao_strength_global_abr"]
    m["quadrante_estavel"] = m["quadrante_abr"].eq(m["quadrante_mai"])
    m.to_csv(OUT / "comparacao_compradores_comuns.csv", index=False, encoding="utf-8-sig")

    summary = {
        "elegiveis_abr": int(len(a)), "elegiveis_mai": int(len(b)), "compradores_comuns": int(len(m)),
        "retencao_elegiveis_abr_pct": float(len(m) / max(len(a), 1) * 100),
        "cortes_common_sample": {"abr": cut_a, "mai": cut_b},
        "spearman_estabilidade": correlations, "sobreposicao_top_quartil": overlaps,
        "exposicao_oculta": hidden,
        "quadrante_estavel_pct": float(m["quadrante_estavel"].mean() * 100),
        "delta_hhi_mediana": float(m["delta_hhi"].median()),
        "delta_hhi_norm_mediana": float(m["delta_hhi_norm"].median()),
        "delta_exposicao_strength_mediana": float(m["delta_exposicao_strength"].median()),
        "nota": "Comparação condicionada aos compradores elegíveis em ambas as janelas e à mesma especificação global. Não mede estabilidade anual nem corrige mudança de cobertura do PNCP."
    }
    (OUT / "resumo_estabilidade_risco.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
