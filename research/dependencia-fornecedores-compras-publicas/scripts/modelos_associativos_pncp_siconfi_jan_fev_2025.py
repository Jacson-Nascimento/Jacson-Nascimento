#!/usr/bin/env python3
"""Modelos associativos diagnósticos PNCP × SICONFI, janeiro-fevereiro/2025.

Versão reparametrizada após diagnóstico de multicolinearidade.

A parametrização original usava simultaneamente log(despesa), log(população),
log(instrumentos) e log(fornecedores), produzindo VIFs elevados. A especificação
principal passa a decompor essas dimensões em:

- tamanho territorial: log(população);
- intensidade fiscal: log(despesa empenhada per capita);
- amplitude da carteira: log(número de fornecedores);
- recorrência: log(instrumentos por fornecedor).

Erros-padrão principais são agrupados por município, porque compradores do mesmo
município compartilham controles fiscais e ambiente territorial. HC3 é mantido
como robustez. Não há estratégia causal.
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


def fit_model(df, name, formula, covariance="cluster_municipio"):
    base = smf.ols(formula, data=df)
    if covariance == "cluster_municipio":
        model = base.fit(cov_type="cluster", cov_kwds={"groups": df["municipio_ibge"], "use_correction": True})
        cov_label = "cluster_municipio"
    elif covariance == "HC3":
        model = base.fit(cov_type="HC3")
        cov_label = "HC3"
    else:
        model = base.fit()
        cov_label = "classica"
    ci = model.conf_int(alpha=.05)
    tab = pd.DataFrame({
        "modelo": name,
        "covariancia": cov_label,
        "termo": model.params.index,
        "coef": model.params.values,
        "erro_padrao": model.bse.values,
        "estatistica": model.tvalues.values,
        "p": model.pvalues.values,
        "ci95_inf": ci.iloc[:,0].values,
        "ci95_sup": ci.iloc[:,1].values,
    })
    info = {
        "modelo": name, "covariancia": cov_label, "formula": formula,
        "n": int(model.nobs), "r2": float(model.rsquared),
        "r2_ajustado": float(model.rsquared_adj), "aic": float(model.aic), "bic": float(model.bic),
        "clusters_municipio": int(df["municipio_ibge"].nunique()) if covariance=="cluster_municipio" else None,
    }
    return tab, info


def calc_vif(df, cols, label):
    z = df[cols].replace([np.inf,-np.inf],np.nan).dropna().copy()
    X = z.astype(float)
    X = (X-X.mean())/X.std(ddof=0)
    rows=[]
    for i,c in enumerate(cols):
        rows.append({"parametrizacao":label,"variavel":c,"vif":float(variance_inflation_factor(X.values,i)),"n":len(X)})
    return pd.DataFrame(rows)


def main():
    d = pd.read_csv(INP, dtype={"orgao_cnpj":"string","uf":"string","municipio_ibge":"string"}, low_memory=False)
    numeric=["portfolio_hhi","count_hhi","n_fornecedores","n_instrumentos","despesa_empenhada_2025",
             "populacao_siconfi_2025","exposicao_strength","log_despesa_empenhada","log_populacao_siconfi","valor_total"]
    for c in numeric: d[c]=pd.to_numeric(d[c],errors="coerce")

    d["portfolio_hhi_norm"]=normalized_hhi(d["portfolio_hhi"],d["n_fornecedores"])
    d["count_hhi_norm"]=normalized_hhi(d["count_hhi"],d["n_fornecedores"])
    d["hhi_norm_gap_value_count"]=d["portfolio_hhi_norm"]-d["count_hhi_norm"]
    d["log_n_instrumentos"]=np.log(d["n_instrumentos"].where(d["n_instrumentos"]>0))
    d["log_n_fornecedores"]=np.log(d["n_fornecedores"].where(d["n_fornecedores"]>0))
    d["log_valor_total"]=np.log(d["valor_total"].where(d["valor_total"]>0))
    d["despesa_pc"]=d["despesa_empenhada_2025"]/d["populacao_siconfi_2025"]
    d["log_despesa_pc"]=np.log(d["despesa_pc"].where(d["despesa_pc"]>0))
    d["instrumentos_por_fornecedor"]=d["n_instrumentos"]/d["n_fornecedores"]
    d["log_instrumentos_por_fornecedor"]=np.log(d["instrumentos_por_fornecedor"].where(d["instrumentos_por_fornecedor"]>0))

    a=d[(d["n_fornecedores"]>=3)&(d["n_instrumentos"]>=5)&d["despesa_empenhada_2025"].gt(0)
        &d["populacao_siconfi_2025"].gt(0)&d["portfolio_hhi_norm"].notna()&d["count_hhi_norm"].notna()
        &d["exposicao_strength"].notna()&d["uf"].notna()&d["municipio_ibge"].notna()].copy()

    raw_cols=["log_despesa_empenhada","log_populacao_siconfi","log_n_instrumentos","log_n_fornecedores"]
    new_cols=["log_populacao_siconfi","log_despesa_pc","log_n_fornecedores","log_instrumentos_por_fornecedor"]
    vif=pd.concat([calc_vif(a,raw_cols,"original"),calc_vif(a,new_cols,"reparametrizada")],ignore_index=True)
    vif.to_csv(OUT/"diagnostico_vif.csv",index=False,encoding="utf-8-sig")

    specs=[
        ("P1_HHI_norm_externo","portfolio_hhi_norm ~ log_populacao_siconfi + log_despesa_pc"),
        ("P2_HHI_norm_carteira","portfolio_hhi_norm ~ log_populacao_siconfi + log_despesa_pc + log_n_fornecedores + log_instrumentos_por_fornecedor"),
        ("P3_HHI_norm_UF_FE","portfolio_hhi_norm ~ log_populacao_siconfi + log_despesa_pc + log_n_fornecedores + log_instrumentos_por_fornecedor + C(uf)"),
        ("P4_CountHHI_norm","count_hhi_norm ~ log_populacao_siconfi + log_despesa_pc + log_n_fornecedores + log_instrumentos_por_fornecedor + C(uf)"),
        ("P5_Gap_valor_frequencia","hhi_norm_gap_value_count ~ log_populacao_siconfi + log_despesa_pc + log_n_fornecedores + log_instrumentos_por_fornecedor + C(uf)"),
        ("P6_Exposicao_strength","exposicao_strength ~ log_populacao_siconfi + log_despesa_pc + log_n_fornecedores + log_instrumentos_por_fornecedor + C(uf)"),
    ]

    tabs=[]; infos=[]
    for name,formula in specs:
        tab,info=fit_model(a,name,formula,"cluster_municipio"); tabs.append(tab); infos.append(info)
        # Mesma especificação com HC3, para robustez da inferência.
        tab_h,info_h=fit_model(a,name,formula,"HC3"); tabs.append(tab_h); infos.append(info_h)
    coefs=pd.concat(tabs,ignore_index=True)
    coefs.to_csv(OUT/"coeficientes_modelos.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame(infos).to_csv(OUT/"ajuste_modelos.csv",index=False,encoding="utf-8-sig")

    key_terms={"log_populacao_siconfi","log_despesa_pc","log_n_fornecedores","log_instrumentos_por_fornecedor"}
    key=coefs[coefs["termo"].isin(key_terms)].copy()
    key.to_csv(OUT/"coeficientes_chave.csv",index=False,encoding="utf-8-sig")

    desc=a[["portfolio_hhi_norm","count_hhi_norm","hhi_norm_gap_value_count","exposicao_strength",
            "log_populacao_siconfi","log_despesa_pc","log_n_fornecedores","log_instrumentos_por_fornecedor"]].describe(percentiles=[.1,.25,.5,.75,.9]).T
    desc.to_csv(OUT/"descritivas_amostra_modelos.csv",encoding="utf-8-sig")

    # Correlações entre novos controles para facilitar leitura do VIF.
    corr=a[new_cols].corr(method="pearson")
    corr.to_csv(OUT/"correlacao_controles_reparametrizados.csv",encoding="utf-8-sig")

    def getcoef(model,term,cov="cluster_municipio"):
        z=coefs[(coefs["modelo"]==model)&(coefs["covariancia"]==cov)&(coefs["termo"]==term)]
        if z.empty:return None
        r=z.iloc[0]
        return {"coef":float(r["coef"]),"se":float(r["erro_padrao"]),"p":float(r["p"]),"ci95":[float(r["ci95_inf"]),float(r["ci95_sup"])]}

    vif_new=vif[vif["parametrizacao"]=="reparametrizada"].copy()
    vif_old=vif[vif["parametrizacao"]=="original"].copy()
    summary={
        "natureza":"Modelos associativos diagnósticos; sem interpretação causal.",
        "escopo":"Contratos assinados em 2025 e publicados até fevereiro; compradores >=3 fornecedores e >=5 instrumentos; cobertura fiscal válida.",
        "n":int(len(a)),"clusters_municipio":int(a["municipio_ibge"].nunique()),
        "parametrizacao_principal":{"tamanho":"log_populacao_siconfi","intensidade_fiscal":"log_despesa_pc","amplitude_carteira":"log_n_fornecedores","recorrencia":"log_instrumentos_por_fornecedor"},
        "motivo_reparametrizacao":"A parametrização original apresentou VIFs elevados (~31 para despesa/população e ~14 para instrumentos/fornecedores).",
        "vif_original":vif_old.to_dict(orient="records"),"vif_reparametrizada":vif_new.to_dict(orient="records"),
        "P1_HHI_externo":{"log_populacao":getcoef("P1_HHI_norm_externo","log_populacao_siconfi"),"log_despesa_pc":getcoef("P1_HHI_norm_externo","log_despesa_pc")},
        "P3_HHI_UF_FE":{"log_populacao":getcoef("P3_HHI_norm_UF_FE","log_populacao_siconfi"),"log_despesa_pc":getcoef("P3_HHI_norm_UF_FE","log_despesa_pc"),"log_n_fornecedores":getcoef("P3_HHI_norm_UF_FE","log_n_fornecedores"),"log_instr_por_forn":getcoef("P3_HHI_norm_UF_FE","log_instrumentos_por_fornecedor")},
        "P5_Gap":{"log_populacao":getcoef("P5_Gap_valor_frequencia","log_populacao_siconfi"),"log_despesa_pc":getcoef("P5_Gap_valor_frequencia","log_despesa_pc"),"log_n_fornecedores":getcoef("P5_Gap_valor_frequencia","log_n_fornecedores"),"log_instr_por_forn":getcoef("P5_Gap_valor_frequencia","log_instrumentos_por_fornecedor")},
        "P6_Exposicao":{"log_populacao":getcoef("P6_Exposicao_strength","log_populacao_siconfi"),"log_despesa_pc":getcoef("P6_Exposicao_strength","log_despesa_pc"),"log_n_fornecedores":getcoef("P6_Exposicao_strength","log_n_fornecedores"),"log_instr_por_forn":getcoef("P6_Exposicao_strength","log_instrumentos_por_fornecedor")},
        "nao_usado":"ProcurementIntensity parcial continua fora dos modelos principais por incompletude do numerador e possível correlação mecânica com medidas de valor.",
    }
    (OUT/"resumo_modelos.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2)); print("\nVIF:\n",vif.to_string(index=False)); print("\nCoeficientes-chave cluster:\n",key[key["covariancia"]=="cluster_municipio"].to_string(index=False))

if __name__=="__main__":main()
