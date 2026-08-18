#!/usr/bin/env python3
"""Diagnóstico agregado das datas de publicação nas partições PNCP de janeiro de 2025.

Lê somente a base pública PJ já versionada. Não grava identificadores individuais.
Também compara o parsing separado por partição com o parsing da série concatenada,
para detectar falha de inferência de formatos datetime mistos.
"""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
OUT = ROOT / "results" / "diagnostico_datas_janeiro_2025"
OUT.mkdir(parents=True, exist_ok=True)

PARTS = [
    ("2025-01-d01-d08", "2025-01-01", "2025-01-08"),
    ("2025-01-d09-d16", "2025-01-09", "2025-01-16"),
    ("2025-01-d17-d24", "2025-01-17", "2025-01-24"),
    ("2025-01-d25-d31", "2025-01-25", "2025-01-31"),
]


def main():
    rows=[]
    month_rows=[]
    year_rows=[]
    total_out_jan=0
    total_out_part=0
    total=0
    raw_parts=[]

    for label, start_s, end_s in PARTS:
        path=DATA/f"pncp_{label}_municipal_pj.csv.gz"
        d=pd.read_csv(path, usecols=["data_publicacao"], low_memory=False)
        d["particao"]=label
        raw_parts.append(d.copy())
        dt=pd.to_datetime(d["data_publicacao"], errors="coerce")
        start=pd.Timestamp(start_s)
        end=pd.Timestamp(end_s)+pd.Timedelta(days=1)-pd.Timedelta(microseconds=1)
        jan_start=pd.Timestamp("2025-01-01")
        jan_end=pd.Timestamp("2025-02-01")-pd.Timedelta(microseconds=1)
        valid=dt.notna()
        in_part=dt.between(start,end,inclusive="both")
        in_jan=dt.between(jan_start,jan_end,inclusive="both")
        n=len(d)
        out_part=int((valid & ~in_part).sum())
        out_jan=int((valid & ~in_jan).sum())
        total += n
        total_out_part += out_part
        total_out_jan += out_jan
        rows.append({
            "particao":label,
            "intervalo_inicio":start_s,
            "intervalo_fim":end_s,
            "linhas":n,
            "datas_validas":int(valid.sum()),
            "data_min":dt.min().isoformat() if pd.notna(dt.min()) else None,
            "data_max":dt.max().isoformat() if pd.notna(dt.max()) else None,
            "dentro_intervalo_n":int((valid & in_part).sum()),
            "fora_intervalo_n":out_part,
            "fora_intervalo_pct":round(out_part/max(int(valid.sum()),1)*100,4),
            "fora_janeiro_n":out_jan,
            "fora_janeiro_pct":round(out_jan/max(int(valid.sum()),1)*100,4),
            "antes_intervalo_n":int((valid & (dt<start)).sum()),
            "depois_intervalo_n":int((valid & (dt>end)).sum()),
            "antes_janeiro_n":int((valid & (dt<jan_start)).sum()),
            "depois_janeiro_n":int((valid & (dt>jan_end)).sum()),
        })
        ym=dt.dropna().dt.to_period("M").astype(str).value_counts().rename_axis("ano_mes").reset_index(name="n")
        ym.insert(0,"particao",label)
        month_rows.append(ym)
        yy=dt.dropna().dt.year.value_counts().sort_index().rename_axis("ano").reset_index(name="n")
        yy.insert(0,"particao",label)
        year_rows.append(yy)

    concat=pd.concat(raw_parts,ignore_index=True)
    global_default=pd.to_datetime(concat["data_publicacao"],errors="coerce")
    global_mixed=pd.to_datetime(concat["data_publicacao"],errors="coerce",format="mixed")
    parse_rows=[]
    for label,g in concat.assign(_default=global_default,_mixed=global_mixed).groupby("particao"):
        parse_rows.append({
            "particao":label,
            "linhas":len(g),
            "nat_parsing_global_padrao":int(g["_default"].isna().sum()),
            "nat_parsing_global_mixed":int(g["_mixed"].isna().sum()),
        })
    parse_df=pd.DataFrame(parse_rows)
    parse_df.to_csv(OUT/"comparacao_parsing_global.csv",index=False,encoding="utf-8-sig")

    detail=pd.DataFrame(rows)
    detail.to_csv(OUT/"resumo_por_particao.csv",index=False,encoding="utf-8-sig")
    pd.concat(month_rows,ignore_index=True).to_csv(OUT/"distribuicao_ano_mes.csv",index=False,encoding="utf-8-sig")
    pd.concat(year_rows,ignore_index=True).to_csv(OUT/"distribuicao_ano.csv",index=False,encoding="utf-8-sig")
    summary={
        "linhas_pj_total":total,
        "fora_intervalo_particao_total":total_out_part,
        "fora_janeiro_total":total_out_jan,
        "nat_parsing_global_padrao":int(global_default.isna().sum()),
        "nat_parsing_global_mixed":int(global_mixed.isna().sum()),
        "observacao":"Diagnóstico agregado do campo data_publicacao derivado de dataPublicacaoPncp. Não altera nem exclui registros.",
    }
    (OUT/"resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(detail.to_string(index=False))
    print('--- PARSING GLOBAL ---')
    print(parse_df.to_string(index=False))
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
