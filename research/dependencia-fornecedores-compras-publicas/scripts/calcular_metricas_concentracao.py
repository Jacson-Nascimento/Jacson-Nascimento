#!/usr/bin/env python3
"""Calcula métricas de concentração e exposição de rede a partir da base PNCP tratada.

Entrada mínima esperada:
- municipio_ibge
- categoria
- ano_assinatura
- fornecedor_id_limpo
- valorInicial

Saídas:
- relacoes_comprador_fornecedor.csv
- metricas_mercado.csv
- metricas_fornecedor.csv
"""

import argparse
import math
from pathlib import Path
import pandas as pd


def _entropy(shares: pd.Series) -> float:
    vals = shares[shares > 0].astype(float)
    if vals.empty:
        return float("nan")
    return float(-(vals * vals.map(math.log)).sum())


def _market_metrics(group: pd.DataFrame) -> pd.Series:
    vals = group["valor_relacao"].astype(float)
    total = vals.sum()
    if total <= 0:
        return pd.Series(dtype=float)
    shares = vals / total
    shares_sorted = shares.sort_values(ascending=False)
    hhi = float((shares ** 2).sum())
    n = int(len(shares))
    entropy = _entropy(shares)
    entropy_norm = entropy / math.log(n) if n > 1 else 0.0
    return pd.Series({
        "valor_total": total,
        "n_fornecedores": n,
        "hhi": hhi,
        "hhi_10000": hhi * 10000,
        "cr1": float(shares_sorted.iloc[0]),
        "cr4": float(shares_sorted.iloc[:4].sum()),
        "n_efetivo": (1.0 / hhi) if hhi > 0 else float("nan"),
        "entropia": entropy,
        "entropia_normalizada": entropy_norm,
    })


def calculate(df: pd.DataFrame):
    required = {
        "municipio_ibge", "categoria", "ano_assinatura",
        "fornecedor_id_limpo", "valorInicial"
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")

    x = df.copy()
    x["valorInicial"] = pd.to_numeric(x["valorInicial"], errors="coerce")
    x = x[
        x["municipio_ibge"].notna()
        & x["categoria"].notna()
        & x["ano_assinatura"].notna()
        & x["fornecedor_id_limpo"].notna()
        & x["valorInicial"].gt(0)
    ].copy()

    market_keys = ["municipio_ibge", "categoria", "ano_assinatura"]
    relation_keys = market_keys + ["fornecedor_id_limpo"]

    relations = (
        x.groupby(relation_keys, dropna=False)
        .agg(valor_relacao=("valorInicial", "sum"), n_instrumentos=("valorInicial", "size"))
        .reset_index()
    )

    totals = relations.groupby(market_keys)["valor_relacao"].transform("sum")
    relations["share_fornecedor"] = relations["valor_relacao"] / totals

    markets = (
        relations.groupby(market_keys, group_keys=False)
        .apply(_market_metrics, include_groups=False)
        .reset_index()
    )

    # Métricas do fornecedor dentro de categoria e ano.
    supplier_keys = ["categoria", "ano_assinatura", "fornecedor_id_limpo"]
    suppliers = (
        relations.groupby(supplier_keys)
        .agg(
            degree=("municipio_ibge", "nunique"),
            strength=("valor_relacao", "sum"),
        )
        .reset_index()
    )

    buyer_counts = (
        relations.groupby(["categoria", "ano_assinatura"])["municipio_ibge"]
        .nunique()
        .rename("n_compradores_categoria")
        .reset_index()
    )
    suppliers = suppliers.merge(buyer_counts, on=["categoria", "ano_assinatura"], how="left")
    suppliers["reach"] = suppliers["degree"] / suppliers["n_compradores_categoria"]

    # Percentis de centralidade para exposição do comprador.
    suppliers["pct_degree"] = suppliers.groupby(["categoria", "ano_assinatura"])["degree"].rank(pct=True, method="average")
    suppliers["pct_strength"] = suppliers.groupby(["categoria", "ano_assinatura"])["strength"].rank(pct=True, method="average")

    rel2 = relations.merge(
        suppliers[["categoria", "ano_assinatura", "fornecedor_id_limpo", "pct_degree", "pct_strength"]],
        on=["categoria", "ano_assinatura", "fornecedor_id_limpo"],
        how="left",
    )
    rel2["exp_degree_parcela"] = rel2["share_fornecedor"] * rel2["pct_degree"]
    rel2["exp_strength_parcela"] = rel2["share_fornecedor"] * rel2["pct_strength"]

    exposures = (
        rel2.groupby(market_keys)
        .agg(
            exposicao_degree=("exp_degree_parcela", "sum"),
            exposicao_strength=("exp_strength_parcela", "sum"),
        )
        .reset_index()
    )
    markets = markets.merge(exposures, on=market_keys, how="left")

    return rel2, markets, suppliers


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_csv")
    p.add_argument("--out", default="results")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input_csv, dtype={"municipio_ibge": "string", "fornecedor_id_limpo": "string"})
    rel, markets, suppliers = calculate(df)
    rel.to_csv(out / "relacoes_comprador_fornecedor.csv", index=False, encoding="utf-8-sig")
    markets.to_csv(out / "metricas_mercado.csv", index=False, encoding="utf-8-sig")
    suppliers.to_csv(out / "metricas_fornecedor.csv", index=False, encoding="utf-8-sig")
    print(markets.describe(include="all").to_string())


if __name__ == "__main__":
    main()
