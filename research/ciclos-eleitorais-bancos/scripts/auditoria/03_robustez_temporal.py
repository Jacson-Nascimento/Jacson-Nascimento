#!/usr/bin/env python3
"""Auditoria de efeitos marginais e robustez temporal do ROA.

Parte da V13 arquivística e executa efeitos marginais, sazonalidade,
recodificação da eleição para T4 e diagnósticos de robustez.
"""
from __future__ import annotations
import argparse, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

GENERAL_ELECTION_YEARS = [2002, 2006, 2010, 2014, 2018, 2022]


def fit_within(df, outcome, dynamic=False, election_var="dummy_EG",
               election_interactions=True, quarter_fe=False, trend_degree=0):
    d = df.copy().sort_values(["Instituição", "Data"]).reset_index(drop=True)
    if dynamic:
        d["y_lag"] = d.groupby("Instituição")[outcome].shift(1)
        d = d.dropna(subset=["y_lag"]).copy()
    cols = {}
    if dynamic:
        cols["y_lag"] = d["y_lag"]
    for source, alias in [
        ("IND_EFICIENCIA", "ieo"), ("Indice_individamento", "iend"),
        ("Spread Bancário", "spread"), ("Desp_Provisao_At", "dpcdl"),
        ("PC", "capat"), ("PCC", "ccat"), ("MCAT", "mcat"),
        ("Taxa_IPCA", "ipca"), ("taxa_selic_", "selic"),
        (election_var, "deg"), ("dummy_EM", "dem")]:
        cols[alias] = d[source]
    if election_interactions:
        cols["dpcdl:deg"] = d["Desp_Provisao_At"] * d[election_var]
        cols["iend:deg"] = d["Indice_individamento"] * d[election_var]
        cols["deg:dtc"] = d[election_var] * d["dummy_tp"]
    cols["dpcdl:dem"] = d["Desp_Provisao_At"] * d["dummy_EM"]
    cols["dpcdl:dtc"] = d["Desp_Provisao_At"] * d["dummy_tp"]
    cols["iend:dem"] = d["Indice_individamento"] * d["dummy_EM"]
    cols["dem:dtc"] = d["dummy_EM"] * d["dummy_tp"]
    cols["spread:dtc"] = d["Spread Bancário"] * d["dummy_tp"]
    cols["capat:dtc"] = d["PC"] * d["dummy_tp"]
    cols["ccat:dtc"] = d["PCC"] * d["dummy_tp"]
    if quarter_fe:
        q = d["Data"].dt.quarter
        for qq in (2, 3, 4):
            cols[f"q{qq}"] = (q == qq).astype(float)
    if trend_degree:
        periods = d["Data"].dt.to_period("Q")
        minimum = periods.min().ordinal
        raw = np.array([p.ordinal - minimum for p in periods], dtype=float)
        z = (raw - raw.mean()) / raw.std()
        for degree in range(1, trend_degree + 1):
            cols[f"trend{degree}"] = z ** degree
    X = pd.DataFrame(cols, index=d.index)
    groups = d["Instituição"]
    Xw = X - X.groupby(groups).transform("mean")
    yw = d[outcome] - d.groupby("Instituição")[outcome].transform("mean")
    Xw = Xw.loc[:, Xw.abs().max() > 1e-14]
    Xn, yn = Xw.to_numpy(float), yw.to_numpy(float)
    beta = np.linalg.lstsq(Xn, yn, rcond=None)[0]
    resid = yn - Xn @ beta
    bread = np.linalg.inv(Xn.T @ Xn)
    meat = np.zeros_like(bread)
    gv = groups.to_numpy()
    for g in pd.unique(gv):
        idx = np.flatnonzero(gv == g)
        score = Xn[idx].T @ resid[idx]
        meat += np.outer(score, score)
    n, k, nb = len(d), Xn.shape[1], d["Instituição"].nunique()
    df_resid = n - nb - k
    cov = bread @ meat @ bread * (n / (n - k))
    se = np.sqrt(np.diag(cov))
    p = 2 * student_t.sf(np.abs(beta / se), df_resid)
    return {"data": d, "columns": Xw.columns,
            "beta": pd.Series(beta, index=Xw.columns),
            "se": pd.Series(se, index=Xw.columns),
            "p": pd.Series(p, index=Xw.columns),
            "cov": cov, "df_resid": df_resid}


def marginal_effect(result, event_column="dummy_EG", sample="all"):
    d = result["data"]
    if sample == "election": d = d[d[event_column] == 1]
    elif sample == "private": d = d[d["dummy_tp"] == 0]
    elif sample == "public": d = d[d["dummy_tp"] == 1]
    columns = result["columns"]
    L = np.zeros(len(columns))
    for name, value in {
        "deg": 1.0,
        "dpcdl:deg": d["Desp_Provisao_At"].mean(),
        "iend:deg": d["Indice_individamento"].mean(),
        "deg:dtc": d["dummy_tp"].mean()}.items():
        if name in columns: L[columns.get_loc(name)] = value
    estimate = float(L @ result["beta"].to_numpy())
    variance = float(L @ result["cov"] @ L)
    se = math.sqrt(max(variance, 0.0))
    p = 2 * student_t.sf(abs(estimate / se), result["df_resid"])
    return estimate, se, p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    df["Data"] = pd.to_datetime(df["Data"])
    df["ROA_clean"] = df["ROA"] - 1.0
    df["year"] = df["Data"].dt.year
    df["quarter"] = df["Data"].dt.quarter
    df["eg_q4"] = (df["year"].isin(GENERAL_ELECTION_YEARS) &
                    (df["quarter"] == 4)).astype(int)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    ame_rows = []
    for dynamic in (False, True):
        r = fit_within(df, "ROA_clean", dynamic=dynamic)
        for sample in ("all", "election", "private", "public"):
            est, se, p = marginal_effect(r, sample=sample)
            ame_rows.append({"model": "dynamic" if dynamic else "static",
                             "sample": sample, "AME": est, "SE": se, "p_value": p})
    pd.DataFrame(ame_rows).to_csv(args.output_dir / "ame_recalculado.csv", index=False)

    seasonal = []
    specs = [(False, 0, "original"), (True, 0, "quarter_FE"),
             (True, 1, "quarter_FE_linear_trend"),
             (True, 2, "quarter_FE_quadratic_trend")]
    for dynamic in (False, True):
        for qfe, trend, label in specs:
            r = fit_within(df, "ROA_clean", dynamic=dynamic,
                           quarter_fe=qfe, trend_degree=trend)
            ame, ame_se, ame_p = marginal_effect(r)
            seasonal.append({"model": "dynamic" if dynamic else "static",
                             "spec": label, "coef_deg": r["beta"]["deg"],
                             "se_deg": r["se"]["deg"], "p_deg": r["p"]["deg"],
                             "AME": ame, "AME_se": ame_se, "AME_p": ame_p})
    pd.DataFrame(seasonal).to_csv(args.output_dir / "sazonalidade_recalculada.csv", index=False)

    event_rows = []
    for dynamic in (False, True):
        for interactions in (False, True):
            r = fit_within(df, "ROA_clean", dynamic=dynamic, election_var="eg_q4",
                           election_interactions=interactions, quarter_fe=True, trend_degree=1)
            if interactions:
                ame, ame_se, ame_p = marginal_effect(r, event_column="eg_q4")
            else:
                ame, ame_se, ame_p = r["beta"]["deg"], r["se"]["deg"], r["p"]["deg"]
            event_rows.append({"model": "dynamic" if dynamic else "static",
                               "interactions": interactions,
                               "coef_event_q4": r["beta"]["deg"],
                               "se_event_q4": r["se"]["deg"],
                               "p_event_q4": r["p"]["deg"],
                               "AME_event_q4": ame, "AME_se": ame_se, "AME_p": ame_p})
    pd.DataFrame(event_rows).to_csv(args.output_dir / "evento_q4_recalculado.csv", index=False)

    agg = df.groupby(["year", "quarter"], as_index=False)["ROA_clean"].mean()
    agg.groupby("quarter", as_index=False)["ROA_clean"].mean().to_csv(
        args.output_dir / "roa_medio_por_trimestre.csv", index=False)


if __name__ == "__main__":
    main()
