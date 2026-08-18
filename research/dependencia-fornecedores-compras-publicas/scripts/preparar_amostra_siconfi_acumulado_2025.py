#!/usr/bin/env python3
"""Prepara amostra PNCP acumulada para integração incremental com SICONFI/DCA 2025.

A unidade analítica é o CNPJ comprador. O cruzamento fiscal principal exige que
cada CNPJ elegível esteja associado a exatamente um código IBGE municipal na
coorte acumulada de instrumentos assinados em 2025.

O script também identifica apenas os municípios ainda não consultados na
integração janeiro-fevereiro, evitando recoleta desnecessária do SICONFI.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results"


def norm_ibge(s: pd.Series) -> pd.Series:
    return s.astype("string").str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(7)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--month", type=int, required=True, choices=range(1, 13))
    p.add_argument("--previous-integration", default="siconfi_integracao_jan_fev_2025")
    args = p.parse_args()

    month = args.month
    out = RES / f"siconfi_integracao_acumulada_2025_{month:02d}"
    out.mkdir(parents=True, exist_ok=True)

    elig_path = RES / f"carteira_acumulada_2025_{month:02d}_diagnostico" / "compradores_elegiveis.csv"
    eligible = pd.read_csv(elig_path, dtype={"orgao_cnpj": "string"}, low_memory=False)
    ids = set(eligible["orgao_cnpj"].dropna().astype(str))

    frames = []
    for m in range(1, month + 1):
        path = DATA / f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        d = pd.read_csv(
            path,
            dtype={"orgao_cnpj": "string", "municipio_ibge": "string"},
            low_memory=False,
        )
        d["ano_assinatura"] = pd.to_numeric(d["ano_assinatura"], errors="coerce")
        d = d[d["ano_assinatura"].eq(2025) & d["orgao_cnpj"].astype(str).isin(ids)].copy()
        frames.append(d[["orgao_cnpj", "municipio_ibge", "municipio", "uf", "id_contrato"]])

    x = pd.concat(frames, ignore_index=True)
    x = x.dropna(subset=["orgao_cnpj", "municipio_ibge"])
    x["municipio_ibge"] = norm_ibge(x["municipio_ibge"])

    counts = (
        x.groupby("orgao_cnpj")
        .agg(
            n_municipios=("municipio_ibge", "nunique"),
            n_instrumentos_mapeados=("id_contrato", "nunique"),
        )
        .reset_index()
    )
    first = (
        x.sort_values(["orgao_cnpj", "municipio_ibge"])
        .drop_duplicates("orgao_cnpj")[["orgao_cnpj", "municipio_ibge", "municipio", "uf"]]
    )
    mapping = counts.merge(first, on="orgao_cnpj", how="left")
    mapping = mapping.merge(eligible, on="orgao_cnpj", how="left", suffixes=("", "_metricas"))
    mapping["integracao_siconfi_principal"] = mapping["n_municipios"].eq(1)

    principal = mapping[mapping["integracao_siconfi_principal"]].copy()
    multi = mapping[~mapping["integracao_siconfi_principal"]].copy()
    municipios = (
        principal[["municipio_ibge", "municipio", "uf"]]
        .drop_duplicates("municipio_ibge")
        .sort_values("municipio_ibge")
    )

    previous_dir = RES / args.previous_integration
    previous_status = previous_dir / "coleta" / "siconfi_dca_2025_status.csv"
    previous_municipios: set[str] = set()
    if previous_status.exists():
        st = pd.read_csv(previous_status, dtype={"municipio_ibge": "string"}, low_memory=False)
        if "municipio_ibge" in st.columns:
            previous_municipios = set(norm_ibge(st["municipio_ibge"].dropna()).astype(str))

    delta = municipios[~municipios["municipio_ibge"].astype(str).isin(previous_municipios)].copy()

    mapping.to_csv(out / "mapeamento_comprador_municipio.csv", index=False, encoding="utf-8-sig")
    principal.to_csv(out / "compradores_integracao_principal.csv", index=False, encoding="utf-8-sig")
    multi.to_csv(out / "compradores_multimunicipio.csv", index=False, encoding="utf-8-sig")
    municipios.to_csv(out / "municipios_siconfi.csv", index=False, encoding="utf-8-sig")
    delta.to_csv(out / "municipios_siconfi_delta.csv", index=False, encoding="utf-8-sig")

    summary = {
        "mes_final_publicacao": f"2025-{month:02d}",
        "compradores_elegiveis_entrada": int(len(eligible)),
        "compradores_mapeados": int(mapping["municipio_ibge"].notna().sum()),
        "compradores_unico_municipio": int(len(principal)),
        "compradores_multi_municipio": int(len(multi)),
        "municipios_unicos_para_siconfi": int(municipios["municipio_ibge"].nunique()),
        "municipios_ja_coletados_reutilizados": int(len(set(municipios["municipio_ibge"].astype(str)) & previous_municipios)),
        "municipios_novos_para_coleta": int(len(delta)),
        "regra": "Integração fiscal principal requer exatamente um municipio_ibge observado por CNPJ comprador na coorte PNCP acumulada assinada em 2025.",
    }
    (out / "resumo_mapeamento.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
