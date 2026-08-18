#!/usr/bin/env python3
"""Coleta DCA/SICONFI para a amostra municipal definida pelo PNCP.

Uso:
  python scripts/coletar_siconfi_dca.py \
    results/piloto2025_cobertura_municipal.csv \
    --year 2025 \
    --annexes 'DCA-Anexo I-D' 'DCA-Anexo I-E'

A coleta é deliberadamente condicionada à amostra PNCP para evitar baixar
controles fiscais de municípios que não entrarão na análise contratual.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

BASE_URL = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca"
DEFAULT_ANNEXES = ["DCA-Anexo I-D", "DCA-Anexo I-E"]


def fetch_all(session: requests.Session, params: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    limit = 5000

    for attempt_page in range(1000):
        q = dict(params)
        q.update({"offset": offset, "limit": limit})
        payload = None

        for attempt in range(5):
            try:
                r = session.get(BASE_URL, params=q, timeout=90)
                if r.status_code in (429, 500, 502, 503, 504):
                    time.sleep(min(3 * (attempt + 1), 20))
                    continue
                r.raise_for_status()
                payload = r.json()
                break
            except (requests.RequestException, ValueError):
                if attempt == 4:
                    raise
                time.sleep(min(3 * (attempt + 1), 20))

        if payload is None:
            break

        items = payload.get("items", [])
        if not isinstance(items, list):
            raise ValueError("Resposta SICONFI sem lista 'items'.")

        rows.extend(items)
        has_more = bool(payload.get("hasMore") or payload.get("has_more"))
        if not has_more or len(items) == 0:
            break

        offset += len(items)
        time.sleep(0.08)

    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("municipios_csv", help="CSV contendo a coluna municipio_ibge.")
    p.add_argument("--year", type=int, default=2025)
    p.add_argument("--annexes", nargs="+", default=DEFAULT_ANNEXES)
    p.add_argument("--min-coverage", type=float, default=0.0,
                   help="Se existir coverage_sentinela, mantém municípios acima deste valor.")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    src = pd.read_csv(args.municipios_csv, dtype={"municipio_ibge": "string"})
    if "municipio_ibge" not in src.columns:
        raise ValueError("Arquivo de municípios precisa conter municipio_ibge.")

    if "coverage_sentinela" in src.columns and args.min_coverage > 0:
        src = src[pd.to_numeric(src["coverage_sentinela"], errors="coerce").ge(args.min_coverage)]

    municipios = (
        src["municipio_ibge"].dropna().astype("string").str.strip().drop_duplicates().sort_values().tolist()
    )
    if not municipios:
        raise RuntimeError("Nenhum município disponível para coleta.")

    root = Path(__file__).resolve().parents[1]
    out = Path(args.out) if args.out else root / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Pesquisa-Academica-SICONFI/1.0",
        "Accept": "application/json",
    })

    records = []
    status = []

    for idx, municipio in enumerate(municipios, start=1):
        for annex in args.annexes:
            params = {
                "an_exercicio": args.year,
                "id_ente": municipio,
                "no_anexo": annex,
            }
            try:
                rows = fetch_all(session, params)
                for row in rows:
                    row["_municipio_consulta"] = municipio
                    row["_anexo_consulta"] = annex
                    row["_exercicio_consulta"] = args.year
                records.extend(rows)
                status.append({
                    "municipio_ibge": municipio,
                    "anexo": annex,
                    "exercicio": args.year,
                    "status": "ok",
                    "n_registros": len(rows),
                })
            except Exception as exc:
                status.append({
                    "municipio_ibge": municipio,
                    "anexo": annex,
                    "exercicio": args.year,
                    "status": "erro",
                    "n_registros": 0,
                    "erro": repr(exc),
                })
            time.sleep(0.10)

        if idx % 100 == 0 or idx == len(municipios):
            print(f"SICONFI: {idx}/{len(municipios)} municípios processados")

    status_df = pd.DataFrame(status)
    status_df.to_csv(out / f"siconfi_dca_{args.year}_status.csv", index=False, encoding="utf-8-sig")

    if records:
        data = pd.json_normalize(records, sep=".")
        data.to_csv(
            out / f"siconfi_dca_{args.year}.csv.gz",
            index=False, compression="gzip", encoding="utf-8"
        )
    else:
        data = pd.DataFrame()

    resumo = {
        "exercicio": args.year,
        "anexos": args.annexes,
        "municipios_solicitados": len(municipios),
        "consultas": len(status_df),
        "consultas_ok": int(status_df["status"].eq("ok").sum()),
        "consultas_erro": int(status_df["status"].eq("erro").sum()),
        "consultas_sem_registros": int((status_df["status"].eq("ok") & status_df["n_registros"].eq(0)).sum()),
        "registros_coletados": int(len(data)),
    }
    (out / f"siconfi_dca_{args.year}_resumo.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
