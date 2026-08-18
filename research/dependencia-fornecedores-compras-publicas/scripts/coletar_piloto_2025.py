#!/usr/bin/env python3
"""Coleta piloto sentinela do PNCP para 2025.

Amostra uma quarta-feira de cada mês, baixa todas as páginas de contratos
publicados naquela data, mede qualidade e calcula métricas exploratórias.

Privacidade:
- diagnósticos agregados usam todos os tipos de fornecedor;
- arquivos públicos com identificador de fornecedor usam somente PJ;
- PF e PE não são republicados no repositório público.

Os resultados NÃO representam estimativas anuais.
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

    # Base pública com identificadores somente de pessoas jurídicas.
    muni_pj = muni[muni["tipo_pessoa"].astype("string").str.upper().eq("PJ")].copy()

    cols_publicos = [
        "data_consulta", "mes_consulta", "id_contrato", "id_compra",
        "esfera", "poder", "municipio_ibge", "municipio", "uf",
        "fornecedor_id_limpo", "tipo_pessoa", "categoria", "tipo_contrato",
        "valorInicial", "valorGlobal", "valorAcumulado", "data_assinatura",
        "data_publicacao", "lag_publicacao_dias", "ano_assinatura",
    ]
    muni_pj[cols_publicos].to_csv(
        OUT_DATA / "pncp_piloto_2025_sentinela_publica_pj.csv.gz",
        index=False, compression="gzip", encoding="utf-8"
    )

    # Diagnóstico agregado por data sentinela, sem identificadores pessoais.
    date_rows = []
    for date, g in df.groupby("data_consulta"):
        gm = muni[muni["data_consulta"].eq(date)]
        date_rows.append({
            "data": date.date().isoformat(),
            "registros_total": len(g),
            "registros_municipais_validos": len(gm),
            "registros_pj": int(gm["tipo_pessoa"].astype("string").str.upper().eq("PJ").sum()),
            "registros_pf": int(gm["tipo_pessoa"].astype("string").str.upper().eq("PF").sum()),
            "registros_pe": int(gm["tipo_pessoa"].astype("string").str.upper().eq("PE").sum()),
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

    presenca = (
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
    presenca["presenca_sentinela"] = presenca["datas_sentinela"] / len(DATES)
    presenca.to_csv(OUT_RESULTS / "piloto2025_presenca_municipal.csv", index=False)

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

    # Métricas com todos os fornecedores somente em nível agregado, sem IDs.
    if len(muni):
        _, markets_all, _ = calculate(muni)
        markets_all = markets_all.merge(
            muni.groupby(["municipio_ibge", "categoria", "ano_assinatura"])
            .agg(n_instrumentos=("id_contrato", "nunique"), datas_sentinela=("data_consulta", "nunique"))
            .reset_index(),
            on=["municipio_ibge", "categoria", "ano_assinatura"], how="left"
        )
        markets_all["interpretavel_piloto"] = (
            markets_all["n_fornecedores"].ge(3)
            & markets_all["n_instrumentos"].ge(5)
            & markets_all["datas_sentinela"].ge(2)
        )
        markets_all.to_csv(OUT_RESULTS / "piloto2025_metricas_exploratorias_agregadas.csv", index=False)

    # Arquivos com identificadores de fornecedor são restritos a PJ.
    if len(muni_pj):
        rel_pj, markets_pj, suppliers_pj = calculate(muni_pj)
        markets_pj.to_csv(OUT_RESULTS / "piloto2025_metricas_mercado_pj.csv", index=False)
        suppliers_pj.to_csv(OUT_RESULTS / "piloto2025_metricas_fornecedor_pj.csv", index=False)
        rel_pj.to_csv(OUT_RESULTS / "piloto2025_relacoes_pj.csv.gz", index=False, compression="gzip")

    tipos = muni["tipo_pessoa"].astype("string").str.upper().value_counts().to_dict()
    summary = {
        "datas_sentinela": DATES,
        "registros_total": int(len(df)),
        "registros_municipais_validos": int(len(muni)),
        "registros_pj": int(tipos.get("PJ", 0)),
        "registros_pf": int(tipos.get("PF", 0)),
        "registros_pe": int(tipos.get("PE", 0)),
        "municipios_unicos": int(muni["municipio_ibge"].nunique()),
        "ufs_unicas": int(muni["uf"].nunique()),
        "fornecedores_unicos": int(muni["fornecedor_id_limpo"].nunique()),
        "contratos_unicos": int(muni["id_contrato"].nunique()),
        "compras_unicas": int(muni["id_compra"].nunique()),
        "politica_publicacao": "GitHub: identificadores somente de fornecedores PJ. PF e PE ficam fora das bases identificadas públicas.",
        "observacao": "Amostra sentinela de 12 dias. Não interpretar HHI como concentração anual.",
    }
    (OUT_RESULTS / "piloto2025_resumo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
