#!/usr/bin/env python3
"""Constrói a base canônica limpa a partir da V13 arquivística.

A V13 reproduz as tabelas finais da dissertação. Esta rotina preserva a coluna original
ROA_arquivistico e corrige a definição de ROA removendo o deslocamento +1 identificado
na auditoria histórica.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd

EXPECTED_SHA256 = "058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f"
EXPECTED_ROWS = 3072
EXPECTED_BANKS = 32
EXPECTED_PERIODS = 96


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()

    digest = sha256(args.input)
    if digest != EXPECTED_SHA256:
        raise ValueError(f"SHA-256 inesperado para V13: {digest}")

    df = pd.read_csv(args.input)
    df["Data"] = pd.to_datetime(df["Data"])

    if len(df) != EXPECTED_ROWS:
        raise ValueError(f"Número de linhas inesperado: {len(df)}")
    if df["Instituição"].nunique() != EXPECTED_BANKS:
        raise ValueError("Número de bancos diferente de 32")
    if df["Data"].nunique() != EXPECTED_PERIODS:
        raise ValueError("Número de trimestres diferente de 96")
    if df.duplicated(["Instituição", "Data"]).any():
        raise ValueError("Há duplicidade banco-data")
    if df.isna().any().any():
        raise ValueError("Há valores ausentes na V13")

    df.insert(df.columns.get_loc("ROA") + 1, "ROA_arquivistico", df["ROA"])
    df["ROA"] = df["ROA_arquivistico"] - 1.0

    for field in ["dummy_tp", "dummy_EG", "dummy_EM"]:
        if not set(df[field].unique()).issubset({0, 1}):
            raise ValueError(f"{field} fora de {{0,1}}")

    df = df.sort_values(["Instituição", "Data"]).reset_index(drop=True)
    df["Data"] = df["Data"].dt.strftime("%Y-%m-%d")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)

    manifest = {
        "source_file": args.input.name,
        "source_sha256": digest,
        "rows": len(df),
        "banks": int(df["Instituição"].nunique()),
        "periods": int(pd.to_datetime(df["Data"]).nunique()),
        "corrections": [
            {
                "field": "ROA",
                "rule": "ROA = ROA_arquivistico - 1",
                "reason": "V13 equals 1 + ROA from dataset_2024_3 on 2,852 common bank-quarter observations; dissertation defines ROA as net income / total assets.",
            }
        ],
        "unchanged_macro": {
            "taxa_selic_": "quarterly compounded Selic from monthly series 4390",
            "Taxa_IPCA": "decimal proportion as in V13",
        },
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
