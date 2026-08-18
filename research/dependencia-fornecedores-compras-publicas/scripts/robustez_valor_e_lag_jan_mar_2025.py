#!/usr/bin/env python3
"""Robustez janeiro-março/2025: valor contratual e lags negativos.

Testes:
1. excluir instrumentos com lag_publicacao_dias < 0;
2. comparar valorInicial e valorGlobal em uma amostra comum de instrumentos com
   ambos os campos positivos;
3. diagnosticar a distribuição instrumento a instrumento de valorGlobal / valorInicial.

As métricas usam comprador institucional por CNPJ, rede global observada e
Strength global como ordenação principal dos choques. Resultados permanecem
condicionais à coorte de publicações até março de 2025.
"""
from __future__ import annotations

import json, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"processed"/"pncp_mensal"
RES=ROOT/"results"
OUT=RES/"robustez_valor_lag_jan_mar_2025"
OUT.mkdir(parents=True,exist_ok=True)
SEED=20260818
DRAWS=1000


def load():
    frames=[]
    for m in [1,2,3]:
        p=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        d=pd.read_csv(p,dtype={"id_contrato":"string","orgao_cnpj":"string","fornecedor_id_limpo":"string"},low_memory=False)
        for c in ["valorInicial","valorGlobal","lag_publicacao_dias","ano_assinatura"]:
            d[c]=pd.to_numeric(d[c],errors="coerce")
        frames.append(d)
    x=pd.concat(frames,ignore_index=True)
    return x[x["ano_assinatura"].eq(2025)].copy()


def norm_hhi(h,n):
    floor=1/n
    return ((h-floor)/(1-floor)) if n>1 else np.nan


def metrics(x,value_col):
    z=x[pd.to_numeric(x[value_col],errors="coerce").gt(0)].copy()
    z["value"]=pd.to_numeric(z[value_col],errors="coerce")
    rel=z.groupby(["orgao_cnpj","fornecedor_id_limpo"]).agg(value=("value","sum"),n=("id_contrato","nunique")).reset_index()
    rel["share"]=rel["value"]/rel.groupby("orgao_cnpj")["value"].transform("sum")
    rel["share_n"]=rel["n"]/rel.groupby("orgao_cnpj")["n"].transform("sum")
    rows=[]
    for b,g in rel.groupby("orgao_cnpj"):
        sv=g.share.sort_values(ascending=False); sn=g.share_n.sort_values(ascending=False)
        h=float((sv**2).sum()); hc=float((sn**2).sum()); N=len(g)
        rows.append({"orgao_cnpj":b,"n_fornecedores":N,"n_instrumentos":int(g.n.sum()),"hhi":h,"hhi_norm":norm_hhi(h,N),"count_hhi":hc,"cr1":float(sv.iloc[0]),"cr4":float(sv.iloc[:4].sum()),"neff":1/h})
    buyers=pd.DataFrame(rows)
    sup=rel.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"),strength=("value","sum")).reset_index()
    sup["pct_strength"]=sup.strength.rank(pct=True,method="average")
    zz=rel.merge(sup[["fornecedor_id_limpo","pct_strength"]],on="fornecedor_id_limpo",how="left")
    zz["piece"]=zz.share*zz.pct_strength
    exp=zz.groupby("orgao_cnpj").piece.sum().rename("exposure_strength").reset_index()
    buyers=buyers.merge(exp,on="orgao_cnpj",how="left")
    return z,rel,buyers,sup


def describe(b,eligible_ids,label):
    g=b[b.orgao_cnpj.astype(str).isin(set(eligible_ids))].copy()
    qh=g.hhi.quantile(.75); qe=g.exposure_strength.quantile(.75)
    rho,p=spearmanr(g.hhi_norm,g.exposure_strength,nan_policy="omit")
    return {"spec":label,"n":len(g),"hhi_mediana":float(g.hhi.median()),"hhi_norm_mediana":float(g.hhi_norm.median()),"count_hhi_mediana":float(g.count_hhi.median()),"cr1_mediana":float(g.cr1.median()),"cr4_mediana":float(g.cr4.median()),"neff_mediana":float(g.neff.median()),"value_hhi_gt_count_pct":float((g.hhi>g.count_hhi).mean()*100),"hidden_exposure_pct":float(((g.hhi<qh)&(g.exposure_strength>=qe)).mean()*100),"rho_hhi_norm_exposure":float(rho),"p_rho":float(p)}


def simulate(rel,sup,eligible_ids):
    r=rel.copy(); r["orgao_cnpj"]=r.orgao_cnpj.astype(str); r["fornecedor_id_limpo"]=r.fornecedor_id_limpo.astype(str)
    bids=sorted(set(map(str,eligible_ids))); slist=sorted(sup.fornecedor_id_limpo.astype(str).unique())
    bi={v:i for i,v in enumerate(bids)}; si={v:i for i,v in enumerate(slist)}
    A=np.zeros((len(bids),len(slist)),dtype=np.float32)
    for row in r[r.orgao_cnpj.isin(set(bids))].itertuples(index=False):A[bi[row.orgao_cnpj],si[row.fornecedor_id_limpo]]+=float(row.share)
    ss=sup.copy(); ss["fornecedor_id_limpo"]=ss.fornecedor_id_limpo.astype(str); ss["idx"]=ss.fornecedor_id_limpo.map(si)
    rng=np.random.default_rng(SEED); out=[]
    for pct in [.01,.05,.10]:
        k=max(1,int(math.ceil(len(slist)*pct))); rnd=[]
        for _ in range(DRAWS):
            idx=rng.choice(len(slist),size=k,replace=False); loss=A[:,idx].sum(axis=1); rnd.append(float((loss>=.5).mean()))
        rr=np.asarray(rnd); idx=ss.nlargest(k,"strength").idx.astype(int).to_numpy(); loss=A[:,idx].sum(axis=1)
        out.append({"pct_removed":pct,"k":k,"target_strength_severe_50":float((loss>=.5).mean()),"random_mean":float(rr.mean()),"random_p025":float(np.quantile(rr,.025)),"random_p975":float(np.quantile(rr,.975))})
    return out


def value_ratio_diagnostics(common):
    z=common[["id_contrato","valorInicial","valorGlobal"]].copy()
    z["ratio_global_inicial"]=z["valorGlobal"]/z["valorInicial"]
    ratio=z["ratio_global_inicial"].replace([np.inf,-np.inf],np.nan).dropna()
    equal=np.isclose(z["valorGlobal"],z["valorInicial"],rtol=1e-9,atol=0.01)
    gt=z["valorGlobal"]>z["valorInicial"]+0.01
    lt=z["valorGlobal"]<z["valorInicial"]-0.01
    quantiles={str(q):float(ratio.quantile(q)) for q in [0,.01,.05,.25,.5,.75,.9,.95,.99,1]}
    summary={"n_instrumentos_comuns":int(len(z)),"valor_global_igual_inicial_n":int(equal.sum()),"valor_global_igual_inicial_pct":float(equal.mean()*100),"valor_global_maior_inicial_n":int(gt.sum()),"valor_global_maior_inicial_pct":float(gt.mean()*100),"valor_global_menor_inicial_n":int(lt.sum()),"valor_global_menor_inicial_pct":float(lt.mean()*100),"ratio_global_inicial_quantiles":quantiles,"soma_valorInicial":float(z["valorInicial"].sum()),"soma_valorGlobal":float(z["valorGlobal"].sum()),"razao_somas_global_inicial":float(z["valorGlobal"].sum()/z["valorInicial"].sum())}
    pd.DataFrame([summary | {"ratio_global_inicial_quantiles":json.dumps(quantiles,ensure_ascii=False)}]).to_csv(OUT/"diagnostico_valorGlobal_valorInicial.csv",index=False,encoding="utf-8-sig")
    return summary


def main():
    x=load(); baseline=x[x.valorInicial.gt(0)].copy(); no_neg=baseline[~baseline.lag_publicacao_dias.lt(0)].copy(); common=x[x.valorInicial.gt(0)&x.valorGlobal.gt(0)].copy(); ratio_diag=value_ratio_diagnostics(common)
    _,r0,b0,s0=metrics(baseline,"valorInicial"); _,rn,bn,sn=metrics(no_neg,"valorInicial"); _,ri,bi,si=metrics(common,"valorInicial"); _,rg,bg,sg=metrics(common,"valorGlobal")
    e0=set(b0[(b0.n_fornecedores>=3)&(b0.n_instrumentos>=5)].orgao_cnpj.astype(str)); en=set(bn[(bn.n_fornecedores>=3)&(bn.n_instrumentos>=5)].orgao_cnpj.astype(str)); common_lag=sorted(e0&en)
    ei=set(bi[(bi.n_fornecedores>=3)&(bi.n_instrumentos>=5)].orgao_cnpj.astype(str)); eg=set(bg[(bg.n_fornecedores>=3)&(bg.n_instrumentos>=5)].orgao_cnpj.astype(str)); common_value=sorted(ei&eg)
    desc=pd.DataFrame([describe(b0,common_lag,"lag_baseline"),describe(bn,common_lag,"lag_exclui_negativos"),describe(bi,common_value,"valorInicial_amostra_comum"),describe(bg,common_value,"valorGlobal_amostra_comum")]); desc.to_csv(OUT/"comparacao_metricas.csv",index=False,encoding="utf-8-sig")
    simulations=[]
    for label,rel,sup,ids in [("lag_baseline",r0,s0,common_lag),("lag_exclui_negativos",rn,sn,common_lag),("valorInicial_amostra_comum",ri,si,common_value),("valorGlobal_amostra_comum",rg,sg,common_value)]:
        for row in simulate(rel,sup,ids):row["spec"]=label; simulations.append(row)
    pd.DataFrame(simulations).to_csv(OUT/"simulacoes_strength.csv",index=False,encoding="utf-8-sig")
    val_cov={"instrumentos_assinados_2025":int(len(x)),"valorInicial_positivo":int(x.valorInicial.gt(0).sum()),"valorGlobal_positivo":int(x.valorGlobal.gt(0).sum()),"ambos_positivos":int((x.valorInicial.gt(0)&x.valorGlobal.gt(0)).sum()),"valorGlobal_positivo_pct_sobre_valorInicial":float((x.valorInicial.gt(0)&x.valorGlobal.gt(0)).sum()/max(int(x.valorInicial.gt(0).sum()),1)*100),"lags_negativos_no_baseline":int(baseline.lag_publicacao_dias.lt(0).sum())}
    summary={"cobertura":val_cov,"diagnostico_valor_global_vs_inicial":ratio_diag,"amostra_comum_lag_compradores":len(common_lag),"amostra_comum_valores_compradores":len(common_value),"metricas":desc.to_dict(orient="records"),"simulacoes":simulations,"decision_rule":"Se excluir lags negativos produzir mudanças desprezíveis, a exclusão será robustez. Se valorGlobal alterar níveis/magnitudes, valorInicial permanece principal por representar o compromisso na celebração e valorGlobal deve ser reportado como robustez material, não como equivalência."}
    (OUT/"resumo_robustez.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
