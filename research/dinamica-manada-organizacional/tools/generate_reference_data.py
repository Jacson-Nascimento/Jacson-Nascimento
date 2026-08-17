#!/usr/bin/env python3
"""Generate the exact reference realization used by the validated baseline experiment.

This script is intentionally limited to the baseline Monte Carlo design and the four
parameter points reported in Table 5. It generates the large raw tables locally so
that GitHub does not need to version the full 10,000 x 60 simulation matrix.
"""

from pathlib import Path
import csv
import gzip
import math
import numpy as np
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

N = 60
THETA = -1.0
RHO = 0.20
KAPPA = 5.0
SEED = 20260816
N_REP = 10_000
TAU = 0.80

H = np.array([1.00] + [0.65] * 5 + [0.30] * 12 + [0.00] * 42, dtype=float)
ROLES = ["executivo"] + ["gestor"] * 5 + ["senior"] * 12 + ["demais"] * 42
SIGMA = 0.90 + H
Q = 1.0 / SIGMA**2


def stationary_pi(W: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eig(W.T)
    idx = np.argmin(np.abs(vals - 1.0))
    p = np.real(vecs[:, idx])
    if p.sum() < 0:
        p = -p
    return p / p.sum()


def make_network() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    graph = nx.watts_strogatz_graph(N, 6, 0.12, seed=SEED)
    A = nx.to_numpy_array(graph, nodelist=range(N), dtype=float)
    np.fill_diagonal(A, 1.0)  # auto-influence required for exact reproduction

    multiplier = np.exp(KAPPA * H)
    W = A * multiplier[np.newaxis, :]
    W = W / W.sum(axis=1, keepdims=True)
    pi = stationary_pi(W)
    return A, W, pi


def write_agents(pi: np.ndarray) -> None:
    with (DATA / "agents_metadata.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["agent_id", "role", "h", "sigma", "q", "pi_baseline"])
        for i in range(N):
            w.writerow([
                i + 1,
                ROLES[i],
                f"{H[i]:.8f}",
                f"{SIGMA[i]:.8f}",
                f"{Q[i]:.12f}",
                f"{pi[i]:.15f}",
            ])


def write_matrix(path: Path, prefix: str, M: np.ndarray, integer: bool = False) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["agent_id"] + [f"{prefix}_{j+1:03d}" for j in range(N)])
        for i in range(N):
            if integer:
                row = [int(x) for x in M[i]]
            else:
                row = [f"{x:.15f}" for x in M[i]]
            w.writerow([i + 1] + row)


def wilson(x: int, n: int) -> tuple[float, float]:
    z = 1.959963984540054
    p = x / n
    den = 1 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, center - half), min(1.0, center + half)


def main() -> None:
    A, W, pi = make_network()
    write_agents(pi)
    write_matrix(DATA / "network_baseline_A.csv", "a", A, integer=True)
    write_matrix(DATA / "network_baseline_W.csv", "w", W)

    rng = np.random.default_rng(SEED)
    eps = rng.normal(size=(N_REP, N)) * SIGMA[np.newaxis, :]
    E = THETA + eps

    correct = np.sign(E) == np.sign(THETA)
    n_correct = correct.sum(axis=1)
    frac_correct = correct.mean(axis=1)
    seed_aggregate = E @ pi
    seed_wrong = np.sign(seed_aggregate) != np.sign(THETA)

    raw_path = DATA / "monte_carlo_10000_raw.csv.gz"
    with gzip.open(raw_path, "wt", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "replicate_id",
            "n_correct_signals",
            "frac_correct_signals",
            "seed_aggregate_pi_e",
            "seed_wrong",
        ] + [f"e_{j+1:03d}" for j in range(N)])
        for r in range(N_REP):
            w.writerow([
                r + 1,
                int(n_correct[r]),
                f"{frac_correct[r]:.12f}",
                f"{seed_aggregate[r]:.15f}",
                int(seed_wrong[r]),
            ] + [f"{x:.15f}" for x in E[r]])

    scenarios = [
        (0.30, 0.30, "b030_c030"),
        (0.50, 0.60, "b050_c060"),
        (0.70, 0.90, "b070_c090"),
        (0.75, 0.95, "b075_c095"),
    ]

    I = np.eye(N)
    outcomes = {}
    for beta, c, label in scenarios:
        lam = 0.80 - beta
        transfer = lam * (1 - c) * np.linalg.inv(
            (lam + beta) * I - (beta + lam * c) * W
        )
        Y = E @ transfer.T
        frac_wrong = (np.sign(Y) != np.sign(THETA)).mean(axis=1)
        herd = frac_wrong >= TAU
        outcomes[label] = (frac_wrong, herd)

    with gzip.open(DATA / "monte_carlo_10000_outcomes.csv.gz", "wt", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        header = ["replicate_id", "seed_wrong"]
        for _, _, label in scenarios:
            header += [f"{label}_frac_wrong_final", f"{label}_herd80"]
        w.writerow(header)
        for r in range(N_REP):
            row = [r + 1, int(seed_wrong[r])]
            for _, _, label in scenarios:
                frac_wrong, herd = outcomes[label]
                row += [f"{frac_wrong[r]:.12f}", int(herd[r])]
            w.writerow(row)

    n_eff = 1.0 / np.sum(pi**2)
    print(f"mean_fraction_correct={frac_correct.mean():.12f}")
    print(f"minimum_fraction_correct={frac_correct.min():.12f}")
    print(f"wrong_seed_count={int(seed_wrong.sum())}")
    print(f"wrong_seed_probability={seed_wrong.mean():.12f}")
    print(f"executive_stationary_weight={pi[0]:.15f}")
    print(f"top6_stationary_weight={pi[:6].sum():.15f}")
    print(f"effective_number_sources={n_eff:.15f}")

    nS = int(seed_wrong.sum())
    for beta, c, label in scenarios:
        herd = outcomes[label][1]
        x = int(herd[seed_wrong].sum())
        lo, hi = wilson(x, nS)
        print(
            f"beta={beta:.2f}, c={c:.2f}, count={x}, "
            f"P(H|S)={x/nS:.12f}, Wilson95=({lo:.12f},{hi:.12f}), "
            f"P(H)={herd.mean():.12f}"
        )


if __name__ == "__main__":
    main()
