#!/usr/bin/env python3
"""Reprodução independente dos modelos de efeitos fixos da dissertação.

Implementa transformação within por banco e covariância cluster por banco com ajuste
HC1 equivalente ao uso de vcovHC(modelo, type='HC1') no pacote plm.

Uso:
  python 02_reproduzir_modelos.py --data-dir data/raw --output results/auditoria/modelos_reproduzidos.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

ALIASES = {
    "IND_EFICIENCIA": "ieo",
    "Indice_individamento": "iend",
    "Spread Bancário": "spread",
    "Desp_Provisao_At": "dpcdl",
    "PC": "capat",
    "PCC": "ccat",
    "MCAT": "mcat",
    "Taxa_IPCA": "ipca",
    "taxa_selic_": "selic",
    "dummy_EG": "deg",
    "dummy_EM": "dem",
}


def design(df: pd.DataFrame, outcome: str, dynamic: bool):
    d = df.copy()
    d["Data"] = pd.to_datetime(d["Data"])
    d = d.sort_values(["Instituição", "Data"]).reset_index(drop=True)

    if dynamic:
        d[f"{outcome}_lag"] = d.groupby("Instituição", sort=False)[outcome].shift(1)
        d = d.dropna(subset=[f"{outcome}_lag"]).copy()

    cols = {}
    if dynamic:
        cols[f"{outcome.lower()}_lag"] = d[f"{outcome}_lag"]

    for src, alias in ALIASES.items():
        cols[alias] = d[src]

    cols["dpcdl:deg"] = d["Desp_Provisao_At"] * d["dummy_EG"]
    cols["dpcdl:dem"] = d["Desp_Provisao_At"] * d["dummy_EM"]
    cols["dpcdl:dtc"] = d["Desp_Provisao_At"] * d["dummy_tp"]
    cols["iend:deg"] = d["Indice_individamento"] * d["dummy_EG"]
    cols["iend:dem"] = d["Indice_individamento"] * d["dummy_EM"]
    cols["deg:dtc"] = d["dummy_EG"] * d["dummy_tp"]
    cols["dem:dtc"] = d["dummy_EM"] * d["dummy_tp"]
    cols["spread:dtc"] = d["Spread Bancário"] * d["dummy_tp"]
    cols["capat:dtc"] = d["PC"] * d["dummy_tp"]
    cols["ccat:dtc"] = d["PCC"] * d["dummy_tp"]

    X = pd.DataFrame(cols, index=d.index)
    groups = d["Instituição"]
    Xw = X - X.groupby(groups).transform("mean")
    yw = d[outcome] - d.groupby("Instituição")[outcome].transform("mean")

    # dummy_tp em nível é invariável e é absorvida pelos efeitos fixos de banco.
    keep = Xw.columns[Xw.abs().max() > 1e-14]
    return d, Xw[keep], yw


def fit_within_cluster_hc1(df: pd.DataFrame, outcome: str, dynamic: bool):
    d, Xw, yw = design(df, outcome, dynamic)
    X = Xw.to_numpy(dtype=float)
    y = yw.to_numpy(dtype=float)

    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    bread = np.linalg.inv(X.T @ X)

    meat = np.zeros((X.shape[1], X.shape[1]))
    group_arr = d["Instituição"].to_numpy()
    for g in pd.unique(group_arr):
        idx = np.flatnonzero(group_arr == g)
        score = X[idx].T @ resid[idx]
        meat += np.outer(score, score)

    n_obs = len(d)
    k = X.shape[1]
    n_banks = d["Instituição"].nunique()
    df_resid = n_obs - n_banks - k

    # Ajuste HC1 do plm: N/(N-k), sem a correção adicional G/(G-1).
    cov = bread @ meat @ bread * (n_obs / (n_obs - k))
    se = np.sqrt(np.diag(cov))
    tval = beta / se
    pval = 2 * student_t.sf(np.abs(tval), df_resid)

    within_tss = float(y @ y)
    rss = float(resid @ resid)
    r2 = 1 - rss / within_tss
    adj_r2 = 1 - (1 - r2) * (n_obs - 1) / df_resid
    f_stat = (r2 / k) / ((1 - r2) / df_resid)
    total_tss = float(((d[outcome] - d[outcome].mean()) ** 2).sum())

    out = pd.DataFrame({
        "term": Xw.columns,
        "Estimate": beta,
        "Std.Error": se,
        "t.value": tval,
        "p.value": pval,
    })
    stats = {
        "n_obs_effective": n_obs,
        "n_banks": n_banks,
        "n_periods_effective": d["Data"].nunique(),
        "k": k,
        "df_resid": df_resid,
        "total_sum_squares": total_tss,
        "residual_sum_squares": rss,
        "r_squared_within": r2,
        "adj_r_squared": adj_r2,
        "f_statistic": f_stat,
    }
    return out, stats


def run_version(path: Path, version: str):
    df = pd.read_csv(path)
    coef_frames = []
    stat_rows = []
    specs = [
        ("2000-2023", None, False, "ROA"),
        ("2000-2023", None, False, "ROE"),
        ("2000-2023", None, True, "ROA"),
        ("2000-2023", None, True, "ROE"),
        ("2012-2023", "2012-01-01", False, "ROA"),
        ("2012-2023", "2012-01-01", False, "ROE"),
        ("2012-2023", "2012-01-01", True, "ROA"),
        ("2012-2023", "2012-01-01", True, "ROE"),
    ]

    for period, start, dynamic, outcome in specs:
        sub = df.copy()
        sub["Data"] = pd.to_datetime(sub["Data"])
        if start:
            sub = sub[sub["Data"] >= pd.Timestamp(start)].copy()

        coef, stats = fit_within_cluster_hc1(sub, outcome, dynamic)
        coef.insert(0, "outcome", outcome)
        coef.insert(0, "model", "dynamic" if dynamic else "static")
        coef.insert(0, "period", period)
        coef.insert(0, "version", version)
        coef_frames.append(coef)
        stat_rows.append({
            "version": version,
            "period": period,
            "model": "dynamic" if dynamic else "static",
            "outcome": outcome,
            **stats,
        })

    return pd.concat(coef_frames, ignore_index=True), pd.DataFrame(stat_rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stats-output", type=Path, default=None)
    args = parser.parse_args()

    versions = {
        "V11": args.data_dir / "dataset_290624_11.csv",
        "V12": args.data_dir / "dataset_290624_12.csv",
        "V13": args.data_dir / "dataset_290624_13.csv",
    }

    all_coef = []
    all_stats = []
    for version, path in versions.items():
        if not path.exists():
            raise FileNotFoundError(path)
        coef, stats = run_version(path, version)
        all_coef.append(coef)
        all_stats.append(stats)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(all_coef, ignore_index=True).to_csv(args.output, index=False)
    stats_output = args.stats_output or args.output.with_name(args.output.stem + "_stats.csv")
    pd.concat(all_stats, ignore_index=True).to_csv(stats_output, index=False)


if __name__ == "__main__":
    main()
