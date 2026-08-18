#!/usr/bin/env python3
"""Criticidade de fornecedor único na rede municipal PNCP jan-mar/2025.

Mede diretamente o impacto da remoção de cada fornecedor, sem índice composto:
- número/proporção de compradores elegíveis que perderiam >=25%, >=50%, >=75%;
- perda média de participação da carteira se o fornecedor fosse removido;
- degree e strength na rede global;
- comparação entre fornecedores por Strength e distribuição de impactos.

A análise é estrutural e contrafactual mecânica, não previsão de inadimplência ou
falha real de fornecedor. Resultados são condicionais à coorte publicada até março.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"processed"/"pncp_mensal"
RES=ROOT/"results"
OUT=RES/"criticidade_fornecedor_jan_mar_2025"
OUT.mkdir(parents=True,exist_ok=True)


def load():
    frames=[]
    for m in [1,2,3]:
        p=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        d=pd.read_csv(p,dtype={"id_contrato":"string","orgao_cnpj":"string","fornecedor_id_limpo":"string"},low_memory=False)
        d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce")
        d["valorInicial"]=pd.to_numeric(d["valorInicial"],errors="coerce")
        frames.append(d)
    x=pd.concat(frames,ignore_index=True)
    return x[x.ano_assinatura.eq(2025)&x.valorInicial.gt(0)].copy()


def corr(a,b):
    z=pd.DataFrame({"a":a,"b":b}).replace([np.inf,-np.inf],np.nan).dropna()
    if len(z)<3:return {"rho":None,"p":None,"n":int(len(z))}
    r,p=spearmanr(z.a,z.b); return {"rho":float(r),"p":float(p),"n":int(len(z))}


def main():
    x=load()
    rel=(x.groupby(["orgao_cnpj","fornecedor_id_limpo"],dropna=False)
         .agg(valor_relacao=("valorInicial","sum"),n_instrumentos=("id_contrato","nunique")).reset_index())
    rel["valor_total_comprador"]=rel.groupby("orgao_cnpj").valor_relacao.transform("sum")
    rel["share_valor"]=rel.valor_relacao/rel.valor_total_comprador

    buyers=(rel.groupby("orgao_cnpj").agg(n_fornecedores=("fornecedor_id_limpo","nunique"),n_instrumentos=("n_instrumentos","sum")).reset_index())
    eligible=set(buyers[(buyers.n_fornecedores>=3)&(buyers.n_instrumentos>=5)].orgao_cnpj.astype(str))
    rel["orgao_cnpj"]=rel.orgao_cnpj.astype(str); rel["fornecedor_id_limpo"]=rel.fornecedor_id_limpo.astype(str)
    er=rel[rel.orgao_cnpj.isin(eligible)].copy()

    global_sup=(rel.groupby("fornecedor_id_limpo").agg(
        degree_global=("orgao_cnpj","nunique"),strength_global=("valor_relacao","sum")).reset_index())
    eligible_sup=(er.groupby("fornecedor_id_limpo").agg(
        degree_elegivel=("orgao_cnpj","nunique"),strength_elegivel=("valor_relacao","sum"),
        perda_media_soma=("share_valor","sum"),
        compradores_perda_25=("share_valor",lambda s:int((s>=.25).sum())),
        compradores_perda_50=("share_valor",lambda s:int((s>=.50).sum())),
        compradores_perda_75=("share_valor",lambda s:int((s>=.75).sum())),
        maior_share_comprador=("share_valor","max"),mediana_share_comprador=("share_valor","median")
    ).reset_index())
    s=global_sup.merge(eligible_sup,on="fornecedor_id_limpo",how="left")
    for c in ["degree_elegivel","strength_elegivel","perda_media_soma","compradores_perda_25","compradores_perda_50","compradores_perda_75"]:
        s[c]=s[c].fillna(0)
    n=len(eligible)
    s["perda_media_todos_compradores"]=s.perda_media_soma/max(n,1)
    for t in [25,50,75]:s[f"share_compradores_perda_{t}"]=s[f"compradores_perda_{t}"]/max(n,1)
    s["pct_degree_global"]=s.degree_global.rank(pct=True,method="average")
    s["pct_strength_global"]=s.strength_global.rank(pct=True,method="average")
    s=s.sort_values(["compradores_perda_50","strength_global"],ascending=[False,False])
    s.to_csv(OUT/"criticidade_fornecedores.csv",index=False,encoding="utf-8-sig")

    # Distribuição exata dos choques de nó único: cada fornecedor é um cenário.
    distribution=s[["fornecedor_id_limpo","degree_global","strength_global","perda_media_todos_compradores",
                    "share_compradores_perda_25","share_compradores_perda_50","share_compradores_perda_75"]].copy()
    distribution.to_csv(OUT/"distribuicao_choque_fornecedor_unico.csv",index=False,encoding="utf-8-sig")

    # Quantos fornecedores são críticos para pelo menos k compradores no limiar 50%.
    critical_counts=[]
    for k in [1,2,3,5,10,20]:
        critical_counts.append({"min_compradores_perda_50":k,"n_fornecedores":int((s.compradores_perda_50>=k).sum()),
                                "share_fornecedores_pct":float((s.compradores_perda_50>=k).mean()*100)})
    pd.DataFrame(critical_counts).to_csv(OUT/"contagem_fornecedores_criticos.csv",index=False,encoding="utf-8-sig")

    # Top Strength sem nomes no resumo; arquivo detalhado mantém IDs públicos para replicação.
    top_strength=s.nlargest(max(1,int(np.ceil(len(s)*.01))),"strength_global")
    top_degree=s.nlargest(max(1,int(np.ceil(len(s)*.01))),"degree_global")

    max50=int(s.compradores_perda_50.max()) if len(s) else 0
    max25=int(s.compradores_perda_25.max()) if len(s) else 0
    max75=int(s.compradores_perda_75.max()) if len(s) else 0
    summary={
        "mes_final_publicacao":"2025-03",
        "compradores_elegiveis":n,
        "fornecedores_rede_global":int(len(s)),
        "fornecedores_criticos_ao_menos_um_comprador_50pct":int((s.compradores_perda_50>=1).sum()),
        "fornecedores_criticos_ao_menos_cinco_compradores_50pct":int((s.compradores_perda_50>=5).sum()),
        "max_compradores_afetados_por_um_fornecedor":{"perda_25pct":max25,"perda_50pct":max50,"perda_75pct":max75,
            "share_50pct":float(max50/max(n,1))},
        "choque_fornecedor_unico_distribuicao":{
            "share_severos_50_mediana":float(s.share_compradores_perda_50.median()),
            "share_severos_50_p95":float(s.share_compradores_perda_50.quantile(.95)),
            "share_severos_50_p99":float(s.share_compradores_perda_50.quantile(.99)),
            "perda_media_mediana":float(s.perda_media_todos_compradores.median()),
            "perda_media_p99":float(s.perda_media_todos_compradores.quantile(.99))},
        "top_1pct_strength":{
            "n":int(len(top_strength)),
            "compradores_perda_50_soma_nao_unicos":int(top_strength.compradores_perda_50.sum()),
            "mediana_compradores_perda_50":float(top_strength.compradores_perda_50.median()),
            "max_compradores_perda_50":int(top_strength.compradores_perda_50.max())},
        "top_1pct_degree":{
            "n":int(len(top_degree)),
            "mediana_compradores_perda_50":float(top_degree.compradores_perda_50.median()),
            "max_compradores_perda_50":int(top_degree.compradores_perda_50.max())},
        "correlacoes":{
            "degree_vs_compradores_perda_50":corr(s.degree_global,s.compradores_perda_50),
            "strength_vs_compradores_perda_50":corr(s.strength_global,s.compradores_perda_50),
            "degree_vs_perda_media":corr(s.degree_global,s.perda_media_todos_compradores),
            "strength_vs_perda_media":corr(s.strength_global,s.perda_media_todos_compradores)},
        "interpretacao":"Remoção de um único fornecedor é choque estrutural mecânico. Não implica probabilidade de falha, irregularidade ou risco de crédito do fornecedor. IDs detalhados são preservados apenas para replicação e triagem técnica."
    }
    (OUT/"resumo_criticidade.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
