#!/usr/bin/env python3
"""Robustez a compras compartilhadas/origem externa, jan-fev 2025.

Compara a rede completa observada com uma rede que exclui instrumentos em que o
CNPJ da contratação de origem difere do CNPJ do órgão do instrumento
(`origem_externa=True`). Para comparabilidade, a análise principal usa somente
compradores que satisfazem >=3 fornecedores e >=5 instrumentos nas DUAS redes.

As simulações usam ranking global de fornecedores em cada rede e 1.000 remoções
aleatórias, semente fixa.
"""
from pathlib import Path
import json, math
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"processed"/"pncp_mensal"
RES=ROOT/"results"
OUT=RES/"robustez_compras_compartilhadas_jan_fev_2025"
OUT.mkdir(parents=True,exist_ok=True)
SEED=20260818; DRAWS=1000


def boolish(s):
    return s.astype("string").str.lower().isin(["true","1","sim"])


def load():
    frames=[]
    for m in [1,2]:
        p=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        d=pd.read_csv(p,dtype={"orgao_cnpj":"string","fornecedor_id_limpo":"string"},low_memory=False)
        d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce")
        d["valorInicial"]=pd.to_numeric(d["valorInicial"],errors="coerce")
        d["origem_externa_bool"]=boolish(d["origem_externa"])
        frames.append(d)
    x=pd.concat(frames,ignore_index=True)
    return x[x["ano_assinatura"].eq(2025)&x["valorInicial"].gt(0)].copy()


def metrics(x):
    rel=x.groupby(["orgao_cnpj","fornecedor_id_limpo"]).agg(valor=("valorInicial","sum"),n=("id_contrato","nunique")).reset_index()
    rel["share"]=rel["valor"]/rel.groupby("orgao_cnpj")["valor"].transform("sum")
    rel["share_n"]=rel["n"]/rel.groupby("orgao_cnpj")["n"].transform("sum")
    rows=[]
    for b,g in rel.groupby("orgao_cnpj"):
        sv=g["share"].sort_values(ascending=False); sn=g["share_n"].sort_values(ascending=False)
        h=float((sv**2).sum()); hc=float((sn**2).sum()); N=len(g)
        hn=(h-1/N)/(1-1/N) if N>1 else np.nan
        rows.append({"orgao_cnpj":b,"n_fornecedores":N,"n_instrumentos":int(g["n"].sum()),"valor_total":float(g["valor"].sum()),"hhi":h,"hhi_norm":hn,"count_hhi":hc,"cr1":float(sv.iloc[0]),"cr4":float(sv.iloc[:4].sum()),"neff":1/h})
    buyers=pd.DataFrame(rows)
    sup=rel.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"),strength=("valor","sum")).reset_index()
    sup["pct_strength"]=sup["strength"].rank(pct=True,method="average")
    z=rel.merge(sup[["fornecedor_id_limpo","pct_strength"]],on="fornecedor_id_limpo",how="left")
    z["piece"]=z["share"]*z["pct_strength"]
    exp=z.groupby("orgao_cnpj")["piece"].sum().rename("exposicao_strength").reset_index()
    buyers=buyers.merge(exp,on="orgao_cnpj",how="left")
    return rel,buyers,sup


def simulate(rel, eligible_ids):
    r=rel.copy(); r["orgao_cnpj"]=r["orgao_cnpj"].astype(str); r["fornecedor_id_limpo"]=r["fornecedor_id_limpo"].astype(str)
    bids=sorted(set(map(str,eligible_ids))); slist=sorted(r["fornecedor_id_limpo"].unique())
    bi={v:i for i,v in enumerate(bids)}; si={v:i for i,v in enumerate(slist)}
    A=np.zeros((len(bids),len(slist)),dtype=np.float32)
    for row in r[r["orgao_cnpj"].isin(bids)].itertuples(index=False): A[bi[row.orgao_cnpj],si[row.fornecedor_id_limpo]]+=float(row.share)
    sup=r.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"),strength=("valor","sum")).reset_index(); sup["idx"]=sup["fornecedor_id_limpo"].map(si)
    rng=np.random.default_rng(SEED); rows=[]
    for pct in [.01,.05,.10]:
        k=max(1,int(math.ceil(len(slist)*pct))); rnd=[]
        for _ in range(DRAWS):
            idx=rng.choice(len(slist),size=k,replace=False); loss=A[:,idx].sum(axis=1); rnd.append(float((loss>=.5).mean()))
        rr=np.asarray(rnd)
        for strategy in ["degree","strength"]:
            idx=sup.nlargest(k,strategy)["idx"].astype(int).to_numpy(); loss=A[:,idx].sum(axis=1)
            rows.append({"pct_removed":pct,"k":k,"strategy":strategy,"target_severe":float((loss>=.5).mean()),"random_mean":float(rr.mean()),"random_p025":float(np.quantile(rr,.025)),"random_p975":float(np.quantile(rr,.975))})
    return pd.DataFrame(rows)


def describe(b, ids, label):
    g=b[b["orgao_cnpj"].astype(str).isin(ids)].copy(); qh=g["hhi"].quantile(.75); qe=g["exposicao_strength"].quantile(.75)
    rho,p=spearmanr(g["hhi_norm"],g["exposicao_strength"],nan_policy="omit")
    return {"rede":label,"n":len(g),"hhi_mediana":float(g["hhi"].median()),"hhi_norm_mediana":float(g["hhi_norm"].median()),"count_hhi_mediana":float(g["count_hhi"].median()),"cr1_mediana":float(g["cr1"].median()),"cr4_mediana":float(g["cr4"].median()),"neff_mediana":float(g["neff"].median()),"hhi_maior_count_pct":float((g["hhi"]>g["count_hhi"]).mean()*100),"hidden_exposure_pct":float(((g["hhi"]<qh)&(g["exposicao_strength"]>=qe)).mean()*100),"rho_hhi_norm_exposure":float(rho),"p_rho":float(p)}


def main():
    x=load(); internal=x[~x["origem_externa_bool"]].copy()
    rel_all,b_all,sup_all=metrics(x); rel_int,b_int,sup_int=metrics(internal)
    elig_all=set(b_all[(b_all.n_fornecedores>=3)&(b_all.n_instrumentos>=5)].orgao_cnpj.astype(str))
    elig_int=set(b_int[(b_int.n_fornecedores>=3)&(b_int.n_instrumentos>=5)].orgao_cnpj.astype(str))
    common=sorted(elig_all&elig_int)
    if len(common)<50: raise RuntimeError(f"Amostra comum muito pequena: {len(common)}")
    desc=pd.DataFrame([describe(b_all,common,"todos"),describe(b_int,common,"sem_origem_externa")])
    desc.to_csv(OUT/"comparacao_metricas_amostra_comum.csv",index=False,encoding="utf-8-sig")
    sa=simulate(rel_all,common); sa["rede"]="todos"; sb=simulate(rel_int,common); sb["rede"]="sem_origem_externa"; sims=pd.concat([sa,sb],ignore_index=True)
    sims.to_csv(OUT/"comparacao_simulacoes.csv",index=False,encoding="utf-8-sig")
    share_instr=float(x["origem_externa_bool"].mean()); share_val=float(x.loc[x.origem_externa_bool,"valorInicial"].sum()/x["valorInicial"].sum())
    summary={"instrumentos_analiticos":len(x),"origem_externa_instrumentos_pct":share_instr*100,"origem_externa_valor_pct":share_val*100,"elegiveis_todos":len(elig_all),"elegiveis_sem_externa":len(elig_int),"amostra_comum":len(common),"metricas":desc.to_dict(orient="records"),"simulacoes_limiar_50pct":sims.to_dict(orient="records"),"regra":"Se a divergência valor-frequência e a superioridade do choque direcionado persistirem sem origem externa, o resultado não é explicado apenas por compras compartilhadas."}
    (OUT/"resumo_robustez_compras_compartilhadas.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
