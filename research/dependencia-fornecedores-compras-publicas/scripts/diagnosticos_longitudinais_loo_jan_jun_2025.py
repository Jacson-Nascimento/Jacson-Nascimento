#!/usr/bin/env python3
"""Diagnósticos longitudinais com exposição externalizada LOO.

Compara abril-maio e maio-junho de 2025 utilizando Strength LOO e Degree LOO.
As classificações por quartil são recalculadas dentro de cada coorte mensal.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = RES / "diagnosticos_longitudinais_loo_jan_jun_2025"


def rho(x, y):
    z = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(z) < 3:
        return {"rho": None, "p": None, "n": int(len(z))}
    r, p = spearmanr(z.x, z.y)
    return {"rho": float(r), "p": float(p), "n": int(len(z))}


def load_month(m):
    p = RES / f"exposicao_loo_2025_{m:02d}" / "metricas_compradores_loo.csv"
    if not p.exists():
        raise FileNotFoundError(p)
    d = pd.read_csv(p, dtype={"orgao_cnpj":"string"}, low_memory=False)
    for c in ["portfolio_hhi", "portfolio_hhi_norm", "exposicao_strength_loo", "exposicao_degree_loo"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d


def flags(d, exposure):
    qh = float(d.portfolio_hhi.quantile(.75))
    qe = float(d[exposure].quantile(.75))
    out = d[["orgao_cnpj", "portfolio_hhi", "portfolio_hhi_norm", exposure]].copy()
    out["hhi_alto"] = out.portfolio_hhi >= qh
    out["exp_alta"] = out[exposure] >= qe
    out["discordancia"] = (~out.hhi_alto) & out.exp_alta
    out["quadrante"] = out.hhi_alto.astype(int).astype(str) + out.exp_alta.astype(int).astype(str)
    return out, qh, qe


def retention(old_ids, new_ids, common_ids):
    old = set(map(str, old_ids)) & set(common_ids)
    new = set(map(str, new_ids)) & set(common_ids)
    return None if not old else float(len(old & new) / len(old))


def compare_pair(m1, m2, d1, d2):
    common_ids = set(d1.orgao_cnpj.astype(str)) & set(d2.orgao_cnpj.astype(str))
    entrants = set(d2.orgao_cnpj.astype(str)) - set(d1.orgao_cnpj.astype(str))
    exits = set(d1.orgao_cnpj.astype(str)) - set(d2.orgao_cnpj.astype(str))

    a = d1[d1.orgao_cnpj.astype(str).isin(common_ids)].copy()
    b = d2[d2.orgao_cnpj.astype(str).isin(common_ids)].copy()
    merged = a.merge(b, on="orgao_cnpj", suffixes=("_m1", "_m2"), validate="one_to_one")

    result = {
        "de": m1,
        "para": m2,
        "n_mes_anterior": int(len(d1)),
        "n_mes_atual": int(len(d2)),
        "n_comuns": int(len(common_ids)),
        "n_entrantes": int(len(entrants)),
        "n_saidas": int(len(exits)),
        "spearman_strength_loo": rho(merged.exposicao_strength_loo_m1, merged.exposicao_strength_loo_m2),
        "spearman_degree_loo": rho(merged.exposicao_degree_loo_m1, merged.exposicao_degree_loo_m2),
    }

    for exposure, label in [("exposicao_strength_loo", "strength_loo"), ("exposicao_degree_loo", "degree_loo")]:
        f1, qh1, qe1 = flags(d1, exposure)
        f2, qh2, qe2 = flags(d2, exposure)
        f1c = f1[f1.orgao_cnpj.astype(str).isin(common_ids)]
        f2c = f2[f2.orgao_cnpj.astype(str).isin(common_ids)]
        fm = f1c.merge(f2c, on="orgao_cnpj", suffixes=("_m1", "_m2"), validate="one_to_one")

        top_old = f1.loc[f1.exp_alta, "orgao_cnpj"]
        top_new = f2.loc[f2.exp_alta, "orgao_cnpj"]
        disc_old = f1.loc[f1.discordancia, "orgao_cnpj"]
        disc_new = f2.loc[f2.discordancia, "orgao_cnpj"]

        result[label] = {
            "q75_hhi_m1": qh1,
            "q75_hhi_m2": qh2,
            "q75_exposicao_m1": qe1,
            "q75_exposicao_m2": qe2,
            "retencao_quartil_superior": retention(top_old, top_new, common_ids),
            "retencao_discordancia": retention(disc_old, disc_new, common_ids),
            "estabilidade_quadrante_completo": float((fm.quadrante_m1 == fm.quadrante_m2).mean()),
            "discordantes_m1": int(f1.discordancia.sum()),
            "discordantes_m2": int(f2.discordancia.sum()),
        }

    b_common = d2[d2.orgao_cnpj.astype(str).isin(common_ids)]
    b_entr = d2[d2.orgao_cnpj.astype(str).isin(entrants)]
    result["composicao"] = {
        "hhi_mediana_comuns_no_mes_atual": float(b_common.portfolio_hhi.median()) if len(b_common) else None,
        "hhi_mediana_entrantes": float(b_entr.portfolio_hhi.median()) if len(b_entr) else None,
        "strength_loo_mediana_comuns": float(b_common.exposicao_strength_loo.median()) if len(b_common) else None,
        "strength_loo_mediana_entrantes": float(b_entr.exposicao_strength_loo.median()) if len(b_entr) else None,
        "degree_loo_mediana_comuns": float(b_common.exposicao_degree_loo.median()) if len(b_common) else None,
        "degree_loo_mediana_entrantes": float(b_entr.exposicao_degree_loo.median()) if len(b_entr) else None,
    }
    return result


def main():
    months = {m: load_month(m) for m in [4, 5, 6]}
    comps = [compare_pair(4, 5, months[4], months[5]), compare_pair(5, 6, months[5], months[6])]
    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([
        {
            "de": x["de"], "para": x["para"], "n_comuns": x["n_comuns"],
            "rho_strength_loo": x["spearman_strength_loo"]["rho"],
            "rho_degree_loo": x["spearman_degree_loo"]["rho"],
            "retencao_top_strength_loo": x["strength_loo"]["retencao_quartil_superior"],
            "retencao_top_degree_loo": x["degree_loo"]["retencao_quartil_superior"],
            "retencao_discord_strength_loo": x["strength_loo"]["retencao_discordancia"],
            "retencao_discord_degree_loo": x["degree_loo"]["retencao_discordancia"],
            "estabilidade_quadrante_strength_loo": x["strength_loo"]["estabilidade_quadrante_completo"],
            "estabilidade_quadrante_degree_loo": x["degree_loo"]["estabilidade_quadrante_completo"],
        }
        for x in comps
    ]).to_csv(OUT / "resumo_transicoes.csv", index=False, encoding="utf-8-sig")

    summary = {
        "natureza": "Diagnostico longitudinal descritivo com exposicao externalizada leave-one-buyer-out.",
        "transicoes": comps,
        "regra_interpretacao": "Persistencia indica estabilidade de screening, nao permanencia causal de risco.",
    }
    (OUT / "resumo_longitudinal_loo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
