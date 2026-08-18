#!/usr/bin/env python3
"""Integra SICONFI/DCA à coorte PNCP acumulada usando cache cumulativa.

Combina a coleta-base jan-fev e todos os deltas mensais disponíveis de março até
o mês solicitado. Usa a amostra GLOBAL vigente e preserva a interpretação
associativa/descritiva.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def num(s):
    return pd.to_numeric(s, errors="coerce")


def norm_ibge(s: pd.Series) -> pd.Series:
    return s.astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(7)


def corr(df, a, b):
    z = df[[a, b]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(z) < 3:
        return {"rho": None, "p": None, "n": int(len(z))}
    rho, p = spearmanr(z[a], z[b])
    return {"rho": float(rho), "p": float(p), "n": int(len(z))}


def read_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, dtype={"cod_ibge": "string", "_municipio_consulta": "string"}, low_memory=False)


def collection_paths(month: int) -> list[Path]:
    paths = [RES / "siconfi_integracao_jan_fev_2025" / "coleta" / "siconfi_dca_2025.csv.gz"]
    for m in range(3, month + 1):
        paths.append(RES / f"siconfi_integracao_acumulada_2025_{m:02d}" / "coleta_delta" / "siconfi_dca_2025.csv.gz")
    return paths


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--month", type=int, required=True, choices=range(3, 13))
    args = p.parse_args()
    month = args.month
    out = RES / f"siconfi_integracao_acumulada_2025_{month:02d}"
    map_path = out / "compradores_integracao_principal.csv"

    paths = collection_paths(month)
    loaded = []
    source_rows = {}
    for path in paths:
        d = read_if_exists(path)
        if not d.empty:
            loaded.append(d)
            source_rows[str(path.relative_to(ROOT))] = int(len(d))
    if not loaded:
        raise RuntimeError("Nenhuma coleta SICONFI disponível para integração.")
    d = pd.concat(loaded, ignore_index=True, sort=False)

    for c in ["cod_ibge", "_municipio_consulta"]:
        if c in d.columns:
            d[c] = norm_ibge(d[c])
    if "cod_ibge" not in d.columns:
        raise RuntimeError("Coleta SICONFI sem coluna cod_ibge.")

    preferred_keys = [c for c in ["cod_ibge", "anexo", "cod_conta", "conta", "coluna", "exercicio"] if c in d.columns]
    before_dedup = len(d)
    d = d.drop_duplicates(preferred_keys, keep="last") if preferred_keys else d.drop_duplicates()
    duplicates_removed = before_dedup - len(d)

    d["valor_num"] = num(d["valor"])
    d["populacao_num"] = num(d["populacao"])
    idd = d[d["anexo"].astype(str).eq("DCA-Anexo I-D")].copy()
    total = idd[idd["cod_conta"].astype(str).eq("TotalDespesas")].copy()
    pivot = total.pivot_table(index="cod_ibge", columns="coluna", values="valor_num", aggfunc="first").reset_index()
    rename = {
        "Despesas Empenhadas": "despesa_empenhada_2025",
        "Despesas Liquidadas": "despesa_liquidada_2025",
        "Despesas Pagas": "despesa_paga_2025",
    }
    pivot = pivot.rename(columns=rename)
    keep = ["cod_ibge"] + [c for c in rename.values() if c in pivot.columns]
    fiscal = pivot[keep].copy()
    pop = d.groupby("cod_ibge", dropna=False)["populacao_num"].max().rename("populacao_siconfi_2025").reset_index()
    fiscal = fiscal.merge(pop, on="cod_ibge", how="outer")
    for c in rename.values():
        if c not in fiscal.columns:
            fiscal[c] = np.nan
    fiscal["liquidada_sobre_empenhada"] = fiscal["despesa_liquidada_2025"] / fiscal["despesa_empenhada_2025"]
    fiscal["paga_sobre_empenhada"] = fiscal["despesa_paga_2025"] / fiscal["despesa_empenhada_2025"]
    fiscal["despesa_empenhada_per_capita"] = fiscal["despesa_empenhada_2025"] / fiscal["populacao_siconfi_2025"]
    fiscal.to_csv(out / "variaveis_fiscais_municipais_2025.csv", index=False, encoding="utf-8-sig")

    buyers = pd.read_csv(map_path, dtype={"orgao_cnpj": "string", "municipio_ibge": "string"}, low_memory=False)
    buyers["municipio_ibge"] = norm_ibge(buyers["municipio_ibge"])
    x = buyers.merge(fiscal, left_on="municipio_ibge", right_on="cod_ibge", how="left", validate="many_to_one")

    numeric_cols = [
        "valor_total", "portfolio_hhi", "portfolio_hhi_norm", "count_hhi", "count_hhi_norm",
        "n_fornecedores", "n_instrumentos", "exposicao_strength_global", "exposicao_degree_global"
    ]
    for c in numeric_cols:
        if c in x.columns:
            x[c] = num(x[c])
    if "portfolio_hhi_norm" not in x.columns:
        x["portfolio_hhi_norm"] = np.where(
            x["n_fornecedores"] > 1,
            (x["portfolio_hhi"] - 1 / x["n_fornecedores"]) / (1 - 1 / x["n_fornecedores"]), np.nan,
        )
    if "count_hhi_norm" not in x.columns:
        x["count_hhi_norm"] = np.where(
            x["n_fornecedores"] > 1,
            (x["count_hhi"] - 1 / x["n_fornecedores"]) / (1 - 1 / x["n_fornecedores"]), np.nan,
        )
    if "exposicao_strength_global" in x.columns:
        x["exposicao_strength"] = x["exposicao_strength_global"]
    if "exposicao_degree_global" in x.columns:
        x["exposicao_degree"] = x["exposicao_degree_global"]

    x["procurement_intensity_parcial"] = x["valor_total"] / x["despesa_empenhada_2025"]
    x["log_despesa_empenhada"] = np.log(x["despesa_empenhada_2025"].where(x["despesa_empenhada_2025"] > 0))
    x["log_populacao_siconfi"] = np.log(x["populacao_siconfi_2025"].where(x["populacao_siconfi_2025"] > 0))
    x["log_despesa_per_capita"] = np.log(x["despesa_empenhada_per_capita"].where(x["despesa_empenhada_per_capita"] > 0))
    x["instrumentos_por_fornecedor"] = x["n_instrumentos"] / x["n_fornecedores"]
    panel_path = out / f"painel_compradores_pncp_siconfi_2025_{month:02d}.csv"
    x.to_csv(panel_path, index=False, encoding="utf-8-sig")

    correlations = {
        "hhi_norm_vs_log_despesa": corr(x, "portfolio_hhi_norm", "log_despesa_empenhada"),
        "hhi_norm_vs_log_populacao": corr(x, "portfolio_hhi_norm", "log_populacao_siconfi"),
        "hhi_norm_vs_log_despesa_per_capita": corr(x, "portfolio_hhi_norm", "log_despesa_per_capita"),
        "hhi_norm_vs_procurement_intensity_parcial": corr(x, "portfolio_hhi_norm", "procurement_intensity_parcial"),
        "exposicao_strength_vs_log_despesa": corr(x, "exposicao_strength", "log_despesa_empenhada"),
        "exposicao_strength_vs_log_populacao": corr(x, "exposicao_strength", "log_populacao_siconfi"),
        "exposicao_strength_vs_log_despesa_per_capita": corr(x, "exposicao_strength", "log_despesa_per_capita"),
    }
    pd.DataFrame([{"variaveis": k, **v} for k, v in correlations.items()]).to_csv(
        out / "correlacoes_fiscais_diagnosticas.csv", index=False, encoding="utf-8-sig"
    )

    coverage = int(x["despesa_empenhada_2025"].notna().sum())
    pi = x["procurement_intensity_parcial"].replace([np.inf, -np.inf], np.nan).dropna()
    resumo = {
        "mes_final_publicacao": f"2025-{month:02d}",
        "especificacao_metricas": "global",
        "compradores_integracao_principal": int(len(x)),
        "compradores_com_despesa_empenhada": coverage,
        "cobertura_despesa_empenhada_pct": float(coverage / max(len(x), 1) * 100),
        "municipios_fiscais_com_total_despesa": int(fiscal["despesa_empenhada_2025"].notna().sum()),
        "registros_siconfi_antes_dedup": int(before_dedup),
        "registros_siconfi_consolidados": int(len(d)),
        "duplicidades_siconfi_removidas": int(duplicates_removed),
        "fontes_coleta_e_registros": source_rows,
        "procurement_intensity_parcial_mediana": None if pi.empty else float(pi.median()),
        "procurement_intensity_parcial_p95": None if pi.empty else float(pi.quantile(.95)),
        "procurement_intensity_parcial_max": None if pi.empty else float(pi.max()),
        "correlacoes_spearman": correlations,
        "nota": "ProcurementIntensity parcial usa instrumentos assinados em 2025 e publicados até o mês de corte; é diagnóstico de escala e não medida de execução orçamentária. Associações não são causais.",
    }
    (out / "resumo_integracao_fiscal.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
