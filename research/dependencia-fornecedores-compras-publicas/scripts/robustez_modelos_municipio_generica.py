#!/usr/bin/env python3
"""Robustezes econometricas para evitar sobrepeso de municipios com varios compradores.

Mantem os modelos principais intactos e adiciona:
1. WLS no nivel comprador com peso 1/N_compradores_municipio;
2. OLS em painel agregado ao municipio;
3. outcomes CR1 e CR4 como verificacao de que conclusoes nao dependem da
   normalizacao do HHI nem da relacao mecanica entre HHI e numero de fornecedores.

Uso:
    python scripts/robustez_modelos_municipio_generica.py --month 6
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
REGION = {
    "AC":"Norte","AP":"Norte","AM":"Norte","PA":"Norte","RO":"Norte","RR":"Norte","TO":"Norte",
    "AL":"Nordeste","BA":"Nordeste","CE":"Nordeste","MA":"Nordeste","PB":"Nordeste","PE":"Nordeste","PI":"Nordeste","RN":"Nordeste","SE":"Nordeste",
    "DF":"Centro-Oeste","GO":"Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste",
    "ES":"Sudeste","MG":"Sudeste","RJ":"Sudeste","SP":"Sudeste","PR":"Sul","RS":"Sul","SC":"Sul",
}
KEY = ["log_populacao", "log_despesa_pc", "log_n_fornecedores", "log_instr_por_forn"]


def prep(path: Path) -> pd.DataFrame:
    d = pd.read_csv(path, dtype={"orgao_cnpj":"string", "uf":"string", "municipio_ibge":"string"}, low_memory=False)
    nums = [
        "portfolio_hhi", "portfolio_hhi_norm", "portfolio_cr1", "portfolio_cr4",
        "n_fornecedores", "n_instrumentos", "despesa_empenhada_2025",
        "populacao_siconfi_2025", "exposicao_strength", "valor_total"
    ]
    for c in nums:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    d["regiao"] = d.uf.map(REGION)
    d["log_populacao"] = np.log(d.populacao_siconfi_2025.where(d.populacao_siconfi_2025 > 0))
    d["despesa_pc"] = d.despesa_empenhada_2025 / d.populacao_siconfi_2025
    d["log_despesa_pc"] = np.log(d.despesa_pc.where(d.despesa_pc > 0))
    d["log_n_fornecedores"] = np.log(d.n_fornecedores.where(d.n_fornecedores > 0))
    d["instr_por_forn"] = d.n_instrumentos / d.n_fornecedores
    d["log_instr_por_forn"] = np.log(d.instr_por_forn.where(d.instr_por_forn > 0))
    req = (
        (d.n_fornecedores >= 3) & (d.n_instrumentos >= 5)
        & d.despesa_empenhada_2025.gt(0) & d.populacao_siconfi_2025.gt(0)
        & d.portfolio_hhi_norm.notna() & d.regiao.notna() & d.municipio_ibge.notna()
    )
    d = d[req].copy()
    nmun = d.groupby("municipio_ibge").orgao_cnpj.transform("size")
    d["n_compradores_municipio"] = nmun
    d["peso_municipio_igual"] = 1.0 / nmun
    return d


def tidy(m, modelo, tipo):
    ci = m.conf_int()
    return pd.DataFrame({
        "modelo": modelo,
        "tipo": tipo,
        "termo": m.params.index,
        "coef": m.params.values,
        "erro_padrao": m.bse.values,
        "p": m.pvalues.values,
        "ci95_inf": ci.iloc[:, 0].values,
        "ci95_sup": ci.iloc[:, 1].values,
    })


def fit_wls(d: pd.DataFrame, outcome: str, name: str):
    f = f"{outcome} ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"
    m = smf.wls(f, data=d, weights=d.peso_municipio_igual).fit(
        cov_type="cluster", cov_kwds={"groups": d.municipio_ibge, "use_correction": True}
    )
    return tidy(m, name, "WLS_peso_municipio_cluster")


def aggregate_municipality(d: pd.DataFrame) -> pd.DataFrame:
    # Variaveis fiscais e populacao sao municipais; medias evitam replicacao por CNPJ comprador.
    g = d.groupby(["municipio_ibge", "uf", "regiao"], as_index=False).agg(
        portfolio_hhi_norm=("portfolio_hhi_norm", "mean"),
        portfolio_cr1=("portfolio_cr1", "mean"),
        portfolio_cr4=("portfolio_cr4", "mean"),
        exposicao_strength=("exposicao_strength", "mean"),
        log_populacao=("log_populacao", "first"),
        log_despesa_pc=("log_despesa_pc", "first"),
        log_n_fornecedores=("log_n_fornecedores", "mean"),
        log_instr_por_forn=("log_instr_por_forn", "mean"),
        n_compradores=("orgao_cnpj", "size"),
    )
    return g


def fit_muni(d: pd.DataFrame, outcome: str, name: str):
    f = f"{outcome} ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"
    m = smf.ols(f, data=d).fit(cov_type="HC3")
    return tidy(m, name, "OLS_municipio_HC3")


def key_summary(coefs: pd.DataFrame, model: str):
    z = coefs[(coefs.modelo == model) & coefs.termo.isin(KEY)]
    return {
        r.termo: {
            "coef": float(r.coef), "se": float(r.erro_padrao), "p": float(r.p),
            "ci95": [float(r.ci95_inf), float(r.ci95_sup)]
        }
        for r in z.itertuples(index=False)
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", type=int, required=True, choices=range(2, 13))
    a = ap.parse_args()
    m = a.month
    path = RES / f"siconfi_integracao_acumulada_2025_{m:02d}" / f"painel_compradores_pncp_siconfi_2025_{m:02d}.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    d = prep(path)
    dm = aggregate_municipality(d)

    outcomes = [
        ("portfolio_hhi_norm", "HHI_norm"),
        ("portfolio_cr1", "CR1"),
        ("portfolio_cr4", "CR4"),
        ("exposicao_strength", "Exposicao_strength"),
    ]
    chunks = []
    for outcome, label in outcomes:
        if outcome not in d.columns or d[outcome].notna().sum() < 30:
            continue
        chunks.append(fit_wls(d.dropna(subset=[outcome]), outcome, f"WLS_{label}"))
        if outcome in dm.columns and dm[outcome].notna().sum() >= 30:
            chunks.append(fit_muni(dm.dropna(subset=[outcome]), outcome, f"MUNI_{label}"))
    coefs = pd.concat(chunks, ignore_index=True)

    out = RES / f"robustez_modelos_municipio_2025_{m:02d}"
    out.mkdir(parents=True, exist_ok=True)
    coefs.to_csv(out / "coeficientes_robustez.csv", index=False, encoding="utf-8-sig")
    dm.to_csv(out / "painel_agregado_municipio.csv", index=False, encoding="utf-8-sig")

    models = list(coefs.modelo.unique())
    summary = {
        "mes_final": m,
        "natureza": "Robustez econometrica associativa; sem interpretacao causal.",
        "n_compradores": int(len(d)),
        "n_municipios": int(d.municipio_ibge.nunique()),
        "peso_comprador": "1/N de compradores elegiveis no municipio",
        "modelos": {model: key_summary(coefs, model) for model in models},
        "interpretacao": [
            "A ponderacao evita que municipios com mais CNPJs compradores tenham peso mecanicamente maior.",
            "A agregacao municipal testa o mesmo ponto em unidade territorial unica.",
            "CR1 e CR4 sao outcomes de robustez para reduzir dependencia da normalizacao do HHI e da relacao matematica entre HHI e numero de fornecedores.",
            "Resultados permanecem associativos e nao identificam efeitos causais.",
        ],
    }
    (out / "resumo_robustez_modelos.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
