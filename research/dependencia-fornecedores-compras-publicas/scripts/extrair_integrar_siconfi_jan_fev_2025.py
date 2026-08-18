#!/usr/bin/env python3
"""Extrai variáveis fiscais DCA 2025 e integra ao diagnóstico PNCP jan-fev.

O cruzamento é territorial: CNPJ comprador -> município único observado -> cod_ibge.
A razão entre valor contratado observado e despesa empenhada é apenas medida de
escala/consistência; não é identidade contábil, pois contratos podem ser
plurianuais e valor contratado difere de execução orçamentária.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"results"
OUT=RES/"siconfi_integracao_jan_fev_2025"
RAW=OUT/"coleta"/"siconfi_dca_2025.csv.gz"
MAP=OUT/"compradores_integracao_principal.csv"


def num(s):
    return pd.to_numeric(s,errors="coerce")


def corr(df,a,b):
    z=df[[a,b]].replace([np.inf,-np.inf],np.nan).dropna()
    if len(z)<3: return {"rho":None,"p":None,"n":len(z)}
    rho,p=spearmanr(z[a],z[b])
    return {"rho":float(rho),"p":float(p),"n":int(len(z))}


def main():
    d=pd.read_csv(RAW,dtype={"cod_ibge":"string","_municipio_consulta":"string"},low_memory=False)
    d["cod_ibge"]=d["cod_ibge"].astype("string").str.replace(r"\.0$","",regex=True).str.zfill(7)
    d["valor_num"]=num(d["valor"])
    d["populacao_num"]=num(d["populacao"])

    # DCA I-D: totais de despesa por estágio.
    idd=d[d["anexo"].astype(str).eq("DCA-Anexo I-D")].copy()
    total=idd[idd["cod_conta"].astype(str).eq("TotalDespesas")].copy()
    pivot=(total.pivot_table(index="cod_ibge",columns="coluna",values="valor_num",aggfunc="first")
        .reset_index())
    rename={
        "Despesas Empenhadas":"despesa_empenhada_2025",
        "Despesas Liquidadas":"despesa_liquidada_2025",
        "Despesas Pagas":"despesa_paga_2025",
    }
    pivot=pivot.rename(columns=rename)
    keep=["cod_ibge"]+[c for c in rename.values() if c in pivot.columns]
    fiscal=pivot[keep].copy()

    pop=(d.groupby("cod_ibge",dropna=False)["populacao_num"].max().rename("populacao_siconfi_2025").reset_index())
    fiscal=fiscal.merge(pop,on="cod_ibge",how="outer")

    # Diagnóstico de consistência interna entre estágios da despesa.
    for c in ["despesa_empenhada_2025","despesa_liquidada_2025","despesa_paga_2025"]:
        if c not in fiscal.columns: fiscal[c]=np.nan
    fiscal["liquidada_sobre_empenhada"]=fiscal["despesa_liquidada_2025"]/fiscal["despesa_empenhada_2025"]
    fiscal["paga_sobre_empenhada"]=fiscal["despesa_paga_2025"]/fiscal["despesa_empenhada_2025"]
    fiscal.to_csv(OUT/"variaveis_fiscais_municipais_2025.csv",index=False,encoding="utf-8-sig")

    buyers=pd.read_csv(MAP,dtype={"orgao_cnpj":"string","municipio_ibge":"string"},low_memory=False)
    buyers["municipio_ibge"]=buyers["municipio_ibge"].astype("string").str.replace(r"\.0$","",regex=True).str.zfill(7)
    x=buyers.merge(fiscal,left_on="municipio_ibge",right_on="cod_ibge",how="left",validate="many_to_one")
    x["valor_total"]=num(x["valor_total"])
    x["procurement_intensity_parcial"]=x["valor_total"]/x["despesa_empenhada_2025"]
    x["log_despesa_empenhada"]=np.log(x["despesa_empenhada_2025"].where(x["despesa_empenhada_2025"]>0))
    x["log_populacao_siconfi"]=np.log(x["populacao_siconfi_2025"].where(x["populacao_siconfi_2025"]>0))
    x.to_csv(OUT/"painel_compradores_pncp_siconfi_jan_fev.csv",index=False,encoding="utf-8-sig")

    coverage=int(x["despesa_empenhada_2025"].notna().sum())
    correlations={
        "hhi_vs_log_despesa":corr(x,"portfolio_hhi","log_despesa_empenhada"),
        "hhi_vs_log_populacao":corr(x,"portfolio_hhi","log_populacao_siconfi"),
        "hhi_vs_procurement_intensity_parcial":corr(x,"portfolio_hhi","procurement_intensity_parcial"),
        "exposicao_strength_vs_log_despesa":corr(x,"exposicao_strength","log_despesa_empenhada"),
        "exposicao_strength_vs_procurement_intensity_parcial":corr(x,"exposicao_strength","procurement_intensity_parcial"),
    }
    pd.DataFrame([
        {"variaveis":k,**v} for k,v in correlations.items()
    ]).to_csv(OUT/"correlacoes_fiscais_diagnosticas.csv",index=False,encoding="utf-8-sig")

    pi=x["procurement_intensity_parcial"].replace([np.inf,-np.inf],np.nan).dropna()
    resumo={
        "compradores_integracao_principal":int(len(x)),
        "compradores_com_despesa_empenhada":coverage,
        "cobertura_despesa_empenhada_pct":float(coverage/max(len(x),1)*100),
        "municipios_fiscais_com_total_despesa":int(fiscal["despesa_empenhada_2025"].notna().sum()),
        "procurement_intensity_parcial_mediana":None if pi.empty else float(pi.median()),
        "procurement_intensity_parcial_p95":None if pi.empty else float(pi.quantile(.95)),
        "procurement_intensity_parcial_max":None if pi.empty else float(pi.max()),
        "correlacoes_spearman":correlations,
        "nota":"ProcurementIntensity parcial usa somente contratos assinados em 2025 e publicados até fevereiro; serve para diagnóstico de escala, não execução orçamentária.",
    }
    (OUT/"resumo_integracao_fiscal.json").write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(resumo,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
