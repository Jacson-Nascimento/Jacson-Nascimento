#!/usr/bin/env python3
"""Decompõe a mudança de concentração entre jan-fev e jan-mar/2025.

Para compradores elegíveis em ambas as janelas, separa a variação exata do HHI
bruto em dois componentes sequenciais:

1. reponderação dos fornecedores já observados em jan-fev, usando seus valores
   acumulados até março e renormalizando apenas o conjunto antigo;
2. entrada/diluição de fornecedores que aparecem pela primeira vez em março.

Delta total = efeito de reponderação + efeito de entrada.

A ordem da decomposição é explícita; não é decomposição causal. Também mede a
participação dos entrantes no valor acumulado e no fluxo incremental de março.
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
OUT=RES/"decomposicao_hhi_jan_mar_2025"
OUT.mkdir(parents=True,exist_ok=True)


def load_month(m):
    p=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
    d=pd.read_csv(p,dtype={"id_contrato":"string","orgao_cnpj":"string","fornecedor_id_limpo":"string"},low_memory=False)
    d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce")
    d["valorInicial"]=pd.to_numeric(d["valorInicial"],errors="coerce")
    return d[d.ano_assinatura.eq(2025)&d.valorInicial.gt(0)].copy()


def relations(x):
    r=x.groupby(["orgao_cnpj","fornecedor_id_limpo"],dropna=False).valorInicial.sum().rename("valor").reset_index()
    r["share"]=r.valor/r.groupby("orgao_cnpj").valor.transform("sum")
    return r


def hhi_norm(h,n):
    if n<=1:return np.nan
    floor=1/n
    return (h-floor)/(1-floor)


def corr(a,b):
    z=pd.DataFrame({"a":a,"b":b}).replace([np.inf,-np.inf],np.nan).dropna()
    if len(z)<3:return {"rho":None,"p":None,"n":int(len(z))}
    r,p=spearmanr(z.a,z.b);return {"rho":float(r),"p":float(p),"n":int(len(z))}


def main():
    m1,m2,m3=[load_month(m) for m in [1,2,3]]
    jf=pd.concat([m1,m2],ignore_index=True)
    jm=pd.concat([m1,m2,m3],ignore_index=True)
    ra=relations(jf); rb=relations(jm); r3=relations(m3)

    ea=pd.read_csv(RES/"carteira_jan_fev_2025_diagnostico"/"compradores_elegiveis_jan_fev.csv",dtype={"orgao_cnpj":"string"},low_memory=False)
    eb=pd.read_csv(RES/"carteira_acumulada_2025_03_diagnostico"/"compradores_elegiveis.csv",dtype={"orgao_cnpj":"string"},low_memory=False)
    common=sorted(set(ea.orgao_cnpj.astype(str))&set(eb.orgao_cnpj.astype(str)))
    ra["orgao_cnpj"]=ra.orgao_cnpj.astype(str); rb["orgao_cnpj"]=rb.orgao_cnpj.astype(str); r3["orgao_cnpj"]=r3.orgao_cnpj.astype(str)
    ra["fornecedor_id_limpo"]=ra.fornecedor_id_limpo.astype(str);rb["fornecedor_id_limpo"]=rb.fornecedor_id_limpo.astype(str);r3["fornecedor_id_limpo"]=r3.fornecedor_id_limpo.astype(str)

    rows=[]
    for buyer in common:
        a=ra[ra.orgao_cnpj.eq(buyer)].copy(); b=rb[rb.orgao_cnpj.eq(buyer)].copy(); inc=r3[r3.orgao_cnpj.eq(buyer)].copy()
        old=set(a.fornecedor_id_limpo); new=set(b.fornecedor_id_limpo)-old
        h_old=float((a.share**2).sum()); h_new=float((b.share**2).sum())
        old_in_b=b[b.fornecedor_id_limpo.isin(old)].copy()
        old_total=float(old_in_b.valor.sum())
        if old_total>0:
            p=old_in_b.valor/old_total; h_reweighted=float((p**2).sum())
        else:h_reweighted=np.nan
        reweight=h_reweighted-h_old
        entry=h_new-h_reweighted
        total=h_new-h_old
        new_value=float(b.loc[b.fornecedor_id_limpo.isin(new),"valor"].sum())
        total_value=float(b.valor.sum())
        march_total=float(inc.valor.sum())
        march_new=float(inc.loc[inc.fornecedor_id_limpo.isin(new),"valor"].sum())
        rows.append({"orgao_cnpj":buyer,"n_fornecedores_jan_fev":len(old),"n_fornecedores_jan_mar":len(b),
            "n_entrantes_marco":len(new),"hhi_jan_fev":h_old,"hhi_jan_mar":h_new,"hhi_oldset_reponderado":h_reweighted,
            "hhi_norm_jan_fev":hhi_norm(h_old,len(old)),"hhi_norm_jan_mar":hhi_norm(h_new,len(b)),
            "delta_hhi":total,"efeito_reponderacao":reweight,"efeito_entrada":entry,
            "share_valor_entrantes_acumulado":new_value/total_value if total_value>0 else np.nan,
            "share_valor_entrantes_marco":march_new/march_total if march_total>0 else np.nan,
            "valor_marco_sobre_acumulado":march_total/total_value if total_value>0 else np.nan})
    d=pd.DataFrame(rows)
    d["erro_identidade"]=d.delta_hhi-(d.efeito_reponderacao+d.efeito_entrada)
    d.to_csv(OUT/"decomposicao_por_comprador.csv",index=False,encoding="utf-8-sig")

    groups=(d.assign(tem_entrante=d.n_entrantes_marco.gt(0)).groupby("tem_entrante").agg(
        n=("orgao_cnpj","size"),delta_hhi_mediana=("delta_hhi","median"),
        efeito_reponderacao_mediana=("efeito_reponderacao","median"),efeito_entrada_mediana=("efeito_entrada","median"),
        delta_hhi_norm_mediana=("hhi_norm_jan_mar",lambda s:np.nan)).reset_index())
    # delta norm explicitamente, sem truque de agregação.
    d["delta_hhi_norm"]=d.hhi_norm_jan_mar-d.hhi_norm_jan_fev
    groups=d.groupby(d.n_entrantes_marco.gt(0).rename("tem_entrante")).agg(
        n=("orgao_cnpj","size"),delta_hhi_mediana=("delta_hhi","median"),delta_hhi_norm_mediana=("delta_hhi_norm","median"),
        efeito_reponderacao_mediana=("efeito_reponderacao","median"),efeito_entrada_mediana=("efeito_entrada","median"),
        share_entrantes_acumulado_mediana=("share_valor_entrantes_acumulado","median"),share_entrantes_marco_mediana=("share_valor_entrantes_marco","median")).reset_index()
    groups.to_csv(OUT/"comparacao_com_sem_entrantes.csv",index=False,encoding="utf-8-sig")

    quant=d[["n_entrantes_marco","share_valor_entrantes_acumulado","share_valor_entrantes_marco","delta_hhi","delta_hhi_norm","efeito_reponderacao","efeito_entrada"]].describe(percentiles=[.1,.25,.5,.75,.9,.95]).T
    quant.to_csv(OUT/"distribuicoes_decomposicao.csv",encoding="utf-8-sig")

    summary={"compradores_comuns":int(len(d)),"identidade_max_erro_abs":float(d.erro_identidade.abs().max()),
        "compradores_com_novos_fornecedores":int(d.n_entrantes_marco.gt(0).sum()),
        "compradores_com_novos_fornecedores_pct":float(d.n_entrantes_marco.gt(0).mean()*100),
        "n_entrantes_mediana":float(d.n_entrantes_marco.median()),
        "share_valor_entrantes_acumulado_mediana":float(d.share_valor_entrantes_acumulado.median()),
        "share_valor_entrantes_marco_mediana":float(d.share_valor_entrantes_marco.median()),
        "delta_hhi_mediana":float(d.delta_hhi.median()),"delta_hhi_norm_mediana":float(d.delta_hhi_norm.median()),
        "efeito_reponderacao_mediana":float(d.efeito_reponderacao.median()),"efeito_entrada_mediana":float(d.efeito_entrada.median()),
        "entrada_reduz_hhi_pct":float(d.efeito_entrada.lt(0).mean()*100),"reponderacao_reduz_hhi_pct":float(d.efeito_reponderacao.lt(0).mean()*100),
        "correlacoes":{"share_entrantes_acumulado_vs_delta_hhi":corr(d.share_valor_entrantes_acumulado,d.delta_hhi),
          "share_entrantes_marco_vs_delta_hhi":corr(d.share_valor_entrantes_marco,d.delta_hhi),
          "n_entrantes_vs_delta_hhi_norm":corr(d.n_entrantes_marco,d.delta_hhi_norm),
          "share_entrantes_vs_efeito_entrada":corr(d.share_valor_entrantes_acumulado,d.efeito_entrada)},
        "grupos":groups.to_dict(orient="records"),
        "interpretacao":"Decomposição sequencial descritiva: primeiro repondera fornecedores antigos; depois adiciona entrantes. A soma dos componentes reproduz exatamente o delta do HHI bruto, mas os componentes não têm interpretação causal."}
    (OUT/"resumo_decomposicao.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
