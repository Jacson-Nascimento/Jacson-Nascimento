#!/usr/bin/env python3
"""Probe rápido do PNCP 2025: apenas a primeira página de quatro datas.

Serve para medir ordem de grandeza, paginação e completude sem confundir a
amostra com resultados econômicos do artigo.
"""
from pathlib import Path
import json
import pandas as pd
import requests

from piloto_pncp_diagnostico import prepare

BASE_URL = "https://pncp.gov.br/api/consulta/v1/contratos"
DATES = ["20250115", "20250416", "20250716", "20251015"]
PAGE_SIZE = 500

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)


def get_records(payload):
    for key in ("data", "content", "items", "resultados"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def main():
    s = requests.Session()
    s.headers.update({"User-Agent": "Pesquisa-Academica-PNCP-Probe/1.0", "Accept": "application/json"})
    rows = []
    summary = []

    for date in DATES:
        r = s.get(BASE_URL, params={
            "dataInicial": date,
            "dataFinal": date,
            "pagina": 1,
            "tamanhoPagina": PAGE_SIZE,
        }, timeout=30)
        r.raise_for_status()
        payload = r.json()
        recs = get_records(payload)
        raw = pd.json_normalize(recs, sep=".") if recs else pd.DataFrame()
        df = prepare(raw) if len(raw) else pd.DataFrame()

        total_pages = payload.get("totalPaginas", payload.get("totalPages"))
        total_records = payload.get("totalRegistros", payload.get("totalElements"))
        if total_pages is None and payload.get("paginasRestantes") is not None:
            total_pages = int(payload["paginasRestantes"]) + 1

        if len(df):
            municipal = df["esfera"].astype("string").str.upper().eq("M")
            executivo = df["poder"].astype("string").str.upper().eq("E")
            valid_supplier = df["fornecedor_id"].notna() & df["fornecedor_id"].ne("")
            valid_ibge = df["municipio_ibge"].notna() & df["municipio_ibge"].ne("")
            positive_value = df["valorInicial"].gt(0)
            usable = municipal & executivo & valid_supplier & valid_ibge & positive_value
            summary.append({
                "data": date,
                "registros_primeira_pagina": len(df),
                "total_registros_reportado": total_records,
                "total_paginas_reportado": total_pages,
                "municipal_pct_pagina1": round(float(municipal.mean()*100), 2),
                "municipal_executivo_pct_pagina1": round(float((municipal & executivo).mean()*100), 2),
                "fornecedor_ausente_pct_pagina1": round(float((~valid_supplier).mean()*100), 2),
                "ibge_ausente_pct_pagina1": round(float((~valid_ibge).mean()*100), 2),
                "valor_nao_positivo_pct_pagina1": round(float((~positive_value).mean()*100), 2),
                "registros_utilizaveis_pagina1": int(usable.sum()),
                "municipios_utilizaveis_pagina1": int(df.loc[usable, "municipio_ibge"].nunique()),
                "fornecedores_utilizaveis_pagina1": int(df.loc[usable, "fornecedor_id_limpo"].nunique()),
            })
        else:
            summary.append({"data": date, "registros_primeira_pagina": 0,
                            "total_registros_reportado": total_records,
                            "total_paginas_reportado": total_pages})

    out = pd.DataFrame(summary)
    out.to_csv(OUT / "probe_pncp_2025.csv", index=False, encoding="utf-8-sig")
    (OUT / "probe_pncp_2025.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out.to_string(index=False))

if __name__ == "__main__":
    main()
