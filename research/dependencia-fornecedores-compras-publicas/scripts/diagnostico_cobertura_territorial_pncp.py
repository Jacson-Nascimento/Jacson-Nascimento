#!/usr/bin/env python3
"""Diagnóstico de presença territorial do PNCP contra o universo municipal estrito do IBGE.

O endpoint de localidades do IBGE inclui, para fins estatísticos, o Distrito Federal
e o Distrito Estadual de Fernando de Noronha. Como a amostra principal é Executivo
municipal, ambos são excluídos do denominador. Em 2025, o universo estrito é de
5.569 municípios. Ausência mensal não é tratada como falha de reporte.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import requests
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"processed"/"pncp_mensal"
RES=ROOT/"results"
IBGE_URL="https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
EXCLUIR_NAO_MUNICIPIOS={"5300108","2605459"}  # Distrito Federal e Distrito Estadual de Fernando de Noronha

def clean_code(s):
 return s.astype("string").str.replace(r"\D","",regex=True).str.zfill(7)

def fetch_ibge():
 r=requests.get(IBGE_URL,timeout=120,headers={"User-Agent":"Pesquisa-Academica-PNCP-Cobertura/1.0"}); r.raise_for_status(); rows=r.json(); out=[]
 for x in rows:
  mic=x.get("microrregiao") or {}; meso=mic.get("mesorregiao") or {}; uf=meso.get("UF") or {}; reg=uf.get("regiao") or {}
  out.append({"municipio_ibge":str(x.get("id","")),"municipio_ibge_nome":x.get("nome"),"uf":uf.get("sigla"),"uf_nome":uf.get("nome"),"regiao":reg.get("nome")})
 d=pd.DataFrame(out); d["municipio_ibge"]=clean_code(d["municipio_ibge"]); return d.drop_duplicates("municipio_ibge")

def main():
 p=argparse.ArgumentParser(); p.add_argument("--month",type=int,required=True,choices=range(1,13)); a=p.parse_args(); mf=a.month
 out=RES/f"cobertura_territorial_pncp_2025_{mf:02d}"; out.mkdir(parents=True,exist_ok=True)
 ibge_api=fetch_ibge(); ibge_api.to_csv(out/"universo_localidades_ibge_api_snapshot.csv",index=False,encoding="utf-8-sig")
 ibge=ibge_api[~ibge_api.municipio_ibge.isin(EXCLUIR_NAO_MUNICIPIOS)].copy(); ibge.to_csv(out/"universo_municipios_estritos_ibge.csv",index=False,encoding="utf-8-sig")
 universe=set(ibge.municipio_ibge.dropna().astype(str)); frames=[]; monthly=[]
 for m in range(1,mf+1):
  path=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
  if not path.exists():raise FileNotFoundError(path)
  d=pd.read_csv(path,dtype={"municipio_ibge":"string","orgao_cnpj":"string"},low_memory=False); d["municipio_ibge"]=clean_code(d["municipio_ibge"]); d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce"); d["mes_publicacao_ref"]=m
  s=d[d.ano_assinatura.eq(2025)].copy(); frames.append(s); mun=set(s.municipio_ibge.dropna().astype(str)); valid=mun&universe; outside=mun-universe
  monthly.append({"mes":m,"instrumentos_pj_assinados_2025":int(len(s)),"compradores_unicos":int(s.orgao_cnpj.nunique()),"municipios_observados":len(mun),"municipios_validos_ibge":len(valid),"municipios_fora_universo_municipal":len(outside),"presenca_universo_pct":len(valid)/len(universe)*100})
 allx=pd.concat(frames,ignore_index=True); allx["municipio_ibge"]=clean_code(allx["municipio_ibge"]); observed=set(allx.municipio_ibge.dropna().astype(str)); outside_obs=observed-universe
 pm=(allx[allx.municipio_ibge.isin(universe)].groupby(["municipio_ibge","mes_publicacao_ref"]).agg(instrumentos=("id_contrato","nunique"),compradores=("orgao_cnpj","nunique")).reset_index())
 cont=(pm.groupby("municipio_ibge").agg(meses_observados=("mes_publicacao_ref","nunique"),primeiro_mes=("mes_publicacao_ref","min"),ultimo_mes=("mes_publicacao_ref","max"),instrumentos=("instrumentos","sum"),compradores_mes_soma=("compradores","sum")).reset_index())
 cont=ibge.merge(cont,on="municipio_ibge",how="left")
 for c in ["meses_observados","instrumentos","compradores_mes_soma"]:cont[c]=cont[c].fillna(0).astype(int)
 cont.to_csv(out/"presenca_observacional_municipios.csv",index=False,encoding="utf-8-sig")
 seen=cont[cont.meses_observados.gt(0)]; den=ibge.groupby(["uf","regiao"],dropna=False).size().rename("municipios_universo").reset_index(); num=seen.groupby(["uf","regiao"],dropna=False).size().rename("municipios_observados").reset_index(); uf=den.merge(num,on=["uf","regiao"],how="left"); uf["municipios_observados"]=uf.municipios_observados.fillna(0).astype(int); uf["presenca_pct"]=uf.municipios_observados/uf.municipios_universo*100; uf.to_csv(out/"presenca_por_uf.csv",index=False,encoding="utf-8-sig")
 dist=cont.groupby("meses_observados").size().rename("municipios").reset_index(); dist["pct_universo"]=dist.municipios/len(ibge)*100; dist.to_csv(out/"distribuicao_meses_observados.csv",index=False,encoding="utf-8-sig"); pd.DataFrame(monthly).to_csv(out/"presenca_por_mes.csv",index=False,encoding="utf-8-sig")
 entrants=cont[cont.meses_observados.gt(0)].groupby("primeiro_mes").size().rename("novos_municipios_observados").reset_index(); entrants.to_csv(out/"primeira_aparicao_por_mes.csv",index=False,encoding="utf-8-sig")
 n=len(ibge); obs=cont.meses_observados
 summary={"mes_final_publicacao":f"2025-{mf:02d}","registros_endpoint_localidades_ibge":int(len(ibge_api)),"unidades_estatisticas_excluidas":["5300108 - Distrito Federal","2605459 - Distrito Estadual de Fernando de Noronha"],"universo_ibge_municipios_estritos":int(n),"municipios_observados_ao_menos_1_mes":int((obs>=1).sum()),"presenca_universo_ao_menos_1_mes_pct":float((obs>=1).sum()/n*100),"municipios_observados_ao_menos_metade_meses":int((obs>=((mf+1)//2)).sum()),"municipios_observados_todos_meses":int((obs==mf).sum()),"pct_observados_todos_meses_universo":float((obs==mf).sum()/n*100),"mediana_meses_observados_entre_municipios_presentes":None if not (obs>0).any() else float(obs[obs>0].median()),"codigos_pncp_fora_universo_municipal_estrito":sorted(outside_obs),"n_codigos_pncp_fora_universo_municipal_estrito":len(outside_obs),"instrumentos_pj_assinados_2025_acumulados":int(len(allx)),"compradores_institucionais_acumulados":int(allx.orgao_cnpj.nunique()),"nota_metodologica":"Presença mensal no PNCP não equivale a completude de reporte. Município sem instrumento em um mês pode simplesmente não ter contratação publicada. O indicador mede presença/continuidade observacional.","fonte_universo":IBGE_URL}
 if n!=5569: raise RuntimeError(f"Universo municipal estrito inesperado: {n}, esperado 5569")
 (out/"resumo_cobertura_territorial.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
