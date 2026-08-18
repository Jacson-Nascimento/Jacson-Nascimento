#!/usr/bin/env python3
"""Diagnostica efeito de composição dos compradores elegíveis março→abril/2025.

Separa compradores comuns e novos elegíveis em abril para explicar a diferença
entre mudança longitudinal dentro dos compradores e mudança da mediana agregada.
Não há interpretação causal.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = RES / "composicao_elegiveis_mar_abr_2025"
OUT.mkdir(parents=True, exist_ok=True)

P3 = RES / "carteira_acumulada_2025_03_global" / "compradores_elegiveis_3_5.csv"
P4 = RES / "carteira_acumulada_2025_04_global" / "compradores_elegiveis_3_5.csv"
METRICS = [
    "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
    "count_hhi", "count_hhi_norm", "n_fornecedores", "n_instrumentos",
    "exposicao_strength_global", "exposicao_degree_global"
]


def med(d: pd.DataFrame, c: str):
    x = pd.to_numeric(d[c], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return None if x.empty else float(x.median())


def summarize(d: pd.DataFrame, group: str) -> dict:
    out = {"grupo": group, "n": int(len(d))}
    for c in METRICS:
        if c in d.columns:
            out[f"{c}_mediana"] = med(d, c)
    return out


def main() -> None:
    a = pd.read_csv(P3, dtype={"orgao_cnpj": "string"}, low_memory=False)
    b = pd.read_csv(P4, dtype={"orgao_cnpj": "string"}, low_memory=False)
    for d in [a, b]:
        for c in METRICS:
            if c in d.columns:
                d[c] = pd.to_numeric(d[c], errors="coerce")

    ids_a = set(a.orgao_cnpj.dropna().astype(str))
    ids_b = set(b.orgao_cnpj.dropna().astype(str))
    common = ids_a & ids_b
    entrants = ids_b - ids_a
    exits = ids_a - ids_b

    a_common = a[a.orgao_cnpj.astype(str).isin(common)].copy()
    b_common = b[b.orgao_cnpj.astype(str).isin(common)].copy()
    b_new = b[b.orgao_cnpj.astype(str).isin(entrants)].copy()

    comp = a_common[["orgao_cnpj"] + METRICS].merge(
        b_common[["orgao_cnpj"] + METRICS], on="orgao_cnpj", suffixes=("_mar", "_abr"), validate="one_to_one"
    )
    for c in METRICS:
        comp[f"delta_{c}"] = comp[f"{c}_abr"] - comp[f"{c}_mar"]
    comp.to_csv(OUT / "mudancas_compradores_comuns.csv", index=False, encoding="utf-8-sig")

    groups = [
        summarize(a, "todos_mar"),
        summarize(b, "todos_abr"),
        summarize(a_common, "comuns_mar"),
        summarize(b_common, "comuns_abr"),
        summarize(b_new, "novos_elegiveis_abr"),
    ]
    pd.DataFrame(groups).to_csv(OUT / "estatisticas_grupos.csv", index=False, encoding="utf-8-sig")

    delta_common = {c: med(comp, f"delta_{c}") for c in METRICS}
    # Diferença simples entre mediana dos novos e dos incumbentes em abril.
    entrant_gap = {}
    for c in METRICS:
        entrant_gap[c] = None if b_new.empty else med(b_new, c) - med(b_common, c)

    summary = {
        "elegiveis_mar": int(len(a)),
        "elegiveis_abr": int(len(b)),
        "comuns": int(len(common)),
        "novos_elegiveis_abril": int(len(entrants)),
        "saidas_da_elegibilidade": int(len(exits)),
        "crescimento_elegiveis_pct": float((len(b) / len(a) - 1) * 100),
        "hhi_agregado_mediana_mar": med(a, "portfolio_hhi"),
        "hhi_agregado_mediana_abr": med(b, "portfolio_hhi"),
        "hhi_comuns_mediana_mar": med(a_common, "portfolio_hhi"),
        "hhi_comuns_mediana_abr": med(b_common, "portfolio_hhi"),
        "hhi_novos_mediana_abr": med(b_new, "portfolio_hhi"),
        "hhi_norm_novos_mediana_abr": med(b_new, "portfolio_hhi_norm"),
        "n_fornecedores_novos_mediana_abr": med(b_new, "n_fornecedores"),
        "n_instrumentos_novos_mediana_abr": med(b_new, "n_instrumentos"),
        "delta_mediano_dentro_comuns": delta_common,
        "gap_mediana_novos_vs_comuns_abril": entrant_gap,
        "interpretacao": "A diferença entre a evolução da mediana agregada e a evolução dentro dos compradores comuns é tratada como efeito de composição descritivo. Novos elegíveis não são contrafactual nem grupo causal.",
    }
    (OUT / "resumo_composicao.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
