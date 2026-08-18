#!/usr/bin/env python3
"""Modelos associativos PNCP × SICONFI parametrizados por mês final de 2025.

Preserva a especificação pré-fixada: HHI normalizado; população e despesa
empenhada per capita; amplitude e recorrência da carteira; efeitos de
macrorregião; erros agrupados por município; fractional logit como robustez.

Uso:
  python scripts/modelos_associativos_pncp_siconfi_generico.py --month 6 --compare-month 5
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"results"
KEY=["log_populacao","log_despesa_pc","log_n_fornecedores","log_instr_por_forn"]
HIST={2:"fev",3:"mar",4:"abr",5:"mai",6:"jun"}
REGION={
 "AC":"Norte","AP":"Norte","AM":"Norte","PA":"Norte","RO":"Norte","RR":"Norte","TO":"Norte",
 "AL":"Nordeste","BA":"Nordeste","CE":"Nordeste","MA":"Nordeste","PB":"Nordeste","PE":"Nordeste","PI":"Nordeste","RN":"Nordeste","SE":"Nordeste",
 "DF":"Centro-Oeste","GO":"Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste",
 "ES":"Sudeste","MG":"Sudeste","RJ":"Sudeste","SP":"Sudeste","PR":"Sul","RS":"Sul","SC":"Sul"}

def args():
 p=argparse.ArgumentParser(); p.add_argument("--month",type=int,required=True,choices=range(2,13)); p.add_argument("--compare-month",type=int,default=None,choices=range(1,13)); return p.parse_args()

def norm_hhi(hhi,n):
 h=pd.to_numeric(hhi,errors="coerce"); nn=pd.to_numeric(n,errors="coerce"); floor=1/nn
 return ((h-floor)/(1-floor)).where(nn>1).clip(0,1)

def model_dir(month):
 if month in HIST: return RES/f"modelos_associativos_jan_{HIST[month]}_2025"
 return RES/f"modelos_associativos_generico_2025_{month:02d}"

def prep(inp):
 d=pd.read_csv(inp,dtype={"orgao_cnpj":"string","uf":"string","municipio_ibge":"string"},low_memory=False)
 nums=["portfolio_hhi","portfolio_hhi_norm","count_hhi","count_hhi_norm","n_fornecedores","n_instrumentos","despesa_empenhada_2025","populacao_siconfi_2025","exposicao_strength","valor_total"]
 for c in nums:
  if c in d.columns:d[c]=pd.to_numeric(d[c],errors="coerce")
 d["portfolio_hhi_norm"]=norm_hhi(d.portfolio_hhi,d.n_fornecedores); d["count_hhi_norm"]=norm_hhi(d.count_hhi,d.n_fornecedores)
 d["hhi_norm_gap_value_count"]=d.portfolio_hhi_norm-d.count_hhi_norm; d["regiao"]=d.uf.map(REGION)
 d["log_populacao"]=np.log(d.populacao_siconfi_2025.where(d.populacao_siconfi_2025>0)); d["despesa_pc"]=d.despesa_empenhada_2025/d.populacao_siconfi_2025
 d["log_despesa_pc"]=np.log(d.despesa_pc.where(d.despesa_pc>0)); d["log_n_fornecedores"]=np.log(d.n_fornecedores.where(d.n_fornecedores>0))
 d["instr_por_forn"]=d.n_instrumentos/d.n_fornecedores; d["log_instr_por_forn"]=np.log(d.instr_por_forn.where(d.instr_por_forn>0))
 return d[(d.n_fornecedores>=3)&(d.n_instrumentos>=5)&d.despesa_empenhada_2025.gt(0)&d.populacao_siconfi_2025.gt(0)&d.portfolio_hhi_norm.notna()&d.count_hhi_norm.notna()&d.exposicao_strength.notna()&d.regiao.notna()&d.municipio_ibge.notna()].copy()

def tidy(m,name,kind):
 ci=m.conf_int(); return pd.DataFrame({"modelo":name,"tipo":kind,"termo":m.params.index,"coef":m.params.values,"erro_padrao":m.bse.values,"estatistica":m.tvalues.values,"p":m.pvalues.values,"ci95_inf":ci.iloc[:,0].values,"ci95_sup":ci.iloc[:,1].values})
def ols(a,n,f):
 m=smf.ols(f,data=a).fit(cov_type="cluster",cov_kwds={"groups":a.municipio_ibge,"use_correction":True}); return tidy(m,n,"OLS_cluster")
def frac(a,n,f):
 m=smf.glm(f,data=a,family=sm.families.Binomial()).fit(cov_type="cluster",cov_kwds={"groups":a.municipio_ibge,"use_correction":True}); t=tidy(m,n,"fractional_logit_cluster"); mu=np.asarray(m.predict(a),dtype=float); t["ame_continuo"]=np.where(t.termo.isin(KEY),t.coef*float(np.mean(mu*(1-mu))),np.nan); return t
def vif(a):
 z=a[KEY].replace([np.inf,-np.inf],np.nan).dropna().astype(float); z=(z-z.mean())/z.std(ddof=0); return pd.DataFrame([{"variavel":c,"vif":float(variance_inflation_factor(z.values,i)),"n":len(z)} for i,c in enumerate(KEY)])

def compare(new,old_path,cm,m):
 if not old_path.exists(): return pd.DataFrame()
 old=pd.read_csv(old_path/"coeficientes_modelos.csv",low_memory=False); rows=[]
 for model in ["O2_HHI_norm_regiao","F2_HHI_norm_regiao"]:
  for term in KEY:
   x=old[(old.modelo==model)&(old.termo==term)]; y=new[(new.modelo==model)&(new.termo==term)]
   if x.empty or y.empty:continue
   ro,rn=x.iloc[0],y.iloc[0]; co,cn=float(ro.coef),float(rn.coef)
   rows.append({"modelo":model,"termo":term,f"coef_m{cm:02d}":co,f"p_m{cm:02d}":float(ro.p),f"coef_m{m:02d}":cn,f"p_m{m:02d}":float(rn.p),"mesmo_sinal":bool(np.sign(co)==np.sign(cn)),"delta_coef":cn-co,"razao_abs_coef":None if abs(co)<1e-12 else abs(cn)/abs(co),f"significativo_5pct_m{cm:02d}":bool(float(ro.p)<.05),f"significativo_5pct_m{m:02d}":bool(float(rn.p)<.05)})
 return pd.DataFrame(rows)

def main():
 a0=args(); m=a0.month; cm=a0.compare_month or m-1
 if cm>=m:raise ValueError("--compare-month deve ser menor que --month")
 inp=RES/f"siconfi_integracao_acumulada_2025_{m:02d}"/f"painel_compradores_pncp_siconfi_2025_{m:02d}.csv"; out=RES/f"modelos_associativos_generico_2025_{m:02d}"; out.mkdir(parents=True,exist_ok=True)
 if not inp.exists():raise FileNotFoundError(inp)
 a=prep(inp)
 fext="portfolio_hhi_norm ~ log_populacao + log_despesa_pc"; fmain="portfolio_hhi_norm ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"; fgap="hhi_norm_gap_value_count ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"; fexp="exposicao_strength ~ log_populacao + log_despesa_pc + log_n_fornecedores + log_instr_por_forn + C(regiao)"
 coefs=pd.concat([ols(a,"O1_HHI_norm_externo",fext),ols(a,"O2_HHI_norm_regiao",fmain),ols(a,"O3_Gap_regiao",fgap),ols(a,"O4_Exposicao_strength_regiao",fexp),frac(a,"F1_HHI_norm_externo",fext),frac(a,"F2_HHI_norm_regiao",fmain)],ignore_index=True)
 coefs.to_csv(out/"coeficientes_modelos.csv",index=False,encoding="utf-8-sig"); coefs[coefs.termo.isin(KEY)].to_csv(out/"coeficientes_chave.csv",index=False,encoding="utf-8-sig")
 vv=vif(a); vv.to_csv(out/"diagnostico_vif.csv",index=False,encoding="utf-8-sig"); counts=a.groupby("regiao").agg(n_compradores=("orgao_cnpj","size"),n_municipios=("municipio_ibge","nunique")).reset_index(); counts.to_csv(out/"contagens_por_regiao.csv",index=False,encoding="utf-8-sig")
 comp=compare(coefs,model_dir(cm),cm,m); comp.to_csv(out/f"comparacao_coeficientes_m{cm:02d}_m{m:02d}.csv",index=False,encoding="utf-8-sig")
 def get(model,term):
  z=coefs[(coefs.modelo==model)&(coefs.termo==term)]
  if z.empty:return None
  r=z.iloc[0]; return {"coef":float(r.coef),"se":float(r.erro_padrao),"p":float(r.p),"ci95":[float(r.ci95_inf),float(r.ci95_sup)]}
 summary={"natureza":"Modelos associativos; sem interpretação causal.","mes_final_publicacao":f"2025-{m:02d}","mes_comparacao":f"2025-{cm:02d}","especificacao":"Especificação pré-fixada; nenhuma seleção de covariáveis após observar o mês.","n":int(len(a)),"clusters_municipio":int(a.municipio_ibge.nunique()),"regioes":counts.to_dict(orient="records"),"vif":vv.to_dict(orient="records"),"OLS_regiao":{"populacao":get("O2_HHI_norm_regiao","log_populacao"),"despesa_pc":get("O2_HHI_norm_regiao","log_despesa_pc"),"n_fornecedores":get("O2_HHI_norm_regiao","log_n_fornecedores"),"recorrencia":get("O2_HHI_norm_regiao","log_instr_por_forn")},"fractional_regiao":{"populacao":get("F2_HHI_norm_regiao","log_populacao"),"despesa_pc":get("F2_HHI_norm_regiao","log_despesa_pc"),"n_fornecedores":get("F2_HHI_norm_regiao","log_n_fornecedores"),"recorrencia":get("F2_HHI_norm_regiao","log_instr_por_forn")},"gap_regiao":{"populacao":get("O3_Gap_regiao","log_populacao"),"despesa_pc":get("O3_Gap_regiao","log_despesa_pc"),"n_fornecedores":get("O3_Gap_regiao","log_n_fornecedores"),"recorrencia":get("O3_Gap_regiao","log_instr_por_forn")},"exposicao_strength_regiao":{"populacao":get("O4_Exposicao_strength_regiao","log_populacao"),"despesa_pc":get("O4_Exposicao_strength_regiao","log_despesa_pc"),"n_fornecedores":get("O4_Exposicao_strength_regiao","log_n_fornecedores"),"recorrencia":get("O4_Exposicao_strength_regiao","log_instr_por_forn")},"comparacao_mes_anterior":comp.to_dict(orient="records"),"regra_interpretacao":"Priorizar persistência de sinal e ordem de grandeza; significância isolada não é evidência causal."}
 (out/"resumo_modelos_generico.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
