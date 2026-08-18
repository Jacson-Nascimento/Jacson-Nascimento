#!/usr/bin/env python3
"""Robustez dos modelos associativos: região e fractional logit.

Testa duas questões:
1. substituir efeitos fixos de UF por macrorregião, reduzindo risco de estimativas
   instáveis em UFs com poucas observações;
2. estimar fractional logit (GLM Binomial com resposta fracionária) para
   PortfolioHHI normalizado, que respeita o suporte [0,1].

Erros-padrão são agrupados por município. Resultados são associativos e
condicionais à coorte jan-fev/2025.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"results"
INP=RES/"siconfi_integracao_jan_fev_2025"/"painel_compradores_pncp_siconfi_jan_fev.csv"
OUT=RES/"robustez_modelos_regiao_fractional_jan_fev_2025"
OUT.mkdir(parents=True,exist_ok=True)

REGION={
    "AC":"Norte","AP":"Norte","AM":"Norte","PA":"Norte","RO":"Norte","RR":"Norte","TO":"Norte",
    "AL":"Nordeste","BA":"Nordeste","CE":"Nordeste","MA":"Nordeste","PB":"Nordeste","PE":"Nordeste","PI":"Nordeste","RN":"Nordeste","SE":"Nordeste",
    "DF":"Centro-Oeste","GO":"Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste",
    "ES":"Sudeste","MG":"Sudeste","RJ":"Sudeste","SP":"Sudeste",
    "PR":"Sul","RS":"Sul","SC":"Sul",
}


def norm_hhi(hhi,n):
    h=pd.to_numeric(hhi,errors="coerce"); nn=pd.to_numeric(n,errors="coerce")
    floor=1/nn
    return ((h-floor)/(1-floor)).where(nn>1).clip(0,1)


def prep():
    d=pd.read_csv(INP,dtype={"orgao_cnpj":"string","uf":"string","municipio_ibge":"string"},low_memory=False)
    for c in ["portfolio_hhi","count_hhi","n_fornecedores","n_instrumentos","despesa_empenhada_2025","populacao_siconfi_2025","exposicao_strength","valor_total"]:
        d[c]=pd.to_numeric(d[c],errors="coerce")
    d["portfolio_hhi_norm"]=norm_hhi(d["portfolio_hhi"],d["n_fornecedores"])
    d["count_hhi_norm"]=norm_hhi(d["count_hhi"],d["n_fornecedores"])
    d["regiao"]=d["uf"].map(REGION)
    d["log_populacao"]=np.log(d["populacao_siconfi_2025"].where(d["populacao_siconfi_2025"]>0))
    d["despesa_pc"]=d["despesa_empenhada_2025"]/d["populacao_siconfi_2025"]
    d["log_despesa_pc"]=np.log(d["despesa_pc"].where(d["despesa_pc"]>0))
    d["log_n_fornecedores"]=np.log(d["n_fornecedores"].where(d["n_fornecedores"]>0))
    d["instr_por_forn"]=d["n_instrumentos"]/d["n_fornecedores"]
    d["log_instr_por_forn"]=np.log(d["instr_por_forn"].where(d["instr_por_forn"]>0))
    a=d[(d["n_fornecedores"]>=3)&(d["n_instrumentos"]>=5)&d["despesa_empenhada_2025"].gt(0)&d["populacao_siconfi_2025"].gt(0)&d["portfolio_hhi_norm"].notna()&d["regiao"].notna()&d["municipio_ibge"].notna()].copy()
    return a


def tidy(model,name,kind):
    ci=model.conf_int()
    return pd.DataFrame({
        "modelo":name,"tipo":kind,"termo":model.params.index,"coef":model.params.values,
        "erro_padrao":model.bse.values,"estatistica":model.tvalues.values,"p":model.pvalues.values,
        "ci95_inf":ci.iloc[:,0].values,"ci95_sup":ci.iloc[:,1].values,
    })


def fit_ols(a,name,formula):
    m=smf.ols(formula,data=a).fit(cov_type="cluster",cov_kwds={"groups":a["municipio_ibge"],"use_correction":True})
    return m,tidy(m,name,"OLS_cluster")


def fit_frac(a,name,formula):
    m=smf.glm(formula,data=a,family=sm.families.Binomial()).fit(cov_type="cluster",cov_kwds={"groups":a["municipio_ibge"],"use_correction":True})
    tab=tidy(m,name,"fractional_logit_cluster")
    # Average marginal effect aproximado para covariáveis contínuas:
    # beta_j * mean(mu_i*(1-mu_i)). Para dummies de região não é usado.
    mu=np.asarray(m.predict(a),dtype=float)
    scale=float(np.mean(mu*(1-mu)))
    tab["ame_continuo"] = np.where(tab["termo"].isin(["log_populacao","log_despesa_pc","log_n_fornecedores","log_instr_por_forn"]),tab["coef"]*scale,np.nan)
    return m,tab,scale


def main():
    a=prep()
    counts_uf=a.groupby("uf").agg(n_compradores=("orgao_cnpj","size"),n_municipios=("municipio_ibge","nunique")).reset_index().sort_values("n_compradores")
    counts_reg=a.groupby("regiao").agg(n_compradores=("orgao_cnpj","size"),n_municipios=("municipio_ibge","nunique")).reset_index().sort_values("regiao")
    counts_uf.to_csv(OUT/"contagens_por_uf.csv",index=False,encoding="utf-8-sig")
    counts_reg.to_csv(OUT/"contagens_por_regiao.csv",index=False,encoding="utf-8-sig")

    f_ext="portfolio_hhi_norm ~ log_populacao + log_despesa_pc"
    f_reg="portfolio_hhi_norm ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"

    ols1,t1=fit_ols(a,"O1_HHI_norm_externo",f_ext)
    ols2,t2=fit_ols(a,"O2_HHI_norm_regiao",f_reg)
    fl1,tf1,s1=fit_frac(a,"F1_HHI_norm_externo",f_ext)
    fl2,tf2,s2=fit_frac(a,"F2_HHI_norm_regiao",f_reg)
    allcoef=pd.concat([t1,t2,tf1,tf2],ignore_index=True)
    allcoef.to_csv(OUT/"coeficientes_robustez.csv",index=False,encoding="utf-8-sig")

    key_terms=["log_populacao","log_despesa_pc","log_n_fornecedores","log_instr_por_forn"]
    key=allcoef[allcoef["termo"].isin(key_terms)].copy()
    key.to_csv(OUT/"coeficientes_chave.csv",index=False,encoding="utf-8-sig")

    def get(model,term):
        z=allcoef[(allcoef["modelo"]==model)&(allcoef["termo"]==term)]
        if z.empty:return None
        r=z.iloc[0]
        return {"coef":float(r.coef),"se":float(r.erro_padrao),"p":float(r.p),"ci95":[float(r.ci95_inf),float(r.ci95_sup)],"ame":None if pd.isna(r.ame_continuo) else float(r.ame_continuo)}

    # Quão esparsas são as UFs? Relatar contagens <=5 e <=10.
    sparse5=counts_uf[counts_uf["n_compradores"]<=5].to_dict(orient="records")
    sparse10=counts_uf[counts_uf["n_compradores"]<=10].to_dict(orient="records")
    summary={
        "n":int(len(a)),"clusters_municipio":int(a["municipio_ibge"].nunique()),
        "regioes":counts_reg.to_dict(orient="records"),
        "ufs_com_ate_5_compradores":sparse5,"ufs_com_ate_10_compradores":sparse10,
        "fractional_logit":"GLM Binomial para resposta fracionária; erros agrupados por município.",
        "O1":{"populacao":get("O1_HHI_norm_externo","log_populacao"),"despesa_pc":get("O1_HHI_norm_externo","log_despesa_pc")},
        "O2":{"populacao":get("O2_HHI_norm_regiao","log_populacao"),"despesa_pc":get("O2_HHI_norm_regiao","log_despesa_pc"),"n_fornecedores":get("O2_HHI_norm_regiao","log_n_fornecedores"),"recorrencia":get("O2_HHI_norm_regiao","log_instr_por_forn")},
        "F1":{"populacao":get("F1_HHI_norm_externo","log_populacao"),"despesa_pc":get("F1_HHI_norm_externo","log_despesa_pc")},
        "F2":{"populacao":get("F2_HHI_norm_regiao","log_populacao"),"despesa_pc":get("F2_HHI_norm_regiao","log_despesa_pc"),"n_fornecedores":get("F2_HHI_norm_regiao","log_n_fornecedores"),"recorrencia":get("F2_HHI_norm_regiao","log_instr_por_forn")},
        "decision_rule":"Se sinais e conclusões sobre as covariáveis principais persistirem em OLS-região e fractional logit, a evidência não depende criticamente da forma linear nem de FE de UF esparsos.",
    }
    (OUT/"resumo_robustez_modelos.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2)); print("\nCoeficientes-chave:\n",key.to_string(index=False))

if __name__=="__main__":main()
