#!/usr/bin/env python3
"""Diagnósticos longitudinais genéricos entre duas janelas acumuladas de 2025.

Reproduz, sem alterar definições, os diagnósticos já validados:
- estabilidade de rankings e métricas;
- retenção no quartil superior;
- persistência da exposição estrutural oculta;
- transição de quadrantes;
- efeito de composição entre compradores comuns e novos elegíveis.

Uso:
  python scripts/diagnosticos_longitudinais_generico.py --from-month 5 --to-month 6

As conclusões são descritivas e condicionadas à cobertura acumulada do PNCP.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
METRICS = [
    "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
    "count_hhi", "count_hhi_norm", "n_fornecedores", "n_instrumentos",
    "exposicao_strength_global", "exposicao_degree_global"
]
CORR_METRICS = [
    "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
    "count_hhi", "count_hhi_norm", "exposicao_strength_global", "exposicao_degree_global"
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--from-month", type=int, required=True, choices=range(1, 13))
    p.add_argument("--to-month", type=int, required=True, choices=range(1, 13))
    return p.parse_args()


def rho(a: pd.Series, b: pd.Series) -> dict:
    z = pd.DataFrame({"a": a, "b": b}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(z) < 3:
        return {"rho": None, "p": None, "n": int(len(z))}
    r, p = spearmanr(z["a"], z["b"])
    return {"rho": float(r), "p": float(p), "n": int(len(z))}


def jaccard(a: set[str], b: set[str]) -> float | None:
    u = a | b
    return None if not u else len(a & b) / len(u)


def med(d: pd.DataFrame, c: str):
    x = pd.to_numeric(d[c], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return None if x.empty else float(x.median())


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


def summarize(d: pd.DataFrame, group: str) -> dict:
    out = {"grupo": group, "n": int(len(d))}
    for c in METRICS:
        if c in d.columns:
            out[f"{c}_mediana"] = med(d, c)
    return out


def main():
    args = parse_args()
    fm, tm = args.from_month, args.to_month
    if tm <= fm:
        raise ValueError("--to-month deve ser maior que --from-month")

    pin = lambda m: RES / f"carteira_acumulada_2025_{m:02d}_global" / "compradores_elegiveis_3_5.csv"
    p_from, p_to = pin(fm), pin(tm)
    if not p_from.exists() or not p_to.exists():
        raise FileNotFoundError(f"Arquivos ausentes: {p_from} / {p_to}")

    out = RES / f"diagnosticos_longitudinais_2025_{fm:02d}_{tm:02d}"
    out.mkdir(parents=True, exist_ok=True)

    a = pd.read_csv(p_from, dtype={"orgao_cnpj": "string"}, low_memory=False)
    b = pd.read_csv(p_to, dtype={"orgao_cnpj": "string"}, low_memory=False)
    for d in (a, b):
        for c in METRICS:
            if c in d.columns:
                d[c] = pd.to_numeric(d[c], errors="coerce")

    ids_a = set(a.orgao_cnpj.dropna().astype(str))
    ids_b = set(b.orgao_cnpj.dropna().astype(str))
    common = ids_a & ids_b
    entrants = ids_b - ids_a
    exits = ids_a - ids_b

    aa = a[a.orgao_cnpj.astype(str).isin(common)].copy()
    bb = b[b.orgao_cnpj.astype(str).isin(common)].copy()
    b_new = b[b.orgao_cnpj.astype(str).isin(entrants)].copy()

    aa, cut_a = classify(aa)
    bb, cut_b = classify(bb)
    keep = ["orgao_cnpj"] + METRICS + ["quadrante", "exposicao_oculta"]
    m = aa[keep].merge(bb[keep], on="orgao_cnpj", suffixes=("_from", "_to"), validate="one_to_one")

    correlations = {k: rho(m[f"{k}_from"], m[f"{k}_to"]) for k in CORR_METRICS}
    overlaps = {}
    for k in ["portfolio_hhi", "portfolio_hhi_norm", "exposicao_strength_global", "exposicao_degree_global"]:
        qa = float(m[f"{k}_from"].quantile(.75)); qb = float(m[f"{k}_to"].quantile(.75))
        sa = set(m.loc[m[f"{k}_from"].ge(qa), "orgao_cnpj"].astype(str))
        sb = set(m.loc[m[f"{k}_to"].ge(qb), "orgao_cnpj"].astype(str))
        overlaps[k] = {
            "n_top_from": len(sa), "n_top_to": len(sb), "n_intersecao": len(sa & sb),
            "jaccard": jaccard(sa, sb),
            "retencao_from_pct": None if not sa else len(sa & sb) / len(sa) * 100,
        }

    hidden_a = set(m.loc[m["exposicao_oculta_from"], "orgao_cnpj"].astype(str))
    hidden_b = set(m.loc[m["exposicao_oculta_to"], "orgao_cnpj"].astype(str))
    hidden = {
        "n_from": len(hidden_a), "n_to": len(hidden_b), "n_persistentes": len(hidden_a & hidden_b),
        "jaccard": jaccard(hidden_a, hidden_b),
        "retencao_from_pct": None if not hidden_a else len(hidden_a & hidden_b) / len(hidden_a) * 100,
        "novos_to": len(hidden_b - hidden_a), "saidas_to": len(hidden_a - hidden_b),
    }

    transition = pd.crosstab(m["quadrante_from"], m["quadrante_to"], margins=True, dropna=False)
    transition.to_csv(out / "matriz_transicao_quadrantes.csv", encoding="utf-8-sig")

    for c in METRICS:
        m[f"delta_{c}"] = m[f"{c}_to"] - m[f"{c}_from"]
    m["quadrante_estavel"] = m["quadrante_from"].eq(m["quadrante_to"])
    m.to_csv(out / "comparacao_compradores_comuns.csv", index=False, encoding="utf-8-sig")

    groups = [
        summarize(a, "todos_from"), summarize(b, "todos_to"),
        summarize(aa, "comuns_from"), summarize(bb, "comuns_to"),
        summarize(b_new, "novos_elegiveis_to"),
    ]
    pd.DataFrame(groups).to_csv(out / "estatisticas_grupos.csv", index=False, encoding="utf-8-sig")

    delta_common = {c: med(m, f"delta_{c}") for c in METRICS}
    entrant_gap = {}
    for c in METRICS:
        entrant_gap[c] = None if b_new.empty else med(b_new, c) - med(bb, c)

    summary = {
        "from_month": fm, "to_month": tm,
        "elegiveis_from": int(len(a)), "elegiveis_to": int(len(b)), "compradores_comuns": int(len(m)),
        "retencao_elegiveis_from_pct": float(len(m) / max(len(a), 1) * 100),
        "novos_elegiveis_to": int(len(entrants)), "saidas_da_elegibilidade": int(len(exits)),
        "crescimento_elegiveis_pct": float((len(b) / len(a) - 1) * 100),
        "cortes_common_sample": {"from": cut_a, "to": cut_b},
        "spearman_estabilidade": correlations,
        "sobreposicao_top_quartil": overlaps,
        "exposicao_oculta": hidden,
        "quadrante_estavel_pct": float(m["quadrante_estavel"].mean() * 100),
        "delta_mediano_dentro_comuns": delta_common,
        "hhi_agregado_mediana_from": med(a, "portfolio_hhi"),
        "hhi_agregado_mediana_to": med(b, "portfolio_hhi"),
        "hhi_comuns_mediana_from": med(aa, "portfolio_hhi"),
        "hhi_comuns_mediana_to": med(bb, "portfolio_hhi"),
        "hhi_novos_mediana_to": med(b_new, "portfolio_hhi"),
        "hhi_norm_novos_mediana_to": med(b_new, "portfolio_hhi_norm"),
        "n_fornecedores_novos_mediana_to": med(b_new, "n_fornecedores"),
        "n_instrumentos_novos_mediana_to": med(b_new, "n_instrumentos"),
        "gap_mediana_novos_vs_comuns_to": entrant_gap,
        "nota": "Diagnóstico condicionado aos compradores elegíveis e à mesma especificação global; não mede estabilidade anual nem corrige cobertura do PNCP."
    }
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
