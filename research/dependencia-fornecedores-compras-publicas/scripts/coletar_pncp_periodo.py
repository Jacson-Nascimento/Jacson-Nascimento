#!/usr/bin/env python3
"""Coleta PNCP por intervalo de datas de publicação.

Produz uma base pública minimizada para fornecedores PJ e diagnósticos agregados
para todos os tipos de fornecedor. O comprador institucional é o CNPJ do órgão do
instrumento. Município é dimensão territorial, não substitui o comprador.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from piloto_pncp_diagnostico import prepare, first_existing

BASE_URL = "https://pncp.gov.br/api/consulta/v1/contratos"
PAGE_SIZE = 500


def records(payload: dict[str, Any]):
    for key in ("data", "content", "items", "resultados"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def total_pages(payload: dict[str, Any]):
    for key in ("totalPaginas", "totalPages"):
        if payload.get(key) is not None:
            return int(payload[key])
    if payload.get("paginasRestantes") is not None:
        return int(payload["paginasRestantes"]) + 1
    return 1


def fetch_page(session, start, end, page):
    params = {
        "dataInicial": start,
        "dataFinal": end,
        "pagina": page,
        "tamanhoPagina": PAGE_SIZE,
    }
    for attempt in range(7):
        try:
            r = session.get(BASE_URL, params=params, timeout=120)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(2 ** attempt, 45))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError):
            if attempt == 6:
                raise
            time.sleep(min(2 ** attempt, 45))
    raise RuntimeError("Falha PNCP")


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", required=True, help="AAAAMMDD")
    p.add_argument("--end", required=True, help="AAAAMMDD")
    p.add_argument("--label", required=True, help="rótulo dos arquivos, ex. 2025-01")
    p.add_argument("--out-root", default=None)
    args = p.parse_args()

    root = Path(args.out_root) if args.out_root else Path(__file__).resolve().parents[1]
    data_dir = root / "data" / "processed" / "pncp_mensal"
    result_dir = root / "results" / "pncp_mensal"
    data_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    s = requests.Session()
    s.headers.update({"User-Agent":"Pesquisa-Academica-PNCP-Periodo/1.0","Accept":"application/json"})

    first = fetch_page(s, args.start, args.end, 1)
    rows = records(first)
    pages = total_pages(first)
    print(f"{args.label}: {pages} páginas; página 1={len(rows)}")
    page_counts=[{"pagina":1,"n":len(rows)}]
    for page in range(2, pages + 1):
        payload = fetch_page(s, args.start, args.end, page)
        rec = records(payload)
        rows.extend(rec)
        page_counts.append({"pagina":page,"n":len(rec)})
        if page % 25 == 0 or page == pages:
            print(f"{args.label}: {page}/{pages}; acumulado={len(rows)}")
        time.sleep(0.05)

    raw = pd.json_normalize(rows, sep=".")
    df = prepare(raw)

    df["orgao_cnpj"] = first_existing(df, ["orgaoEntidade.cnpj"]).astype("string").str.replace(r"[^0-9A-Za-z]", "", regex=True).str.upper()
    df["orgao_razao_social"] = first_existing(df, ["orgaoEntidade.razaoSocial", "orgaoEntidade.razaoSocialNome"]).astype("string")
    df["unidade_codigo"] = first_existing(df, ["unidadeOrgao.codigoUnidade", "unidadeOrgao.codigo"]).astype("string")
    df["unidade_nome"] = first_existing(df, ["unidadeOrgao.nomeUnidade", "unidadeOrgao.nome"]).astype("string")
    df["orgao_cnpj_id"] = df["id_contrato"].astype("string").str.extract(r"^([0-9A-Za-z]{14})-")[0].str.upper()
    df["orgao_compra_cnpj"] = df["id_compra"].astype("string").str.extract(r"^([0-9A-Za-z]{14})-")[0].str.upper()
    df["flag_orgao_id_diverge"] = df["orgao_cnpj"].notna() & df["orgao_cnpj_id"].notna() & df["orgao_cnpj"].ne(df["orgao_cnpj_id"])
    df["origem_externa"] = df["orgao_cnpj"].notna() & df["orgao_compra_cnpj"].notna() & df["orgao_cnpj"].ne(df["orgao_compra_cnpj"])
    df["flag_lag_negativo"] = df["lag_publicacao_dias"].lt(0)
    df["ano_publicacao"] = df["data_publicacao"].dt.year.astype("Int64")
    df["mes_publicacao"] = df["data_publicacao"].dt.month.astype("Int64")

    muni = df[
        df["esfera"].str.upper().eq("M")
        & df["poder"].str.upper().eq("E")
        & df["orgao_cnpj"].notna() & df["orgao_cnpj"].ne("")
        & df["municipio_ibge"].notna() & df["municipio_ibge"].ne("")
        & df["fornecedor_id_limpo"].notna() & df["fornecedor_id_limpo"].ne("")
        & df["valorInicial"].gt(0)
        & df["receita"].fillna(False).eq(False)
    ].copy()

    pj = muni[muni["tipo_pessoa"].astype("string").str.upper().eq("PJ")].copy()
    cols_public = [
        "id_contrato","id_compra","orgao_cnpj","orgao_compra_cnpj","origem_externa",
        "unidade_codigo","municipio_ibge","municipio","uf","fornecedor_id_limpo",
        "tipo_pessoa","categoria","tipo_contrato","valorInicial","valorGlobal","valorAcumulado",
        "data_assinatura","data_publicacao","lag_publicacao_dias","flag_lag_negativo",
        "ano_assinatura","ano_publicacao","mes_publicacao"
    ]
    public_path = data_dir / f"pncp_{args.label}_municipal_pj.csv.gz"
    pj[cols_public].to_csv(public_path,index=False,compression="gzip",encoding="utf-8")

    # Diagnóstico institucional agregado sem IDs de fornecedores PF.
    buyer = (
        muni.groupby(["orgao_cnpj","municipio_ibge","municipio","uf"], dropna=False)
        .agg(
            instrumentos=("id_contrato","nunique"),
            compras=("id_compra","nunique"),
            fornecedores=("fornecedor_id_limpo","nunique"),
            valor_inicial=("valorInicial","sum"),
            share_origem_externa=("origem_externa","mean"),
            lag_mediano=("lag_publicacao_dias","median"),
        ).reset_index()
    )
    buyer.to_csv(result_dir / f"{args.label}_compradores.csv", index=False, encoding="utf-8-sig")

    tipos = muni["tipo_pessoa"].astype("string").str.upper().value_counts(dropna=False).to_dict()
    tipo_contrato = muni["tipo_contrato"].value_counts(dropna=False).rename_axis("tipo_contrato").reset_index(name="n")
    tipo_contrato.to_csv(result_dir / f"{args.label}_tipos_instrumento.csv", index=False, encoding="utf-8-sig")
    categorias = muni["categoria"].value_counts(dropna=False).rename_axis("categoria").reset_index(name="n")
    categorias.to_csv(result_dir / f"{args.label}_categorias.csv", index=False, encoding="utf-8-sig")

    lag = muni["lag_publicacao_dias"].dropna()
    summary = {
        "label":args.label,"data_inicial_publicacao":args.start,"data_final_publicacao":args.end,
        "paginas":pages,"registros_brutos":int(len(df)),"registros_municipais_validos":int(len(muni)),
        "registros_pj":int(tipos.get("PJ",0)),"registros_pf":int(tipos.get("PF",0)),"registros_pe":int(tipos.get("PE",0)),
        "instrumentos_unicos":int(muni["id_contrato"].nunique()),"compras_unicas":int(muni["id_compra"].nunique()),
        "orgaos_unicos":int(muni["orgao_cnpj"].nunique()),"municipios_unicos":int(muni["municipio_ibge"].nunique()),
        "fornecedores_unicos":int(muni["fornecedor_id_limpo"].nunique()),
        "origem_externa_pct":round(float(muni["origem_externa"].mean()*100),4) if len(muni) else None,
        "flag_orgao_id_diverge_n":int(muni["flag_orgao_id_diverge"].sum()),
        "lag_negativo_n":int(muni["flag_lag_negativo"].sum()),
        "lag_mediana":float(lag.median()) if len(lag) else None,
        "lag_p90":float(lag.quantile(.90)) if len(lag) else None,
        "lag_p95":float(lag.quantile(.95)) if len(lag) else None,
        "lag_max":float(lag.max()) if len(lag) else None,
        "arquivo_publico":str(public_path.relative_to(root)),
        "sha256_arquivo_publico":sha256(public_path),
        "politica":"Base pública identificada contém somente fornecedores PJ; diagnósticos agregados incluem PJ/PF/PE."
    }
    (result_dir/f"{args.label}_resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    pd.DataFrame(page_counts).to_csv(result_dir/f"{args.label}_paginas.csv",index=False)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
