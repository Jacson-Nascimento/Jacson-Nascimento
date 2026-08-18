#!/usr/bin/env python3
"""
Piloto de diagnóstico da API pública do PNCP.

Objetivo:
- testar acesso e estrutura dos contratos;
- medir completude dos campos necessários ao artigo;
- identificar duplicidades, atraso de publicação e instrumentos repetidos;
- produzir uma amostra municipal limpa para inspeção.

Uso recomendado:
    python piloto_pncp_diagnostico.py

Ou:
    python piloto_pncp_diagnostico.py --dates 20250115 20250415 20250715 20251015

Dependências:
    pip install requests pandas
"""

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import requests

BASE_URL = "https://pncp.gov.br/api/consulta/v1/contratos"
DEFAULT_DATES = ["20250115", "20250415", "20250715", "20251015"]
PAGE_SIZE = 500


def fetch_page(date_yyyymmdd: str, page: int, session: requests.Session) -> Dict[str, Any]:
    params = {
        "dataInicial": date_yyyymmdd,
        "dataFinal": date_yyyymmdd,
        "pagina": page,
        "tamanhoPagina": PAGE_SIZE,
    }
    for attempt in range(6):
        try:
            r = session.get(BASE_URL, params=params, timeout=60)
            if r.status_code == 429:
                time.sleep(min(2 ** attempt, 30))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError):
            if attempt == 5:
                raise
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError("Falha inesperada na consulta.")


def get_total_pages(payload: Dict[str, Any]) -> int:
    candidates = [
        payload.get("totalPaginas"),
        payload.get("totalPages"),
        payload.get("paginasRestantes"),
    ]
    if candidates[0] is not None:
        return int(candidates[0])
    if candidates[1] is not None:
        return int(candidates[1])
    if candidates[2] is not None:
        return int(candidates[2]) + 1
    return 1


def get_records(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ("data", "content", "items", "resultados"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def collect_date(date_yyyymmdd: str, session: requests.Session) -> List[Dict[str, Any]]:
    first = fetch_page(date_yyyymmdd, 1, session)
    rows = get_records(first)
    total_pages = get_total_pages(first)
    print(f"{date_yyyymmdd}: página 1/{total_pages}, {len(rows)} registros")

    for page in range(2, total_pages + 1):
        payload = fetch_page(date_yyyymmdd, page, session)
        recs = get_records(payload)
        rows.extend(recs)
        print(f"{date_yyyymmdd}: página {page}/{total_pages}, +{len(recs)}")
        time.sleep(0.10)

    for row in rows:
        row["_data_consulta"] = date_yyyymmdd
    return rows


def first_existing(df: pd.DataFrame, names: List[str]) -> pd.Series:
    for name in names:
        if name in df.columns:
            return df[name]
    return pd.Series([pd.NA] * len(df), index=df.index)


def bool_normalize(s: pd.Series) -> pd.Series:
    text = s.astype("string").str.strip().str.lower()
    return text.map({
        "true": True, "1": True, "sim": True,
        "false": False, "0": False, "não": False, "nao": False
    }).astype("boolean")


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["id_contrato"] = first_existing(out, ["numeroControlePNCP", "numeroControlePncp"]).astype("string")
    out["id_compra"] = first_existing(out, ["numeroControlePNCPCompra", "numeroControlePncpCompra"]).astype("string")
    out["esfera"] = first_existing(out, ["orgaoEntidade.esferaId", "orgaoEntidade.esfera"]).astype("string")
    out["poder"] = first_existing(out, ["orgaoEntidade.poderId", "orgaoEntidade.poder"]).astype("string")
    out["municipio_ibge"] = first_existing(out, ["unidadeOrgao.codigoIbge", "unidadeOrgao.municipioId", "unidadeOrgao.codigoIBGE"]).astype("string").str.replace(r"\.0$", "", regex=True)
    out["municipio"] = first_existing(out, ["unidadeOrgao.municipioNome", "unidadeOrgao.nomeMunicipio"]).astype("string")
    out["uf"] = first_existing(out, ["unidadeOrgao.ufSigla", "unidadeOrgao.uf"]).astype("string")
    out["fornecedor_id"] = first_existing(out, ["niFornecedor", "fornecedor.niFornecedor"]).astype("string").str.strip()
    out["fornecedor_nome"] = first_existing(out, ["nomeRazaoSocialFornecedor", "fornecedor.nomeRazaoSocialFornecedor"]).astype("string")
    out["tipo_pessoa"] = first_existing(out, ["tipoPessoa", "tipoPessoaFornecedor"]).astype("string")
    out["categoria"] = first_existing(out, ["categoriaProcesso.nome", "categoriaProcesso", "categoriaProcessoNome"]).astype("string")
    out["tipo_contrato"] = first_existing(out, ["tipoContrato.nome", "tipoContrato", "tipoContratoNome"]).astype("string")
    out["receita"] = bool_normalize(first_existing(out, ["receita"]))

    for col in ["valorInicial", "valorGlobal", "valorAcumulado"]:
        out[col] = pd.to_numeric(first_existing(out, [col]), errors="coerce")

    out["data_assinatura"] = pd.to_datetime(first_existing(out, ["dataAssinatura"]), errors="coerce")
    out["data_publicacao"] = pd.to_datetime(first_existing(out, ["dataPublicacaoPncp", "dataPublicacaoPNCP"]), errors="coerce")
    out["lag_publicacao_dias"] = (out["data_publicacao"] - out["data_assinatura"]).dt.days
    out["ano_assinatura"] = out["data_assinatura"].dt.year.astype("Int64")
    out["fornecedor_id_limpo"] = out["fornecedor_id"].str.replace(r"[^0-9A-Za-z]", "", regex=True).str.upper()
    out["fornecedor_id_14_numeric"] = out["fornecedor_id_limpo"].str.fullmatch(r"\d{14}", na=False)
    return out


def pct(x: pd.Series) -> float:
    if len(x) == 0:
        return float("nan")
    return round(float(x.mean() * 100), 2)


def diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    def add(metric, value):
        rows.append({"metrica": metric, "valor": value})

    add("registros_total", len(df))
    add("contratos_unicos", df["id_contrato"].nunique(dropna=True))
    add("duplicidade_id_contrato_pct", pct(df["id_contrato"].duplicated(keep=False)))
    add("esfera_municipal_pct", pct(df["esfera"].str.upper().eq("M")))
    add("municipio_ibge_ausente_pct", pct(df["municipio_ibge"].isna() | df["municipio_ibge"].eq("")))
    add("fornecedor_id_ausente_pct", pct(df["fornecedor_id"].isna() | df["fornecedor_id"].eq("")))
    add("fornecedor_cnpj_numerico_14_pct", pct(df["fornecedor_id_14_numeric"]))
    add("valor_inicial_ausente_pct", pct(df["valorInicial"].isna()))
    add("valor_inicial_nao_positivo_pct", pct(df["valorInicial"].fillna(0).le(0)))
    add("data_assinatura_ausente_pct", pct(df["data_assinatura"].isna()))
    add("data_publicacao_ausente_pct", pct(df["data_publicacao"].isna()))
    add("lag_publicacao_mediana_dias", df["lag_publicacao_dias"].median())
    add("lag_publicacao_p90_dias", df["lag_publicacao_dias"].quantile(0.90))
    add("compras_unicas", df["id_compra"].nunique(dropna=True))

    counts = df.dropna(subset=["id_compra"]).groupby("id_compra").size()
    if len(counts):
        add("instrumentos_por_compra_mediana", counts.median())
        add("compras_com_mais_de_um_instrumento_pct", round((counts.gt(1).mean() * 100), 2))
        add("max_instrumentos_mesma_compra", int(counts.max()))
    return pd.DataFrame(rows)


def municipal_clean(df: pd.DataFrame) -> pd.DataFrame:
    mask = (
        df["esfera"].str.upper().eq("M")
        & df["municipio_ibge"].notna()
        & df["municipio_ibge"].ne("")
        & df["fornecedor_id"].notna()
        & df["fornecedor_id"].ne("")
        & df["valorInicial"].gt(0)
        & df["receita"].fillna(False).eq(False)
    )
    return df.loc[mask].copy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dates", nargs="+", default=DEFAULT_DATES, help="Datas de publicação no formato AAAAMMDD.")
    parser.add_argument("--out", default="saida_piloto_pncp", help="Diretório de saída.")
    args = parser.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": "Pesquisa-Academica-PNCP/1.0", "Accept": "application/json"})

    raw_rows = []
    for date in args.dates:
        raw_rows.extend(collect_date(date, session))

    if not raw_rows:
        raise RuntimeError("A API respondeu, mas nenhum registro foi coletado.")

    raw = pd.json_normalize(raw_rows, sep=".")
    raw.to_csv(outdir / "pncp_raw_normalizado.csv", index=False, encoding="utf-8-sig")
    df = prepare(raw)
    df.to_csv(outdir / "pncp_preparado.csv", index=False, encoding="utf-8-sig")
    diag = diagnostics(df)
    diag.to_csv(outdir / "diagnostico.csv", index=False, encoding="utf-8-sig")
    muni = municipal_clean(df)
    muni.to_csv(outdir / "pncp_municipal_limpo.csv", index=False, encoding="utf-8-sig")

    for col in ["esfera", "poder", "categoria", "tipo_contrato", "tipo_pessoa", "uf"]:
        if col in df.columns:
            df[col].fillna("<NA>").value_counts(dropna=False).rename_axis(col).reset_index(name="n").to_csv(outdir / f"distribuicao_{col}.csv", index=False, encoding="utf-8-sig")

    summary = {
        "datas_consultadas": args.dates,
        "registros_total": int(len(df)),
        "registros_municipais_limpos": int(len(muni)),
        "municipios_unicos_amostra": int(muni["municipio_ibge"].nunique(dropna=True)),
        "fornecedores_unicos_amostra": int(muni["fornecedor_id_limpo"].nunique(dropna=True)),
        "observacao": "Esta é uma amostra por datas de PUBLICAÇÃO. Não use HHI ou concentração desta amostra como resultado anual do artigo."
    }
    (outdir / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(diag.to_string(index=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
