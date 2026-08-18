#!/usr/bin/env python3
"""Modelos associativos PNCP × SICONFI para a coorte acumulada jan-mar/2025.

Replica a especificação validada em jan-fev:
- HHI monetário normalizado como resposta principal;
- log população + log despesa empenhada per capita como controles externos;
- log número de fornecedores + log instrumentos por fornecedor como controles de carteira;
- efeitos fixos de macrorregião;
- erros-padrão agrupados por município;
- fractional logit como robustez da forma funcional.

Também compara, termo a termo, os coeficientes OLS/fractional de jan-mar com os
resultados jan-fev já versionados. Não há estratégia causal.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"results"
INP=RES/"siconfi_integracao_acumulada_2025_03"/"painel_compradores_pncp_siconfi_2025_03.csv"
OLD=RES/"robustez_modelos_regiao_fractional_jan_fev_2025"/"coeficientes_robustez.csv"
OUT=RES/"modelos_associativos_jan_mar_2025"
OUT.mkdir(parents=True,exist_ok=True)

REGION={
    "AC":"Norte","AP":"Norte","AM":"Norte","PA":"Norte","RO":"Norte","RR":"Norte","TO":"Norte",
    "AL":"Nordeste","BA":"Nordeste","CE":"Nordeste","MA":"Nordeste","PB":"Nordeste","PE":"Nordeste","PI":"Nordeste","RN":"Nordeste","SE":"Nordeste",
    "DF":"Centro-Oeste","GO":"Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste",
    "ES":"Sudeste","MG":"Sudeste","RJ":"Sudeste","SP":"Sudeste",
    "PR":"Sul","RS":"Sul","SC":"Sul",
}
KEY=["log_populacao","log_despesa_pc","log_n_fornecedores","log_instr_por_forn"]


def norm_hhi(hhi,n):
    h=pd.to_numeric(hhi,errors="coerce"); nn=pd.to_numeric(n,errors="coerce")
    floor=1/nn
    return ((h-floor)/(1-floor)).where(nn>1).clip(0,1)


def prep():
    d=pd.read_csv(INP,dtype={"orgao_cnpj":"string","uf":"string","municipio_ibge":"string"},low_memory=False)
    nums=["portfolio_hhi","count_hhi","n_fornecedores","n_instrumentos","despesa_empenhada_2025",
          "populacao_siconfi_2025","exposicao_strength","valor_total"]
    for c in nums:d[c]=pd.to_numeric(d[c],errors="coerce")
    d["portfolio_hhi_norm"]=norm_hhi(d.portfolio_hhi,d.n_fornecedores)
    d["count_hhi_norm"]=norm_hhi(d.count_hhi,d.n_fornecedores)
    d["hhi_norm_gap_value_count"]=d.portfolio_hhi_norm-d.count_hhi_norm
    d["regiao"]=d.uf.map(REGION)
    d["log_populacao"]=np.log(d.populacao_siconfi_2025.where(d.populacao_siconfi_2025>0))
    d["despesa_pc"]=d.despesa_empenhada_2025/d.populacao_siconfi_2025
    d["log_despesa_pc"]=np.log(d.despesa_pc.where(d.despesa_pc>0))
    d["log_n_fornecedores"]=np.log(d.n_fornecedores.where(d.n_fornecedores>0))
    d["instr_por_forn"]=d.n_instrumentos/d.n_fornecedores
    d["log_instr_por_forn"]=np.log(d.instr_por_forn.where(d.instr_por_forn>0))
    a=d[(d.n_fornecedores>=3)&(d.n_instrumentos>=5)&d.despesa_empenhada_2025.gt(0)&
        d.populacao_siconfi_2025.gt(0)&d.portfolio_hhi_norm.notna()&d.count_hhi_norm.notna()&
        d.exposicao_strength.notna()&d.regiao.notna()&d.municipio_ibge.notna()].copy()
    return a


def tidy(model,name,kind):
    ci=model.conf_int()
    return pd.DataFrame({"modelo":name,"tipo":kind,"termo":model.params.index,
        "coef":model.params.values,"erro_padrao":model.bse.values,"estatistica":model.tvalues.values,
        "p":model.pvalues.values,"ci95_inf":ci.iloc[:,0].values,"ci95_sup":ci.iloc[:,1].values})


def ols(a,name,formula):
    m=smf.ols(formula,data=a).fit(cov_type="cluster",cov_kwds={"groups":a.municipio_ibge,"use_correction":True})
    return m,tidy(m,name,"OLS_cluster")


def frac(a,name,formula):
    m=smf.glm(formula,data=a,family=sm.families.Binomial()).fit(cov_type="cluster",cov_kwds={"groups":a.municipio_ibge,"use_correction":True})
    t=tidy(m,name,"fractional_logit_cluster")
    mu=np.asarray(m.predict(a),dtype=float); scale=float(np.mean(mu*(1-mu)))
    t["ame_continuo"]=np.where(t.termo.isin(KEY),t.coef*scale,np.nan)
    return m,t


def vif(a):
    z=a[KEY].replace([np.inf,-np.inf],np.nan).dropna().astype(float)
    z=(z-z.mean())/z.std(ddof=0)
    return pd.DataFrame([{"variavel":c,"vif":float(variance_inflation_factor(z.values,i)),"n":len(z)} for i,c in enumerate(KEY)])


def compare_old(new):
    if not OLD.exists():return pd.DataFrame()
    old=pd.read_csv(OLD,low_memory=False)
    mapping={"O2_HHI_norm_regiao":"O2_HHI_norm_regiao","F2_HHI_norm_regiao":"F2_HHI_norm_regiao"}
    rows=[]
    for model_old,model_new in mapping.items():
        for term in KEY:
            a=old[(old.modelo==model_old)&(old.termo==term)]
            b=new[(new.modelo==model_new)&(new.termo==term)]
            if a.empty or b.empty:continue
            ro=a.iloc[0]; rn=b.iloc[0]
            co=float(ro.coef); cn=float(rn.coef)
            rows.append({"modelo":model_new,"termo":term,
                "coef_jan_fev":co,"p_jan_fev":float(ro.p),"coef_jan_mar":cn,"p_jan_mar":float(rn.p),
                "mesmo_sinal":bool(np.sign(co)==np.sign(cn)),
                "delta_coef":cn-co,
                "razao_abs_coef":None if abs(co)<1e-12 else abs(cn)/abs(co),
                "significativo_5pct_jan_fev":bool(float(ro.p)<.05),
                "significativo_5pct_jan_mar":bool(float(rn.p)<.05)})
    return pd.DataFrame(rows)


def main():
    a=prep()
    f_ext="portfolio_hhi_norm ~ log_populacao + log_despesa_pc"
    f_main="portfolio_hhi_norm ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"
    f_gap="hhi_norm_gap_value_count ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"
    f_exp="exposicao_strength ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"

    _,t1=ols(a,"O1_HHI_norm_externo",f_ext)
    _,t2=ols(a,"O2_HHI_norm_regiao",f_main)
    _,t3=ols(a,"O3_Gap_regiao",f_gap)
    _,t4=ols(a,"O4_Exposicao_strength_regiao",f_exp)
    _,tf1=frac(a,"F1_HHI_norm_externo",f_ext)
    _,tf2=frac(a,"F2_HHI_norm_regiao",f_main)
    coefs=pd.concat([t1,t2,t3,t4,tf1,tf2],ignore_index=True)
    coefs.to_csv(OUT/"coeficientes_modelos.csv",index=False,encoding="utf-8-sig")
    coefs[coefs.termo.isin(KEY)].to_csv(OUT/"coeficientes_chave.csv",index=False,encoding="utf-8-sig")

    vv=vif(a); vv.to_csv(OUT/"diagnostico_vif.csv",index=False,encoding="utf-8-sig")
    counts=a.groupby("regiao").agg(n_compradores=("orgao_cnpj","size"),n_municipios=("municipio_ibge","nunique")).reset_index()
    counts.to_csv(OUT/"contagens_por_regiao.csv",index=False,encoding="utf-8-sig")
    comp=compare_old(coefs); comp.to_csv(OUT/"comparacao_coeficientes_jan_fev_jan_mar.csv",index=False,encoding="utf-8-sig")

    def get(model,term):
        z=coefs[(coefs.modelo==model)&(coefs.termo==term)]
        if z.empty:return None
        r=z.iloc[0]
        return {"coef":float(r.coef),"se":float(r.erro_padrao),"p":float(r.p),"ci95":[float(r.ci95_inf),float(r.ci95_sup)]}

    summary={"natureza":"Modelos associativos; sem interpretação causal.","mes_final_publicacao":"2025-03",
        "n":int(len(a)),"clusters_municipio":int(a.municipio_ibge.nunique()),"regioes":counts.to_dict(orient="records"),
        "vif":vv.to_dict(orient="records"),
        "OLS_regiao":{"populacao":get("O2_HHI_norm_regiao","log_populacao"),"despesa_pc":get("O2_HHI_norm_regiao","log_despesa_pc"),
          "n_fornecedores":get("O2_HHI_norm_regiao","log_n_fornecedores"),"recorrencia":get("O2_HHI_norm_regiao","log_instr_por_forn")},
        "fractional_regiao":{"populacao":get("F2_HHI_norm_regiao","log_populacao"),"despesa_pc":get("F2_HHI_norm_regiao","log_despesa_pc"),
          "n_fornecedores":get("F2_HHI_norm_regiao","log_n_fornecedores"),"recorrencia":get("F2_HHI_norm_regiao","log_instr_por_forn")},
        "gap_regiao":{"populacao":get("O3_Gap_regiao","log_populacao"),"despesa_pc":get("O3_Gap_regiao","log_despesa_pc"),
          "n_fornecedores":get("O3_Gap_regiao","log_n_fornecedores"),"recorrencia":get("O3_Gap_regiao","log_instr_por_forn")},
        "exposicao_strength_regiao":{"populacao":get("O4_Exposicao_strength_regiao","log_populacao"),"despesa_pc":get("O4_Exposicao_strength_regiao","log_despesa_pc"),
          "n_fornecedores":get("O4_Exposicao_strength_regiao","log_n_fornecedores"),"recorrencia":get("O4_Exposicao_strength_regiao","log_instr_por_forn")},
        "comparacao_jan_fev":comp.to_dict(orient="records"),
        "regra_interpretacao":"Priorizar persistência de sinal e ordem de grandeza entre jan-fev e jan-mar; significância isolada não será tratada como evidência causal."}
    (OUT/"resumo_modelos.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
