#!/usr/bin/env python3
"""Robustez jan-mar/2025 ao tratamento de contratos/empenhos.

Especificações:
A. todos os instrumentos PJ válidos assinados em 2025;
B. exclusão de `tipo_contrato == Empenho`;
C. limite inferior conservador: dentro de cada
   (id_compra, orgao_cnpj, fornecedor), manter apenas o instrumento de maior
   valorInicial. A especificação C não é tratada como verdade econômica; ela
   serve apenas para verificar se o padrão central depende de multiplicidade de
   instrumentos vinculados à mesma contratação e fornecedor.

A comparação principal usa a interseção de compradores elegíveis (>=3
fornecedores e >=5 instrumentos/unidades observadas) entre as especificações.
A rede é global em cada especificação e Strength é o choque principal.
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
OUT=RES/"robustez_tipos_instrumento_jan_mar_2025"
OUT.mkdir(parents=True,exist_ok=True)
SEED=20260818
DRAWS=1000


def load():
    frames=[]
    for m in [1,2,3]:
        p=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        d=pd.read_csv(p,dtype={"id_contrato":"string","id_compra":"string","orgao_cnpj":"string","fornecedor_id_limpo":"string","tipo_contrato":"string"},low_memory=False)
        d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce")
        d["valorInicial"]=pd.to_numeric(d["valorInicial"],errors="coerce")
        d["tipo_contrato_norm"]=d["tipo_contrato"].astype("string").str.strip()
        frames.append(d)
    x=pd.concat(frames,ignore_index=True)
    return x[x.ano_assinatura.eq(2025)&x.valorInicial.gt(0)].copy()


def norm_hhi(h,n):
    if n<=1:return np.nan
    floor=1/n
    return max(0.0,min(1.0,(h-floor)/(1-floor)))


def prepare_variant(x,label):
    if label=="todos":
        z=x.copy(); z["analysis_unit"]=z["id_contrato"].astype(str)
    elif label=="sem_empenho":
        z=x[~x["tipo_contrato_norm"].str.casefold().eq("empenho")].copy(); z["analysis_unit"]=z["id_contrato"].astype(str)
    elif label=="colapsa_compra_fornecedor_max":
        z=x.copy()
        # Se id_compra for ausente, preservar o instrumento individual.
        z["key_compra"] = z["id_compra"].astype("string")
        miss=z["key_compra"].isna()|z["key_compra"].eq("")|z["key_compra"].eq("<NA>")
        z.loc[miss,"key_compra"]="SEMCOMPRA::"+z.loc[miss,"id_contrato"].astype(str)
        z=z.sort_values(["key_compra","orgao_cnpj","fornecedor_id_limpo","valorInicial","id_contrato"],ascending=[True,True,True,False,True])
        z=z.drop_duplicates(["key_compra","orgao_cnpj","fornecedor_id_limpo"],keep="first").copy()
        z["analysis_unit"]=z["key_compra"].astype(str)+"::"+z["orgao_cnpj"].astype(str)+"::"+z["fornecedor_id_limpo"].astype(str)
    else:raise ValueError(label)
    return z


def metrics(z):
    rel=z.groupby(["orgao_cnpj","fornecedor_id_limpo"]).agg(value=("valorInicial","sum"),n=("analysis_unit","nunique")).reset_index()
    rel["share"]=rel.value/rel.groupby("orgao_cnpj").value.transform("sum")
    rel["share_n"]=rel.n/rel.groupby("orgao_cnpj").n.transform("sum")
    rows=[]
    for b,g in rel.groupby("orgao_cnpj"):
        sv=g.share.sort_values(ascending=False); sc=g.share_n.sort_values(ascending=False); N=len(g)
        h=float((sv**2).sum()); hc=float((sc**2).sum())
        rows.append({"orgao_cnpj":b,"n_fornecedores":N,"n_unidades":int(g.n.sum()),"hhi":h,"hhi_norm":norm_hhi(h,N),"count_hhi":hc,"cr1":float(sv.iloc[0]),"cr4":float(sv.iloc[:4].sum()),"neff":1/h})
    buyers=pd.DataFrame(rows)
    sup=rel.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"),strength=("value","sum")).reset_index()
    sup["pct_strength"]=sup.strength.rank(pct=True,method="average")
    q=rel.merge(sup[["fornecedor_id_limpo","pct_strength"]],on="fornecedor_id_limpo",how="left")
    q["piece"]=q.share*q.pct_strength
    exp=q.groupby("orgao_cnpj").piece.sum().rename("exposure_strength").reset_index()
    buyers=buyers.merge(exp,on="orgao_cnpj",how="left")
    return rel,buyers,sup


def description(b,ids,label):
    g=b[b.orgao_cnpj.astype(str).isin(ids)].copy(); qh=g.hhi.quantile(.75); qe=g.exposure_strength.quantile(.75)
    rho,p=spearmanr(g.hhi_norm,g.exposure_strength,nan_policy="omit")
    return {"spec":label,"n_compradores":len(g),"hhi_mediana":float(g.hhi.median()),"hhi_norm_mediana":float(g.hhi_norm.median()),"count_hhi_mediana":float(g.count_hhi.median()),"cr1_mediana":float(g.cr1.median()),"cr4_mediana":float(g.cr4.median()),"neff_mediana":float(g.neff.median()),"value_gt_count_pct":float((g.hhi>g.count_hhi).mean()*100),"hidden_exposure_pct":float(((g.hhi<qh)&(g.exposure_strength>=qe)).mean()*100),"rho_hhi_norm_exposure":float(rho),"p_rho":float(p)}


def simulate(rel,sup,ids):
    r=rel.copy(); r["orgao_cnpj"]=r.orgao_cnpj.astype(str); r["fornecedor_id_limpo"]=r.fornecedor_id_limpo.astype(str)
    bids=sorted(ids); slist=sorted(sup.fornecedor_id_limpo.astype(str).unique()); bi={v:i for i,v in enumerate(bids)}; si={v:i for i,v in enumerate(slist)}
    A=np.zeros((len(bids),len(slist)),dtype=np.float32)
    for row in r[r.orgao_cnpj.isin(set(bids))].itertuples(index=False):A[bi[row.orgao_cnpj],si[row.fornecedor_id_limpo]]+=float(row.share)
    ss=sup.copy(); ss["fornecedor_id_limpo"]=ss.fornecedor_id_limpo.astype(str); ss["idx"]=ss.fornecedor_id_limpo.map(si)
    rng=np.random.default_rng(SEED); out=[]
    for pct in [.01,.05,.10]:
        k=max(1,int(math.ceil(len(slist)*pct))); rnd=[]
        for _ in range(DRAWS):
            idx=rng.choice(len(slist),size=k,replace=False); loss=A[:,idx].sum(axis=1); rnd.append(float((loss>=.5).mean()))
        rr=np.asarray(rnd); idx=ss.nlargest(k,"strength").idx.astype(int).to_numpy(); loss=A[:,idx].sum(axis=1)
        out.append({"pct_removed":pct,"k":k,"strength_severe50":float((loss>=.5).mean()),"random_mean":float(rr.mean()),"random_p025":float(np.quantile(rr,.025)),"random_p975":float(np.quantile(rr,.975))})
    return out


def multiplicity_diagnostics(x):
    g=x.copy(); g["key"] = g["id_compra"].astype("string")+"::"+g["orgao_cnpj"].astype(str)+"::"+g["fornecedor_id_limpo"].astype(str)
    cnt=g.groupby("key").agg(n_instrumentos=("id_contrato","nunique"),valor_soma=("valorInicial","sum"),valor_max=("valorInicial","max"),tipos=("tipo_contrato_norm",lambda s:" | ".join(sorted(set(map(str,s.dropna())))))).reset_index()
    repeated=cnt[cnt.n_instrumentos>1].copy()
    tipo=(x.groupby("tipo_contrato_norm").agg(instrumentos=("id_contrato","nunique"),valor=("valorInicial","sum")).reset_index())
    tipo["share_instrumentos"]=tipo.instrumentos/tipo.instrumentos.sum(); tipo["share_valor"]=tipo.valor/tipo.valor.sum(); tipo.to_csv(OUT/"distribuicao_tipo_contrato.csv",index=False,encoding="utf-8-sig")
    repeated.to_csv(OUT/"multiplicidade_compra_comprador_fornecedor.csv.gz",index=False,compression="gzip")
    return {"grupos_compra_comprador_fornecedor":int(len(cnt)),"grupos_com_multiplos_instrumentos":int(len(repeated)),"grupos_multiplos_pct":float(len(repeated)/max(len(cnt),1)*100),"instrumentos_em_grupos_multiplos":int(repeated.n_instrumentos.sum()),"valor_soma_grupos_multiplos":float(repeated.valor_soma.sum()),"valor_excesso_sobre_max_grupos_multiplos":float((repeated.valor_soma-repeated.valor_max).sum()),"tipos":tipo.to_dict(orient="records")}


def main():
    x=load(); mult=multiplicity_diagnostics(x)
    variants={k:prepare_variant(x,k) for k in ["todos","sem_empenho","colapsa_compra_fornecedor_max"]}
    calc={}
    elig={}
    for label,z in variants.items():
        rel,b,s=metrics(z); calc[label]=(rel,b,s); elig[label]=set(b[(b.n_fornecedores>=3)&(b.n_unidades>=5)].orgao_cnpj.astype(str))
    common=sorted(set.intersection(*elig.values()))
    desc=[]; sims=[]; size=[]
    for label,z in variants.items():
        rel,b,s=calc[label]; desc.append(description(b,common,label)); size.append({"spec":label,"linhas_instrumentais":len(z),"valor_total":float(z.valorInicial.sum()),"compradores_elegiveis_proprios":len(elig[label])})
        for row in simulate(rel,s,common):row["spec"]=label;sims.append(row)
    pd.DataFrame(desc).to_csv(OUT/"comparacao_metricas_amostra_comum.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame(sims).to_csv(OUT/"comparacao_simulacoes_strength.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame(size).to_csv(OUT/"tamanho_variantes.csv",index=False,encoding="utf-8-sig")
    summary={"instrumentos_base":len(x),"multiplicidade":mult,"variantes":size,"compradores_amostra_comum":len(common),"metricas":desc,"simulacoes":sims,"interpretacao":"A especificação colapsada é limite inferior conservador e não substitui a interpretação jurídica/econômica de instrumentos múltiplos. Se os padrões persistirem nas três variantes, a conclusão não depende criticamente da inclusão de empenhos ou da soma de múltiplos instrumentos por compra-fornecedor."}
    (OUT/"resumo_robustez_instrumentos.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
