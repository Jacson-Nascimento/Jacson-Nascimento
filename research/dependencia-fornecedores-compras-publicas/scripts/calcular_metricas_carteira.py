#!/usr/bin/env python3
"""Calcula métricas anuais de dependência da carteira de fornecedores.

Unidade principal: comprador institucional (orgao_cnpj) x fornecedor x ano.

Este módulo mede concentração da carteira de fornecedores. Não interpreta HHI
como concentração antitruste de mercado.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
import numpy as np
import pandas as pd


def entropy_normalized(shares: pd.Series) -> float:
    x = pd.to_numeric(shares, errors="coerce").dropna()
    x = x[x > 0]
    n = len(x)
    if n <= 1:
        return 0.0 if n == 1 else float("nan")
    h = float(-(x * np.log(x)).sum())
    return h / math.log(n)


def _validate(df: pd.DataFrame):
    required = {
        "orgao_cnpj", "fornecedor_id_limpo", "ano_assinatura",
        "valorInicial", "id_contrato"
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    _validate(df)
    x = df.copy()
    x["orgao_cnpj"] = x["orgao_cnpj"].astype("string").str.strip()
    x["fornecedor_id_limpo"] = x["fornecedor_id_limpo"].astype("string").str.strip()
    x["ano_assinatura"] = pd.to_numeric(x["ano_assinatura"], errors="coerce").astype("Int64")
    x["valorInicial"] = pd.to_numeric(x["valorInicial"], errors="coerce")
    x = x[
        x["orgao_cnpj"].notna() & x["orgao_cnpj"].ne("")
        & x["fornecedor_id_limpo"].notna() & x["fornecedor_id_limpo"].ne("")
        & x["ano_assinatura"].notna()
        & x["valorInicial"].gt(0)
        & x["id_contrato"].notna()
    ].copy()
    return x


def relations_by_value(x: pd.DataFrame) -> pd.DataFrame:
    keys = ["orgao_cnpj", "ano_assinatura", "fornecedor_id_limpo"]
    rel = (
        x.groupby(keys, dropna=False)
        .agg(
            valor_relacao=("valorInicial", "sum"),
            n_instrumentos=("id_contrato", "nunique"),
        )
        .reset_index()
    )
    total_value = rel.groupby(["orgao_cnpj", "ano_assinatura"])["valor_relacao"].transform("sum")
    total_count = rel.groupby(["orgao_cnpj", "ano_assinatura"])["n_instrumentos"].transform("sum")
    rel["share_valor"] = rel["valor_relacao"] / total_value
    rel["share_contagem"] = rel["n_instrumentos"] / total_count
    return rel


def buyer_metrics(rel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (buyer, year), g in rel.groupby(["orgao_cnpj", "ano_assinatura"], sort=False):
        sv = g["share_valor"].astype(float).sort_values(ascending=False)
        sc = g["share_contagem"].astype(float).sort_values(ascending=False)
        hv = float((sv ** 2).sum())
        hc = float((sc ** 2).sum())
        rows.append({
            "orgao_cnpj": buyer,
            "ano_assinatura": int(year),
            "valor_total": float(g["valor_relacao"].sum()),
            "n_instrumentos": int(g["n_instrumentos"].sum()),
            "n_fornecedores": int(g["fornecedor_id_limpo"].nunique()),
            "portfolio_hhi": hv,
            "portfolio_hhi_10000": hv * 10000,
            "portfolio_cr1": float(sv.iloc[0]),
            "portfolio_cr4": float(sv.iloc[:4].sum()),
            "portfolio_neff": 1.0 / hv if hv > 0 else float("nan"),
            "portfolio_entropy_norm": entropy_normalized(sv),
            "count_hhi": hc,
            "count_hhi_10000": hc * 10000,
            "count_cr1": float(sc.iloc[0]),
            "count_cr4": float(sc.iloc[:4].sum()),
            "count_neff": 1.0 / hc if hc > 0 else float("nan"),
            "count_entropy_norm": entropy_normalized(sc),
            "hhi_gap_value_minus_count": hv - hc,
        })
    return pd.DataFrame(rows)


def category_mix(x: pd.DataFrame) -> pd.DataFrame:
    if "categoria" not in x.columns:
        return pd.DataFrame(columns=["orgao_cnpj", "ano_assinatura", "category_mix_hhi", "n_categorias"])
    z = x[x["categoria"].notna()].copy()
    if z.empty:
        return pd.DataFrame(columns=["orgao_cnpj", "ano_assinatura", "category_mix_hhi", "n_categorias"])
    cat = (
        z.groupby(["orgao_cnpj", "ano_assinatura", "categoria"], dropna=False)["valorInicial"]
        .sum().rename("valor_categoria").reset_index()
    )
    cat["share_categoria"] = cat["valor_categoria"] / cat.groupby(["orgao_cnpj", "ano_assinatura"])["valor_categoria"].transform("sum")
    out = (
        cat.assign(hhi_piece=cat["share_categoria"] ** 2)
        .groupby(["orgao_cnpj", "ano_assinatura"])
        .agg(
            category_mix_hhi=("hhi_piece", "sum"),
            n_categorias=("categoria", "nunique"),
            categoria_cr1=("share_categoria", "max"),
        ).reset_index()
    )
    return out


def shared_procurement(x: pd.DataFrame) -> pd.DataFrame:
    if "origem_externa" not in x.columns:
        return pd.DataFrame(columns=["orgao_cnpj", "ano_assinatura", "shared_procurement_share"])
    z = x.copy()
    ext = z["origem_externa"].astype("string").str.lower().isin(["true", "1", "sim"])
    z["valor_externo"] = np.where(ext, z["valorInicial"], 0.0)
    return (
        z.groupby(["orgao_cnpj", "ano_assinatura"])
        .agg(valor_total_aux=("valorInicial", "sum"), valor_externo=("valor_externo", "sum"))
        .reset_index()
        .assign(shared_procurement_share=lambda d: d["valor_externo"] / d["valor_total_aux"])
        [["orgao_cnpj", "ano_assinatura", "shared_procurement_share"]]
    )


def supplier_network(rel: pd.DataFrame) -> pd.DataFrame:
    suppliers = (
        rel.groupby(["ano_assinatura", "fornecedor_id_limpo"])
        .agg(
            degree=("orgao_cnpj", "nunique"),
            strength=("valor_relacao", "sum"),
        ).reset_index()
    )
    nbuyers = rel.groupby("ano_assinatura")["orgao_cnpj"].nunique().rename("n_compradores_ano").reset_index()
    suppliers = suppliers.merge(nbuyers, on="ano_assinatura", how="left")
    suppliers["reach"] = suppliers["degree"] / suppliers["n_compradores_ano"]
    total = suppliers.groupby("ano_assinatura")["strength"].transform("sum")
    suppliers["system_share"] = suppliers["strength"] / total
    suppliers["pct_degree"] = suppliers.groupby("ano_assinatura")["degree"].rank(pct=True, method="average")
    suppliers["pct_strength"] = suppliers.groupby("ano_assinatura")["strength"].rank(pct=True, method="average")
    return suppliers


def buyer_network_exposure(rel: pd.DataFrame, suppliers: pd.DataFrame) -> pd.DataFrame:
    z = rel.merge(
        suppliers[["ano_assinatura", "fornecedor_id_limpo", "pct_degree", "pct_strength"]],
        on=["ano_assinatura", "fornecedor_id_limpo"], how="left"
    )
    z["e_degree_piece"] = z["share_valor"] * z["pct_degree"]
    z["e_strength_piece"] = z["share_valor"] * z["pct_strength"]
    return (
        z.groupby(["orgao_cnpj", "ano_assinatura"])
        .agg(
            exposicao_degree=("e_degree_piece", "sum"),
            exposicao_strength=("e_strength_piece", "sum"),
        ).reset_index()
    )


def supplier_buyer_hhi(rel: pd.DataFrame) -> pd.DataFrame:
    z = rel.copy()
    totals = z.groupby(["ano_assinatura", "fornecedor_id_limpo"])["valor_relacao"].transform("sum")
    z["buyer_share_supplier"] = z["valor_relacao"] / totals
    z["buyer_hhi_piece"] = z["buyer_share_supplier"] ** 2
    hhi = (
        z.groupby(["ano_assinatura", "fornecedor_id_limpo"])
        .agg(buyer_hhi=("buyer_hhi_piece", "sum"), n_buyers=("orgao_cnpj", "nunique"))
        .reset_index()
    )
    return hhi


def calculate(df: pd.DataFrame):
    x = prepare(df)
    rel = relations_by_value(x)
    buyers = buyer_metrics(rel)
    buyers = buyers.merge(category_mix(x), on=["orgao_cnpj", "ano_assinatura"], how="left")
    buyers = buyers.merge(shared_procurement(x), on=["orgao_cnpj", "ano_assinatura"], how="left")
    suppliers = supplier_network(rel)
    exposure = buyer_network_exposure(rel, suppliers)
    buyers = buyers.merge(exposure, on=["orgao_cnpj", "ano_assinatura"], how="left")
    bilateral = supplier_buyer_hhi(rel)
    suppliers = suppliers.merge(bilateral, on=["ano_assinatura", "fornecedor_id_limpo"], how="left")
    return rel, buyers, suppliers


def main():
    p = argparse.ArgumentParser()
    p.add_argument("inputs", nargs="+", help="CSV ou CSV.GZ processados")
    p.add_argument("--out", default="results/carteira")
    p.add_argument("--year", type=int, default=None)
    args = p.parse_args()

    frames=[]
    for path in args.inputs:
        frames.append(pd.read_csv(path, dtype={"orgao_cnpj":"string", "fornecedor_id_limpo":"string", "municipio_ibge":"string"}))
    df=pd.concat(frames, ignore_index=True)
    if args.year is not None:
        year=pd.to_numeric(df["ano_assinatura"], errors="coerce")
        df=df[year.eq(args.year)].copy()

    out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rel,buyers,suppliers=calculate(df)
    rel.to_csv(out/"relacoes_carteira.csv.gz", index=False, compression="gzip")
    buyers.to_csv(out/"metricas_compradores.csv", index=False, encoding="utf-8-sig")
    suppliers.to_csv(out/"metricas_fornecedores.csv", index=False, encoding="utf-8-sig")
    print(buyers.describe(include="all").to_string())

if __name__ == "__main__":
    main()
