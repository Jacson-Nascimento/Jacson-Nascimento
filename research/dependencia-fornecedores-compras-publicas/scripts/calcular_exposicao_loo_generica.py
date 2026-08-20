#!/usr/bin/env python3
"""Calcula exposição externa LOO do comprador sem executar stress tests.

Uso:
    python scripts/calcular_exposicao_loo_generica.py --month 4

O script reutiliza a implementação auditada de leave-one-buyer-out da robustez
estrutural e produz uma saída mensal adequada aos diagnósticos longitudinais.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from robustez_estrutural_generica import build_loo, classify_discordance, spearman

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"


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

    rel = pd.read_csv(rel_path, dtype={"orgao_cnpj":"string", "fornecedor_id_limpo":"string"}, low_memory=False)
    buyers = pd.read_csv(buyers_path, dtype={"orgao_cnpj":"string"}, low_memory=False)
    suppliers = pd.read_csv(sup_path, dtype={"fornecedor_id_limpo":"string"}, low_memory=False)
    eligible = buyers[(buyers.n_fornecedores >= 3) & (buyers.n_instrumentos >= 5)].copy()

    loo = build_loo(rel, eligible, suppliers)
    loo, raw_sum = classify_discordance(loo, "exposicao_strength_global", "strength_raw")
    loo, sloo_sum = classify_discordance(loo, "exposicao_strength_loo", "strength_loo")
    loo, dloo_sum = classify_discordance(loo, "exposicao_degree_loo", "degree_loo")

    out = RES / f"exposicao_loo_2025_{m:02d}"
    out.mkdir(parents=True, exist_ok=True)
    loo.to_csv(out / "metricas_compradores_loo.csv", index=False, encoding="utf-8-sig")

    summary = {
        "mes_final": m,
        "n_elegiveis": int(len(loo)),
        "strength_original_vs_loo": spearman(loo.exposicao_strength_global, loo.exposicao_strength_loo),
        "degree_original_vs_loo": spearman(loo.exposicao_degree_global, loo.exposicao_degree_loo),
        "strength_loo_vs_degree_loo": spearman(loo.exposicao_strength_loo, loo.exposicao_degree_loo),
        "hhi_norm_vs_strength_loo": spearman(loo.portfolio_hhi_norm, loo.exposicao_strength_loo),
        "hhi_norm_vs_degree_loo": spearman(loo.portfolio_hhi_norm, loo.exposicao_degree_loo),
        "discordancia": {
            "strength_raw": raw_sum,
            "strength_loo": sloo_sum,
            "degree_loo": dloo_sum,
        },
        "regra": "Strength bruto mede importancia sistemica; Strength LOO e Degree LOO medem exposicao externa do comprador.",
    }
    (out / "resumo_exposicao_loo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
