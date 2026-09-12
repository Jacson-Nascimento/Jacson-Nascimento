#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import gzip
import math
import numpy as np
import matplotlib.pyplot as plt

THIS = Path(__file__).resolve()
SECOND = THIS.parents[1]
ROOT = SECOND.parent
DATA = ROOT / "data"
OUT = SECOND / "outputs" / "generated"
FIG = SECOND / "figures" / "generated"
EXPECTED = SECOND / "outputs" / "expected"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

N = 60
THETA = -1.0
TAU = 0.80

def read_matrix_csv(path: Path) -> np.ndarray:
    return np.loadtxt(path, delimiter=",", skiprows=1, usecols=range(1, N + 1))

def read_agents(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    h = np.array([float(r["h"]) for r in rows])
    sigma = np.array([float(r["sigma"]) for r in rows])
    role = np.array([r["role"] for r in rows], dtype=object)
    return role, h, sigma

def read_raw(path: Path):
    ids, n_correct, frac, agg, seed_wrong, evidence = [], [], [], [], [], []
    with gzip.open(path, "rt", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        e0 = header.index("e_001")
        for row in reader:
            ids.append(int(row[0]))
            n_correct.append(int(row[1]))
            frac.append(float(row[2]))
            agg.append(float(row[3]))
            seed_wrong.append(int(row[4]))
            evidence.append([float(x) for x in row[e0:e0 + N]])
    return (
        np.asarray(ids),
        np.asarray(n_correct),
        np.asarray(frac),
        np.asarray(agg),
        np.asarray(seed_wrong, dtype=bool),
        np.asarray(evidence),
    )

def stationary_pi(W: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eig(W.T)
    idx = np.argmin(np.abs(vals - 1.0))
    p = np.real(vecs[:, idx])
    if p.sum() < 0:
        p = -p
    return p / p.sum()

def herd_outcome(E: np.ndarray, W: np.ndarray, beta: float, c: float):
    lam = 0.80 - beta
    I = np.eye(N)
    transfer = lam * (1 - c) * np.linalg.inv(
        (lam + beta) * I - (beta + lam * c) * W
    )
    Y = E @ transfer.T
    frac_wrong = (np.sign(Y) != np.sign(THETA)).mean(axis=1)
    herd = frac_wrong >= TAU
    return frac_wrong, herd

def auc_rank(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    order = np.argsort(score, kind="mergesort")
    sorted_score = score[order]
    ranks = np.empty(len(score), dtype=float)
    i = 0
    while i < len(score):
        j = i + 1
        while j < len(score) and sorted_score[j] == sorted_score[i]:
            j += 1
        avg = (i + 1 + j) / 2.0
        ranks[order[i:j]] = avg
        i = j
    n1 = int((y == 1).sum())
    n0 = int((y == 0).sum())
    return (ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0)

def logistic_newton(X: np.ndarray, y: np.ndarray, max_iter: int = 100, tol: float = 1e-10):
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(max_iter):
        eta = np.clip(X @ b, -35, 35)
        p = 1 / (1 + np.exp(-eta))
        w = np.maximum(p * (1 - p), 1e-12)
        grad = X.T @ (y - p)
        hess = -(X.T * w) @ X
        step = np.linalg.solve(hess, grad)
        b_new = b - step
        if np.max(np.abs(b_new - b)) < tol:
            b = b_new
            break
        b = b_new
    p = 1 / (1 + np.exp(-np.clip(X @ b, -35, 35)))
    return b, p

def write_csv(path: Path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

def fmt(x):
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, str):
        return x
    return f"{float(x):.12f}"

def validate_csv(actual: Path, expected: Path, key_cols=1, tol=1e-9):
    with actual.open(newline="", encoding="utf-8") as fa, expected.open(newline="", encoding="utf-8") as fe:
        a = list(csv.reader(fa))
        e = list(csv.reader(fe))
    if a[0] != e[0] or len(a) != len(e):
        raise SystemExit(f"Schema/row mismatch: {actual.name}")
    for i, (ra, re) in enumerate(zip(a[1:], e[1:]), start=2):
        if ra[:key_cols] != re[:key_cols]:
            raise SystemExit(f"Key mismatch {actual.name} row {i}: {ra[:key_cols]} != {re[:key_cols]}")
        for j, (xa, xe) in enumerate(zip(ra[key_cols:], re[key_cols:]), start=key_cols + 1):
            try:
                if abs(float(xa) - float(xe)) > tol:
                    raise SystemExit(f"Value mismatch {actual.name} row {i} col {j}: {xa} != {xe}")
            except ValueError:
                if xa != xe:
                    raise SystemExit(f"Text mismatch {actual.name} row {i} col {j}: {xa} != {xe}")

def main(validate=False):
    role, h, sigma = read_agents(DATA / "agents_metadata.csv")
    A = read_matrix_csv(DATA / "network_baseline_A.csv")
    W = read_matrix_csv(DATA / "network_baseline_W.csv")
    _, _, frac_correct, seed_aggregate_archived, seed_wrong_archived, E = read_raw(DATA / "monte_carlo_10000_raw.csv.gz")

    pi = stationary_pi(W)
    seed_aggregate = E @ pi
    seed_wrong = np.sign(seed_aggregate) != np.sign(THETA)
    if not np.array_equal(seed_wrong, seed_wrong_archived):
        raise SystemExit("Archived seed indicator differs from recomputation.")
    if np.max(np.abs(seed_aggregate - seed_aggregate_archived)) > 1e-10:
        raise SystemExit("Archived seed aggregate differs from recomputation.")

    correct = np.sign(E) == np.sign(THETA)
    executive_wrong = ~correct[:, 0]
    manager_wrong_count = (~correct[:, 1:6]).sum(axis=1)
    senior_wrong_count = (~correct[:, 6:18]).sum(axis=1)
    other_wrong_count = (~correct[:, 18:60]).sum(axis=1)

    _, herd_7090 = herd_outcome(E, W, 0.70, 0.90)
    _, herd_7595 = herd_outcome(E, W, 0.75, 0.95)
    margin = seed_aggregate[seed_wrong]

    summary = [
        ("mean_fraction_correct", frac_correct.mean()),
        ("minimum_fraction_correct", frac_correct.min()),
        ("wrong_seed_count", seed_wrong.sum()),
        ("wrong_seed_probability", seed_wrong.mean()),
        ("executive_stationary_weight", pi[0]),
        ("top6_stationary_weight", pi[:6].sum()),
        ("effective_number_sources", 1 / np.sum(pi ** 2)),
        ("P_seed_wrong_given_executive_wrong", seed_wrong[executive_wrong].mean()),
        ("P_seed_wrong_given_executive_correct", seed_wrong[~executive_wrong].mean()),
        ("P_executive_wrong_given_seed_wrong", executive_wrong[seed_wrong].mean()),
        ("median_fraction_correct_given_seed_wrong", np.median(frac_correct[seed_wrong])),
        ("P_frac_correct_ge_080_given_seed_wrong", (frac_correct[seed_wrong] >= 0.80).mean()),
        ("P_frac_correct_ge_085_given_seed_wrong", (frac_correct[seed_wrong] >= 0.85).mean()),
        ("P_frac_correct_ge_090_given_seed_wrong", (frac_correct[seed_wrong] >= 0.90).mean()),
        ("executive_to_lower_mean_weight_ratio", pi[0] / pi[18:].mean()),
        ("manager_to_lower_mean_weight_ratio", pi[1:6].mean() / pi[18:].mean()),
        ("auc_margin_b070_c090", auc_rank(herd_7090[seed_wrong], margin)),
        ("auc_margin_b075_c095", auc_rank(herd_7595[seed_wrong], margin)),
    ]
    write_csv(OUT / "summary.csv", ["metric", "value"], [{"metric": k, "value": fmt(v)} for k, v in summary])

    groups = [
        ("executivo", np.arange(0, 1)),
        ("gestores", np.arange(1, 6)),
        ("seniores", np.arange(6, 18)),
        ("demais", np.arange(18, 60)),
    ]
    contribution = E * pi[np.newaxis, :]
    group_rows = []
    for name, idx in groups:
        total_c = contribution[:, idx].sum(axis=1)
        group_rows.append({
            "group": name,
            "n_agents": len(idx),
            "sigma": fmt(sigma[idx[0]]),
            "fraction_correct": fmt(correct[:, idx].mean()),
            "stationary_weight_total": fmt(pi[idx].sum()),
            "stationary_weight_mean": fmt(pi[idx].mean()),
            "mean_contribution_seed_correct": fmt(total_c[~seed_wrong].mean()),
            "mean_contribution_seed_wrong": fmt(total_c[seed_wrong].mean()),
        })
    write_csv(OUT / "group_decomposition.csv", list(group_rows[0].keys()), group_rows)

    manager_rows = []
    for k in range(6):
        mask = executive_wrong & (manager_wrong_count == k)
        manager_rows.append({
            "manager_wrong_count": k,
            "n_replicates": int(mask.sum()),
            "P_seed_wrong_given_executive_wrong": fmt(seed_wrong[mask].mean()),
        })
    write_csv(OUT / "manager_conditional.csv", list(manager_rows[0].keys()), manager_rows)

    kappa_rows = []
    for kappa in range(6):
        multiplier = np.exp(kappa * h)
        Wk = A * multiplier[np.newaxis, :]
        Wk = Wk / Wk.sum(axis=1, keepdims=True)
        pik = stationary_pi(Wk)
        Sk = np.sign(E @ pik) != np.sign(THETA)
        kappa_rows.append({
            "kappa": kappa,
            "P_seed_wrong": fmt(Sk.mean()),
            "n_eff": fmt(1 / np.sum(pik ** 2)),
            "executive_weight": fmt(pik[0]),
            "top6_weight": fmt(pik[:6].sum()),
            "wrong_seed_count": int(Sk.sum()),
        })
    write_csv(OUT / "kappa_counterfactual.csv", list(kappa_rows[0].keys()), kappa_rows)

    edges = np.quantile(margin, np.linspace(0, 1, 6), method="linear")
    quintile = np.digitize(margin, edges[1:-1], right=True) + 1
    margin_rows = []
    for q in range(1, 6):
        mask = quintile == q
        margin_rows.append({
            "quintile": q,
            "n": int(mask.sum()),
            "mean_margin": fmt(margin[mask].mean()),
            "P_herd_b070_c090": fmt(herd_7090[seed_wrong][mask].mean()),
            "P_herd_b075_c095": fmt(herd_7595[seed_wrong][mask].mean()),
            "min_margin": fmt(margin[mask].min()),
            "max_margin": fmt(margin[mask].max()),
        })
    write_csv(OUT / "margin_quintiles.csv", list(margin_rows[0].keys()), margin_rows)

    X = np.column_stack([
        np.ones(len(E)),
        executive_wrong.astype(float),
        manager_wrong_count,
        senior_wrong_count,
        other_wrong_count,
    ])
    coef, pred = logistic_newton(X, seed_wrong.astype(int))
    names = ["intercept", "executive_wrong", "manager_wrong_count", "senior_wrong_count", "other_wrong_count"]
    log_rows = [{"term": n, "coefficient": fmt(b), "odds_ratio": fmt(math.exp(b))} for n, b in zip(names, coef)]
    log_rows.append({"term": "model_auc", "coefficient": "", "odds_ratio": fmt(auc_rank(seed_wrong.astype(int), pred))})
    write_csv(OUT / "logistic_diagnostic.csv", ["term", "coefficient", "odds_ratio"], log_rows)

    kp = np.array([float(r["kappa"]) for r in kappa_rows])
    ps = np.array([float(r["P_seed_wrong"]) for r in kappa_rows])
    ne = np.array([float(r["n_eff"]) for r in kappa_rows])

    plt.figure(figsize=(8, 5))
    plt.plot(kp, ps * 100, marker="o")
    plt.xlabel("Hierarchical sensitivity (kappa)")
    plt.ylabel("Wrong structural seed (%)")
    plt.title("Informational reversal under increasing hierarchical concentration")
    plt.tight_layout()
    plt.savefig(FIG / "figure1_kappa_seed_wrong.png", dpi=200)
    plt.savefig(FIG / "figure1_kappa_seed_wrong.svg")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(kp, ne, marker="o")
    plt.xlabel("Hierarchical sensitivity (kappa)")
    plt.ylabel("Effective number of sources (n_eff)")
    plt.title("Effective informational diversity")
    plt.tight_layout()
    plt.savefig(FIG / "figure2_kappa_neff.png", dpi=200)
    plt.savefig(FIG / "figure2_kappa_neff.svg")
    plt.close()

    qx = np.arange(1, 6)
    p1 = np.array([float(r["P_herd_b070_c090"]) for r in margin_rows]) * 100
    p2 = np.array([float(r["P_herd_b075_c095"]) for r in margin_rows]) * 100
    width = 0.36
    plt.figure(figsize=(8, 5))
    plt.bar(qx - width / 2, p1, width, label="beta=0.70, c=0.90")
    plt.bar(qx + width / 2, p2, width, label="beta=0.75, c=0.95")
    plt.xlabel("Wrong-seed margin quintile")
    plt.ylabel("P(herd | wrong seed) (%)")
    plt.title("Wrong-seed intensity and subsequent amplification")
    plt.xticks(qx)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "figure3_margin_herd.png", dpi=200)
    plt.savefig(FIG / "figure3_margin_herd.svg")
    plt.close()

    if validate:
        validate_csv(OUT / "summary.csv", EXPECTED / "summary.csv", key_cols=1)
        validate_csv(OUT / "group_decomposition.csv", EXPECTED / "group_decomposition.csv", key_cols=2)
        validate_csv(OUT / "manager_conditional.csv", EXPECTED / "manager_conditional.csv", key_cols=2)
        validate_csv(OUT / "kappa_counterfactual.csv", EXPECTED / "kappa_counterfactual.csv", key_cols=1)
        validate_csv(OUT / "margin_quintiles.csv", EXPECTED / "margin_quintiles.csv", key_cols=2)
        validate_csv(OUT / "logistic_diagnostic.csv", EXPECTED / "logistic_diagnostic.csv", key_cols=1, tol=1e-7)
        print("All complementary-analysis controls reproduced successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    main(validate=args.validate)
