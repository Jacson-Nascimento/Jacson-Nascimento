#!/usr/bin/env python3
"""Probe agregado para identificar quais campos de data acompanham o filtro dataInicial/dataFinal.

Não persiste registros identificados. Consulta apenas as primeiras páginas e salva
estatísticas agregadas por campo de data.
"""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import requests

URL = "https://pncp.gov.br/api/consulta/v1/contratos"
START = "20250101"
END = "20250108"
MAX_PAGES = 5
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "probe_datas_filtro"
OUT.mkdir(parents=True, exist_ok=True)


def records(payload):
    for key in ("data", "content", "items", "resultados"):
        if isinstance(payload.get(key), list):
            return payload[key]
    return []


def main():
    s = requests.Session()
    s.headers.update({"User-Agent":"Pesquisa-Academica-PNCP-Datas/1.0","Accept":"application/json"})
    rows=[]
    for page in range(1, MAX_PAGES + 1):
        r=s.get(URL, params={"dataInicial":START,"dataFinal":END,"pagina":page,"tamanhoPagina":500}, timeout=90)
        r.raise_for_status()
        rows.extend(records(r.json()))
    df=pd.json_normalize(rows, sep=".")
    start=pd.Timestamp("2025-01-01")
    end=pd.Timestamp("2025-01-08 23:59:59.999999")
    candidates=[]
    for col in df.columns:
        if "data" not in col.lower():
            continue
        parsed=pd.to_datetime(df[col], errors="coerce")
        valid=parsed.notna()
        if not valid.any():
            continue
        candidates.append({
            "campo":col,
            "n_total":int(len(df)),
            "n_data_valida":int(valid.sum()),
            "min":parsed.min().isoformat() if pd.notna(parsed.min()) else None,
            "max":parsed.max().isoformat() if pd.notna(parsed.max()) else None,
            "dentro_intervalo_pct":round(float(parsed[valid].between(start,end,inclusive="both").mean()*100),4),
            "fora_intervalo_n":int((valid & ~parsed.between(start,end,inclusive="both")).sum()),
        })
    out=pd.DataFrame(candidates).sort_values(["dentro_intervalo_pct","n_data_valida"], ascending=[False,False])
    out.to_csv(OUT/"campos_data_intervalo.csv", index=False, encoding="utf-8-sig")
    summary={"intervalo":[START,END],"paginas":MAX_PAGES,"registros":len(df),"campos_data":len(out)}
    (OUT/"resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(out.to_string(index=False))
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
