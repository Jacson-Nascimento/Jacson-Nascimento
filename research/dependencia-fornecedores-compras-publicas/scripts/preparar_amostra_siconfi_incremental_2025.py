#!/usr/bin/env python3
"""Prepara amostra PNCP acumulada para integração SICONFI/DCA incremental.

Usa a especificação GLOBAL vigente de compradores elegíveis e constrói uma cache
cumulativa de municípios já consultados com sucesso: coleta-base jan-fev e todos
os deltas mensais anteriores. Apenas municípios sem DCA-Anexo I-D com status ok
entram no novo delta.
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


def successful_municipalities(status_path: Path) -> set[str]:
    if not status_path.exists():
        return set()
    st = pd.read_csv(status_path, dtype={"municipio_ibge": "string"}, low_memory=False)
    if "municipio_ibge" not in st.columns:
        return set()
    st["municipio_ibge"] = norm_ibge(st["municipio_ibge"])
    ok = pd.Series(True, index=st.index)
    if "status" in st.columns:
        ok &= st["status"].astype(str).str.lower().eq("ok")
    if "anexo" in st.columns:
        ok &= st["anexo"].astype(str).eq("DCA-Anexo I-D")
    return set(st.loc[ok, "municipio_ibge"].dropna().astype(str))


def prior_status_paths(month: int) -> list[Path]:
    paths = [RES / "siconfi_integracao_jan_fev_2025" / "coleta" / "siconfi_dca_2025_status.csv"]
    for m in range(3, month):
        paths.append(
            RES / f"siconfi_integracao_acumulada_2025_{m:02d}" / "coleta_delta" / "siconfi_dca_2025_status.csv"
        )
    return paths


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--month", type=int, required=True, choices=range(3, 13))
    args = p.parse_args()
    month = args.month

    out = RES / f"siconfi_integracao_acumulada_2025_{month:02d}"
    out.mkdir(parents=True, exist_ok=True)

    elig_path = RES / f"carteira_acumulada_2025_{month:02d}_global" / "compradores_elegiveis_3_5.csv"
    if not elig_path.exists():
        raise FileNotFoundError(f"Amostra global não encontrada: {elig_path}")
    eligible = pd.read_csv(elig_path, dtype={"orgao_cnpj": "string"}, low_memory=False)
    ids = set(eligible["orgao_cnpj"].dropna().astype(str))

    frames = []
    for m in range(1, month + 1):
        path = DATA / f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        if not path.exists():
            raise FileNotFoundError(path)
        d = pd.read_csv(path, dtype={"orgao_cnpj": "string", "municipio_ibge": "string"}, low_memory=False)
        d["ano_assinatura"] = pd.to_numeric(d["ano_assinatura"], errors="coerce")
        d = d[d["ano_assinatura"].eq(2025) & d["orgao_cnpj"].astype(str).isin(ids)].copy()
        frames.append(d[["orgao_cnpj", "municipio_ibge", "municipio", "uf", "id_contrato"]])

    x = pd.concat(frames, ignore_index=True)
    x = x.dropna(subset=["orgao_cnpj", "municipio_ibge"])
    x["municipio_ibge"] = norm_ibge(x["municipio_ibge"])

    counts = (
        x.groupby("orgao_cnpj")
        .agg(n_municipios=("municipio_ibge", "nunique"), n_instrumentos_mapeados=("id_contrato", "nunique"))
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

    status_paths = prior_status_paths(month)
    cache: set[str] = set()
    cache_by_source = {}
    for path in status_paths:
        found = successful_municipalities(path)
        cache |= found
        cache_by_source[str(path.relative_to(ROOT))] = len(found)

    delta = municipios[~municipios["municipio_ibge"].astype(str).isin(cache)].copy()

    mapping.to_csv(out / "mapeamento_comprador_municipio.csv", index=False, encoding="utf-8-sig")
    principal.to_csv(out / "compradores_integracao_principal.csv", index=False, encoding="utf-8-sig")
    multi.to_csv(out / "compradores_multimunicipio.csv", index=False, encoding="utf-8-sig")
    municipios.to_csv(out / "municipios_siconfi.csv", index=False, encoding="utf-8-sig")
    delta.to_csv(out / "municipios_siconfi_delta.csv", index=False, encoding="utf-8-sig")

    current = set(municipios["municipio_ibge"].astype(str))
    summary = {
        "mes_final_publicacao": f"2025-{month:02d}",
        "especificacao_metricas": "carteira_acumulada_global; elegibilidade 3 fornecedores/5 instrumentos",
        "compradores_elegiveis_entrada": int(len(eligible)),
        "compradores_mapeados": int(mapping["municipio_ibge"].notna().sum()),
        "compradores_unico_municipio": int(len(principal)),
        "compradores_multi_municipio": int(len(multi)),
        "municipios_unicos_para_siconfi": int(municipios["municipio_ibge"].nunique()),
        "municipios_cache_sucesso_total": int(len(cache)),
        "municipios_ja_coletados_reutilizados": int(len(current & cache)),
        "municipios_novos_para_coleta": int(len(delta)),
        "fontes_cache": cache_by_source,
        "regra_cache": "Município é considerado coletado somente se houver DCA-Anexo I-D com status ok em uma coleta anterior.",
        "regra_integracao": "Integração fiscal principal requer exatamente um municipio_ibge observado por CNPJ comprador na coorte PNCP acumulada assinada em 2025.",
    }
    (out / "resumo_mapeamento.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
