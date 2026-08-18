#!/usr/bin/env python3
"""Modelos associativos diagnósticos PNCP × SICONFI, janeiro-fevereiro/2025.

Objetivo: avaliar associações condicionais entre características fiscais/escala
e quatro dimensões da carteira de fornecedores:

1. PortfolioHHI normalizado;
2. CountHHI normalizado;
3. gap normalizado valor - frequência;
4. exposição a fornecedores de alto Strength.

Não há estratégia causal. As estimativas são diagnósticas e condicionais à
coorte de instrumentos assinados em 2025 e publicados até fevereiro.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
INP = RES / "siconfi_integracao_jan_fev_2025" / "painel_compradores_pncp_siconfi_jan_fev.csv"
OUT = RES / "modelos_associativos_jan_fev_2025"
OUT.mkdir(parents=True, exist_ok=True)


def normalized_hhi(hhi, n):
    h = pd.to_numeric(hhi, errors="coerce")
    nn = pd.to_numeric(n, errors="coerce")
    floor = 1.0 / nn
    out = (h - floor) / (1.0 - floor)
    return out.where(nn > 1).clip(0, 1)


def fit_ols(df: pd.DataFrame, name: str, formula: str):
    model = smf.ols(formula, data=df).fit(cov_type="HC3")
    ci = model.conf_int(alpha=0.05)
    tab = pd.DataFrame({
        "modelo": name,
        "termo": model.params.index,
        "coef": model.params.values,
        "erro_padrao_HC3": model.bse.values,
        "t": model.tvalues.values,
        "p": model.pvalues.values,
        "ci95_inf": ci.iloc[:, 0].values,
        "ci95_sup": ci.iloc[:, 1].values,
    })
    info = {
        "modelo": name,
        "formula": formula,
        "n": int(model.nobs),
        "r2": float(model.rsquared),
        "r2_ajustado": float(model.rsquared_adj),
        "aic": float(model.aic),
        "bic": float(model.bic),
        "covariancia": "HC3",
    }
    return model, tab, info


def calc_vif(df: pd.DataFrame, cols):
    z = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if z.empty:
        return pd.DataFrame()
    X = z.astype(float)
    X = (X - X.mean()) / X.std(ddof=0)
    rows = []
    for i, c in enumerate(cols):
        rows.append({"variavel": c, "vif": float(variance_inflation_factor(X.values, i)), "n": len(X)})
    return pd.DataFrame(rows)


def main():
    d = pd.read_csv(INP, dtype={"orgao_cnpj": "string", "uf": "string"}, low_memory=False)

    numeric = [
        "portfolio_hhi", "count_hhi", "n_fornecedores", "n_instrumentos",
        "despesa_empenhada_2025", "populacao_siconfi_2025", "exposicao_strength",
        "log_despesa_empenhada", "log_populacao_siconfi", "valor_total",
    ]
    for c in numeric:
        d[c] = pd.to_numeric(d[c], errors="coerce")

    d["portfolio_hhi_norm"] = normalized_hhi(d["portfolio_hhi"], d["n_fornecedores"])
    d["count_hhi_norm"] = normalized_hhi(d["count_hhi"], d["n_fornecedores"])
    d["hhi_norm_gap_value_count"] = d["portfolio_hhi_norm"] - d["count_hhi_norm"]
    d["log_n_instrumentos"] = np.log1p(d["n_instrumentos"])
    d["log_n_fornecedores"] = np.log(d["n_fornecedores"].where(d["n_fornecedores"] > 0))
    d["log_valor_total"] = np.log(d["valor_total"].where(d["valor_total"] > 0))

    # Amostra principal: mesma elegibilidade já usada no diagnóstico e cobertura fiscal válida.
    a = d[
        (d["n_fornecedores"] >= 3)
        & (d["n_instrumentos"] >= 5)
        & d["despesa_empenhada_2025"].gt(0)
        & d["populacao_siconfi_2025"].gt(0)
        & d["portfolio_hhi_norm"].notna()
        & d["count_hhi_norm"].notna()
        & d["exposicao_strength"].notna()
    ].copy()

    # Não usar ProcurementIntensity parcial nos modelos principais: numerador é coorte parcial.
    specs = [
        (
            "M1_HHI_norm_escala_externa",
            "portfolio_hhi_norm ~ log_despesa_empenhada + log_populacao_siconfi",
        ),
        (
            "M2_HHI_norm_escala_carteira",
            "portfolio_hhi_norm ~ log_despesa_empenhada + log_populacao_siconfi + log_n_instrumentos + log_n_fornecedores",
        ),
        (
            "M3_HHI_norm_UF_FE",
            "portfolio_hhi_norm ~ log_despesa_empenhada + log_populacao_siconfi + log_n_instrumentos + log_n_fornecedores + C(uf)",
        ),
        (
            "M4_CountHHI_norm",
            "count_hhi_norm ~ log_despesa_empenhada + log_populacao_siconfi + log_n_instrumentos + log_n_fornecedores + C(uf)",
        ),
        (
            "M5_Gap_valor_frequencia",
            "hhi_norm_gap_value_count ~ log_despesa_empenhada + log_populacao_siconfi + log_n_instrumentos + log_n_fornecedores + C(uf)",
        ),
        (
            "M6_Exposicao_strength",
            "exposicao_strength ~ log_despesa_empenhada + log_populacao_siconfi + log_n_instrumentos + log_n_fornecedores + C(uf)",
        ),
    ]

    coef_tables = []
    infos = []
    models = {}
    for name, formula in specs:
        m, tab, info = fit_ols(a, name, formula)
        models[name] = m
        coef_tables.append(tab)
        infos.append(info)

    coefs = pd.concat(coef_tables, ignore_index=True)
    coefs.to_csv(OUT / "coeficientes_modelos_OLS_HC3.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(infos).to_csv(OUT / "ajuste_modelos.csv", index=False, encoding="utf-8-sig")

    vif_cols = ["log_despesa_empenhada", "log_populacao_siconfi", "log_n_instrumentos", "log_n_fornecedores"]
    vif = calc_vif(a, vif_cols)
    vif.to_csv(OUT / "diagnostico_vif.csv", index=False, encoding="utf-8-sig")

    # Modelo alternativo sem efeitos fixos de UF e com valor total no lugar de número de instrumentos,
    # apenas como diagnóstico de especificação.
    alt_formula = "portfolio_hhi_norm ~ log_despesa_empenhada + log_populacao_siconfi + log_valor_total + log_n_fornecedores"
    _, alt_tab, alt_info = fit_ols(a, "R1_HHI_norm_log_valor", alt_formula)
    alt_tab.to_csv(OUT / "robustez_modelo_log_valor.csv", index=False, encoding="utf-8-sig")

    # Resultados-chave em formato compacto, excluindo dummies de UF.
    key_terms = {"log_despesa_empenhada", "log_populacao_siconfi", "log_n_instrumentos", "log_n_fornecedores"}
    key = coefs[coefs["termo"].isin(key_terms)].copy()
    key.to_csv(OUT / "coeficientes_chave.csv", index=False, encoding="utf-8-sig")

    descriptive = a[[
        "portfolio_hhi_norm", "count_hhi_norm", "hhi_norm_gap_value_count",
        "exposicao_strength", "log_despesa_empenhada", "log_populacao_siconfi",
        "log_n_instrumentos", "log_n_fornecedores"
    ]].describe(percentiles=[.1,.25,.5,.75,.9]).T
    descriptive.to_csv(OUT / "descritivas_amostra_modelos.csv", encoding="utf-8-sig")

    def coef(name, term):
        z = coefs[(coefs["modelo"] == name) & (coefs["termo"] == term)]
        if z.empty:
            return None
        r = z.iloc[0]
        return {
            "coef": float(r["coef"]), "se_HC3": float(r["erro_padrao_HC3"]),
            "p": float(r["p"]), "ci95": [float(r["ci95_inf"]), float(r["ci95_sup"])],
        }

    summary = {
        "natureza": "Modelos associativos diagnósticos; sem interpretação causal.",
        "escopo": "Contratos assinados em 2025 e publicados até fevereiro; compradores >=3 fornecedores e >=5 instrumentos; cobertura fiscal válida.",
        "n_modelos_principais": len(a),
        "outcomes": ["portfolio_hhi_norm", "count_hhi_norm", "hhi_norm_gap_value_count", "exposicao_strength"],
        "nao_utilizado_como_explicativa_principal": "procurement_intensity_parcial, porque o numerador PNCP é incompleto na coorte jan-fev e compartilha componente de valor com medidas de rede.",
        "M1": {
            "log_despesa": coef("M1_HHI_norm_escala_externa", "log_despesa_empenhada"),
            "log_populacao": coef("M1_HHI_norm_escala_externa", "log_populacao_siconfi"),
        },
        "M3": {
            "log_despesa": coef("M3_HHI_norm_UF_FE", "log_despesa_empenhada"),
            "log_populacao": coef("M3_HHI_norm_UF_FE", "log_populacao_siconfi"),
            "log_n_instrumentos": coef("M3_HHI_norm_UF_FE", "log_n_instrumentos"),
            "log_n_fornecedores": coef("M3_HHI_norm_UF_FE", "log_n_fornecedores"),
        },
        "M5_gap": {
            "log_despesa": coef("M5_Gap_valor_frequencia", "log_despesa_empenhada"),
            "log_populacao": coef("M5_Gap_valor_frequencia", "log_populacao_siconfi"),
            "log_n_instrumentos": coef("M5_Gap_valor_frequencia", "log_n_instrumentos"),
            "log_n_fornecedores": coef("M5_Gap_valor_frequencia", "log_n_fornecedores"),
        },
        "vif": vif.to_dict(orient="records"),
        "ajuste": infos + [alt_info],
    }
    (OUT / "resumo_modelos.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\nCoeficientes-chave:\n", key.to_string(index=False))


if __name__ == "__main__":
    main()
