#!/usr/bin/env python3
"""Prepara a amostra territorial PNCP para integração SICONFI/DCA 2025.

Usa os compradores elegíveis do diagnóstico acumulado janeiro-fevereiro e
mapeia cada CNPJ comprador aos códigos municipais observados nos instrumentos
assinados em 2025. A integração fiscal principal mantém apenas compradores com
um único código IBGE observado nessa coorte; casos multi-município são
preservados em arquivo separado para análise de sensibilidade.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results"
OUT = RES / "siconfi_integracao_jan_fev_2025"
OUT.mkdir(parents=True, exist_ok=True)

ELIG = RES / "carteira_jan_fev_2025_diagnostico" / "compradores_elegiveis_jan_fev.csv"
MONTHS = [
    DATA / "pncp_2025-01_publicacoes_municipal_pj.csv.gz",
    DATA / "pncp_2025-02_publicacoes_municipal_pj.csv.gz",
]


def main():
    eligible = pd.read_csv(ELIG, dtype={"orgao_cnpj":"string"})
    ids = set(eligible["orgao_cnpj"].dropna().astype(str))

    frames=[]
    for p in MONTHS:
        d=pd.read_csv(p,dtype={"orgao_cnpj":"string","municipio_ibge":"string"},low_memory=False)
        d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce")
        d=d[d["ano_assinatura"].eq(2025) & d["orgao_cnpj"].astype(str).isin(ids)].copy()
        frames.append(d[["orgao_cnpj","municipio_ibge","municipio","uf","id_contrato"]])
    x=pd.concat(frames,ignore_index=True)
    x=x.dropna(subset=["orgao_cnpj","municipio_ibge"])
    x["municipio_ibge"]=x["municipio_ibge"].astype("string").str.replace(r"\.0$","",regex=True).str.zfill(7)

    mapping=(x.groupby("orgao_cnpj")
        .agg(n_municipios=("municipio_ibge","nunique"),
             n_instrumentos_mapeados=("id_contrato","nunique"))
        .reset_index())
    first=(x.sort_values(["orgao_cnpj","municipio_ibge"])
        .drop_duplicates("orgao_cnpj")[["orgao_cnpj","municipio_ibge","municipio","uf"]])
    mapping=mapping.merge(first,on="orgao_cnpj",how="left")
    mapping=mapping.merge(eligible,on="orgao_cnpj",how="left",suffixes=("","_metricas"))
    mapping["integracao_siconfi_principal"]=mapping["n_municipios"].eq(1)

    principal=mapping[mapping["integracao_siconfi_principal"]].copy()
    multi=mapping[~mapping["integracao_siconfi_principal"]].copy()

    # Lista municipal única para o coletor SICONFI.
    municipios=(principal[["municipio_ibge","municipio","uf"]]
        .drop_duplicates("municipio_ibge")
        .sort_values("municipio_ibge"))

    mapping.to_csv(OUT/"mapeamento_comprador_municipio.csv",index=False,encoding="utf-8-sig")
    principal.to_csv(OUT/"compradores_integracao_principal.csv",index=False,encoding="utf-8-sig")
    multi.to_csv(OUT/"compradores_multimunicipio.csv",index=False,encoding="utf-8-sig")
    municipios.to_csv(OUT/"municipios_siconfi.csv",index=False,encoding="utf-8-sig")

    summary={
        "compradores_elegiveis_entrada":int(len(eligible)),
        "compradores_mapeados":int(mapping["municipio_ibge"].notna().sum()),
        "compradores_unico_municipio":int(len(principal)),
        "compradores_multi_municipio":int(len(multi)),
        "municipios_unicos_para_siconfi":int(municipios["municipio_ibge"].nunique()),
        "regra":"Integração fiscal principal requer exatamente um municipio_ibge observado por CNPJ comprador na coorte PNCP assinada em 2025.",
    }
    (OUT/"resumo_mapeamento.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
