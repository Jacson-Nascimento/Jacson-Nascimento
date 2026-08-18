#!/usr/bin/env python3
"""Consolida partições de um mês de publicações PNCP de 2025.

Uso:
    python scripts/consolidar_mes_pncp_2025.py --month 4

O script:
- lê todas as partições `pncp_2025-MM-d*_municipal_pj.csv.gz`;
- valida unicidade de `id_contrato`;
- valida datas de publicação no intervalo semiaberto do mês;
- concatena sem deduplicação silenciosa;
- grava `pncp_2025-MM_publicacoes_municipal_pj.csv.gz`;
- produz manifesto e resumo mensal.

Não calcula HHI nem rede; essa responsabilidade pertence ao acumulador global.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"processed"/"pncp_mensal"
RES=ROOT/"results"


def sha256(path: Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return h.hexdigest()


def parse_mixed(s):
    try:return pd.to_datetime(s,errors="coerce",format="mixed")
    except TypeError:return pd.to_datetime(s,errors="coerce")


def load(path):
    d=pd.read_csv(path,dtype={"id_contrato":"string","orgao_cnpj":"string","fornecedor_id_limpo":"string","municipio_ibge":"string"},low_memory=False)
    d["data_publicacao"]=parse_mixed(d["data_publicacao"])
    d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce")
    d["lag_publicacao_dias"]=pd.to_numeric(d["lag_publicacao_dias"],errors="coerce")
    return d


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--month",type=int,required=True,choices=range(1,13)); args=ap.parse_args(); m=args.month
    ym=f"2025-{m:02d}"; out=RES/f"pncp_2025_{m:02d}_consolidacao"; out.mkdir(parents=True,exist_ok=True)
    paths=sorted(DATA.glob(f"pncp_{ym}-d*_municipal_pj.csv.gz"))
    if not paths:raise FileNotFoundError(f"Nenhuma partição encontrada para {ym}")
    frames=[]; manifest=[]; source_summaries=[]
    for p in paths:
        label=p.name.removeprefix("pncp_").removesuffix("_municipal_pj.csv.gz")
        d=load(p); d["particao"]=label; frames.append(d); manifest.append({"particao":label,"arquivo":str(p.relative_to(ROOT)),"linhas_pj":len(d),"sha256":sha256(p)})
        sp=RES/"pncp_mensal"/f"{label}_resumo.json"
        if sp.exists():source_summaries.append(json.loads(sp.read_text(encoding="utf-8")))
    x=pd.concat(frames,ignore_index=True)
    dup=x.duplicated("id_contrato",keep=False)
    if dup.any():
        x.loc[dup,["id_contrato","particao"]].to_csv(out/"duplicidades.csv",index=False,encoding="utf-8-sig")
        raise RuntimeError(f"IDs repetidos entre partições: {x.loc[dup,'id_contrato'].nunique()}")
    invalid=x.data_publicacao.isna()
    if invalid.any():raise RuntimeError(f"Datas de publicação não parseáveis: {int(invalid.sum())}")
    start=pd.Timestamp(2025,m,1); end=pd.Timestamp(2026,1,1) if m==12 else pd.Timestamp(2025,m+1,1)
    outside=~((x.data_publicacao>=start)&(x.data_publicacao<end))
    if outside.any():
        x.loc[outside,["id_contrato","data_publicacao","particao"]].to_csv(out/"fora_mes.csv",index=False,encoding="utf-8-sig")
        raise RuntimeError(f"Publicações fora do mês: {int(outside.sum())}")
    dest=DATA/f"pncp_{ym}_publicacoes_municipal_pj.csv.gz"
    x.drop(columns=["particao"]).to_csv(dest,index=False,compression="gzip",encoding="utf-8")
    pd.DataFrame(manifest).to_csv(out/"manifesto_particoes.csv",index=False,encoding="utf-8-sig")
    summary={"mes":ym,"particoes":len(paths),"registros_pj":int(len(x)),"instrumentos_unicos":int(x.id_contrato.nunique()),"duplicidades":0,"compradores_unicos":int(x.orgao_cnpj.nunique()),"fornecedores_pj_unicos":int(x.fornecedor_id_limpo.nunique()),"municipios_unicos":int(x.municipio_ibge.nunique()),"assinados_2025":int(x.ano_assinatura.eq(2025).sum()),"assinados_antes_2025":int(x.ano_assinatura.lt(2025).sum()),"lag_mediana":float(x.lag_publicacao_dias.median()),"lag_p90":float(x.lag_publicacao_dias.quantile(.90)),"lag_p95":float(x.lag_publicacao_dias.quantile(.95)),"lag_negativo_n":int((x.lag_publicacao_dias<0).sum()),"janela":{"min":x.data_publicacao.min().isoformat(),"max":x.data_publicacao.max().isoformat()},"sha256_base_mensal":sha256(dest)}
    if source_summaries:
        summary.update({"registros_brutos_particoes_soma":int(sum(s.get("registros_brutos",0) for s in source_summaries)),"registros_municipais_validos_todos_tipos_soma":int(sum(s.get("registros_municipais_validos",0) for s in source_summaries)),"registros_pf_soma":int(sum(s.get("registros_pf",0) for s in source_summaries)),"registros_pe_soma":int(sum(s.get("registros_pe",0) for s in source_summaries))})
    (out/"resumo_consolidacao.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
