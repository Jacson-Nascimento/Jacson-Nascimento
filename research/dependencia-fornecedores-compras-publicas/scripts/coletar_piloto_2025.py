#!/usr/bin/env python3
"""Coleta piloto sentinela do PNCP para 2025.

Amostra uma quarta-feira de cada mês, baixa todas as páginas de contratos
publicados naquela data, mede qualidade/cobertura e calcula métricas
exploratórias. Os resultados NÃO representam estimativas anuais.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd
import requests

from piloto_pncp_diagnostico import prepare
from calcular_metricas_concentracao import calculate

BASE_URL = "https://pncp.gov.br/api/consulta/v1/contratos"
DATES = [
    "20250115", "20250212", "20250312", "20250416",
    "20250514", "20250611", "20250716", "20250813",
    "20250910", "20251015", "20251112", "20251210",
]
PAGE_SIZE = 500

ROOT = Path(__file__).resolve().parents[1]
OUT_DATA = ROOT / "data" / "processed"
OUT_RESULTS = ROOT / "results"
OUT_DATA.mkdir(parents=True, exist_ok=True)
OUT_RESULTS.mkdir(parents=True, exist_ok=True)


def records(payload):
    for key in ("data", "content", "items", "resultados"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def total_pages(payload):
    if payload.get("totalPaginas") is not None:
        return int(payload["totalPaginas"])
    if payload.get("totalPages") is not None:
        return int(payload["totalPages"])
    if payload.get("paginasRestantes") is not None:
        return int(payload["paginasRestantes"]) + 1
    return 1


def fetch_page(session, date, page):
    params = {
        "dataInicial": date,
        "dataFinal": date,
        "pagina": page,
        "tamanhoPagina": PAGE_SIZE,
    }
    for attempt in range(6):
        try:
            r = session.get(BASE_URL, params=params, timeout=90)
            if r.status_code == 429:
                time.sleep(min(2 ** attempt, 30))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError):
            if attempt == 5:
                raise
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError("Falha na consulta PNCP")


def collect_date(session, date):
    first = fetch_page(session, date, 1)
    rows = records(first)
    pages = total_pages(first)
    print(f"{date}: {len(rows)} registros na primeira página; {pages} páginas")
    for page in range(2, pages + 1):
        payload = fetch_page(session, date, page)
        rows.extend(records(payload))
        time.sleep(0.08)
    for row in rows:
        row["_data_consulta"] = date
    return rows


def safe_pct(series):
    return float(series.mean() * 100) if len(series) else float("nan")


def main():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Pesquisa-Academica-PNCP/1.0",
        "Accept": "application/json",
    })

    raw_rows = []
    for date in DATES:
        raw_rows.extend(collect_date(session, date))

    if not raw_rows:
        raise RuntimeError("Nenhum registro retornado pelo PNCP.")

    raw = pd.json_normalize(raw_rows, sep=".")
    df = prepare(raw)
    df["data_consulta"] = pd.to_datetime(df["_data_consulta"], format="%Y%m%d")
    df["mes_consulta"] = df["data_consulta"].dt.month

    # Base municipal executiva de despesa para o diagnóstico principal.
    muni = df[
        df["esfera"].str.upper().eq("M")
        & df["poder"].str.upper().eq("E")
        & df["municipio_ibge"].notna()
        & df["municipio_ibge"].ne("")
        & df["fornecedor_id_limpo"].notna()
        & df["fornecedor_id_limpo"].ne("")
        & df["valorInicial"].gt(0)
        & df["receita"].fillna(False).eq(False)
    ].copy()

    # Preserva apenas colunas analíticas para manter o arquivo enxuto.
    cols = [
        "data_consulta", "mes_consulta", "id_contrato", "id_compra",
        "esfera", "poder", "municipio_ibge", "municipio", "uf",
        "fornecedor_id_limpo", "fornecedor_nome", "tipo_pessoa",
        "categoria", "tipo_contrato", "valorInicial", "valorGlobal",
        "valorAcumulado", "data_assinatura", "data_publicacao",
        "lag_publicacao_dias", "ano_assinatura",
    ]
    muni[cols].to_csv(
        OUT_DATA / "pncp_piloto_2025_sentinela.csv.gz",
        index=False, compression="gzip", encoding="utf-8"
    )

    # Diagnóstico por data sentinela.
    date_rows = []
    for date, g in df.groupby("data_consulta"):
        gm = muni[muni["data_consulta"].eq(date)]
        date_rows.append({
            "data": date.date().isoformat(),
            "registros_total": len(g),
            "registros_municipais_validos": len(gm),
            "municipios": gm["municipio_ibge"].nunique(),
            "ufs": gm["uf"].nunique(),
            "fornecedores": gm["fornecedor_id_limpo"].nunique(),
            "categorias": gm["categoria"].nunique(),
            "valor_inicial_total": gm["valorInicial"].sum(),
            "fornecedor_ausente_pct_total": safe_pct(g["fornecedor_id"].isna() | g["fornecedor_id"].eq("")),
            "ibge_ausente_pct_total": safe_pct(g["municipio_ibge"].isna() | g["municipio_ibge"].eq("")),
            "valor_nao_positivo_pct_total": safe_pct(g["valorInicial"].fillna(0).le(0)),
            "lag_publicacao_mediana_dias": gm["lag_publicacao_dias"].median(),
            "lag_publicacao_p90_dias": gm["lag_publicacao_dias"].quantile(0.90),
        })
    pd.DataFrame(date_rows).to_csv(OUT_RESULTS / "piloto2025_resumo_datas.csv", index=False)

    # Presença do município nas 12 datas sentinela.
    cobertura = (
        muni.groupby(["municipio_ibge", "municipio", "uf"], dropna=False)
        .agg(
            datas_sentinela=("data_consulta", "nunique"),
            instrumentos=("id_contrato", "nunique"),
            fornecedores=("fornecedor_id_limpo", "nunique"),
            categorias=("categoria", "nunique"),
            valor_inicial=("valorInicial", "sum"),
        )
        .reset_index()
    )
    cobertura["coverage_sentinela"] = cobertura["datas_sentinela"] / len(DATES)
    cobertura.to_csv(OUT_RESULTS / "piloto2025_cobertura_municipal.csv", index=False)

    uf = (
        muni.groupby("uf", dropna=False)
        .agg(
            datas_sentinela=("data_consulta", "nunique"),
            municipios=("municipio_ibge", "nunique"),
            instrumentos=("id_contrato", "nunique"),
            fornecedores=("fornecedor_id_limpo", "nunique"),
            valor_inicial=("valorInicial", "sum"),
        )
        .reset_index()
    )
    uf.to_csv(OUT_RESULTS / "piloto2025_cobertura_uf.csv", index=False)

    # Multiplicidade de instrumentos por compra.
    compras = (
        muni.dropna(subset=["id_compra"])
        .groupby("id_compra")
        .agg(
            n_instrumentos=("id_contrato", "nunique"),
            n_fornecedores=("fornecedor_id_limpo", "nunique"),
            valor_inicial=("valorInicial", "sum"),
        )
        .reset_index()
    )
    compras.to_csv(OUT_RESULTS / "piloto2025_instrumentos_por_compra.csv", index=False)

    # Métricas exploratórias na amostra sentinela, não anuais.
    if len(muni):
        rel, markets, suppliers = calculate(muni)
        markets = markets.merge(
            muni.groupby(["municipio_ibge", "categoria", "ano_assinatura"])
            .agg(n_instrumentos=("id_contrato", "nunique"), datas_sentinela=("data_consulta", "nunique"))
            .reset_index(),
            on=["municipio_ibge", "categoria", "ano_assinatura"], how="left"
        )
        markets["interpretavel_piloto"] = (
            markets["n_fornecedores"].ge(3)
            & markets["n_instrumentos"].ge(5)
            & markets["datas_sentinela"].ge(2)
        )
        markets.to_csv(OUT_RESULTS / "piloto2025_metricas_exploratorias.csv", index=False)
        suppliers.to_csv(OUT_RESULTS / "piloto2025_metricas_fornecedor.csv", index=False)
        rel.to_csv(OUT_RESULTS / "piloto2025_relacoes.csv.gz", index=False, compression="gzip")

    summary = {
        "datas_sentinela": DATES,
        "registros_total": int(len(df)),
        "registros_municipais_validos": int(len(muni)),
        "municipios_unicos": int(muni["municipio_ibge"].nunique()),
        "ufs_unicas": int(muni["uf"].nunique()),
        "fornecedores_unicos": int(muni["fornecedor_id_limpo"].nunique()),
        "contratos_unicos": int(muni["id_contrato"].nunique()),
        "compras_unicas": int(muni["id_compra"].nunique()),
        "observacao": "Amostra sentinela de 12 dias. Não interpretar HHI como concentração anual.",
    }
    (OUT_RESULTS / "piloto2025_resumo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
