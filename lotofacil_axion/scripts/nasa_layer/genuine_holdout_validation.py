#!/usr/bin/env python3
"""Genuine post-freeze validation for the AXION frequency-persistence signal.

Freeze point: contest 3435, the last contest in the dataset used to define and
triage the NASA Signal Analysis Layer frequency-persistence hypothesis.

The post-freeze contests are used only as genuine holdout observations. The
frequency rules evaluated here were fixed from the pre-3436 analysis:
  1. fixed top-15 by cumulative frequency estimated through contest 3435;
  2. rolling top-15 by the immediately preceding 1000 contests.

The script also summarizes the already-generated AXION 0.3 nested temporal
outer predictions for contests after the freeze point.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "lotofacil_history.csv"
OUTER = ROOT / "results" / "outer_predictions.csv"
OUT = ROOT / "results" / "nasa_layer" / "genuine_holdout"
OUT.mkdir(parents=True, exist_ok=True)

FREEZE_CONTEST = 3435
SEED = 20260915
MC_B = 200_000


def binary_matrix(df: pd.DataFrame) -> np.ndarray:
    nums = df[[f"n{i}" for i in range(1, 16)]].to_numpy(int) - 1
    x = np.zeros((len(df), 25), dtype=np.uint8)
    x[np.arange(len(df))[:, None], nums] = 1
    return x


def bh_adjust(pvals: list[float]) -> list[float]:
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    q = np.empty(m, float)
    running = 1.0
    for rev in range(m - 1, -1, -1):
        idx = order[rev]
        rank = rev + 1
        running = min(running, p[idx] * m / rank)
        q[idx] = min(1.0, running)
    return q.tolist()


def empirical_mean_hits_p(mean_obs: float, n: int, rng: np.random.Generator) -> float:
    # Under a fair 15-of-25 draw, overlap with any predeclared 15-number game is
    # Hypergeometric(N=25, K=15, n=15), irrespective of how the game was chosen
    # from past information. Simulate the distribution of the sample mean.
    # Chunking avoids a large B x n matrix.
    exceed = 0
    done = 0
    batch = 10_000
    while done < MC_B:
        b = min(batch, MC_B - done)
        vals = rng.hypergeometric(ngood=15, nbad=10, nsample=15, size=(b, n)).mean(axis=1)
        exceed += int(np.sum(vals >= mean_obs - 1e-15))
        done += b
    return (1.0 + exceed) / (1.0 + MC_B)


def main() -> None:
    df = pd.read_csv(DATA)
    df["contest"] = df["contest"].astype(int)
    df = df.sort_values("contest").reset_index(drop=True)
    x = binary_matrix(df)

    freeze_idx_arr = np.where(df.contest.to_numpy() == FREEZE_CONTEST)[0]
    if len(freeze_idx_arr) != 1:
        raise RuntimeError(f"Freeze contest {FREEZE_CONTEST} not found exactly once")
    freeze_idx = int(freeze_idx_arr[0]) + 1
    if freeze_idx >= len(df):
        raise RuntimeError("No post-freeze observations are available")

    train = x[:freeze_idx]
    hold = x[freeze_idx:]
    hold_df = df.iloc[freeze_idx:].copy()
    n_hold = len(hold)

    # 1. Fixed cumulative-frequency rule frozen at contest 3435.
    p_train = train.mean(axis=0)
    fixed_game = np.sort(np.argsort(p_train)[-15:])
    fixed_hits = hold[:, fixed_game].sum(axis=1).astype(float)
    fixed_brier = ((hold - p_train[None, :]) ** 2).mean(axis=1)

    # 2. Rolling 1000-contest rule fixed before seeing the post-freeze outcomes.
    rolling_hits = []
    rolling_games = []
    for t in range(freeze_idx, len(x)):
        start = max(0, t - 1000)
        p = x[start:t].mean(axis=0)
        game = np.sort(np.argsort(p)[-15:])
        rolling_games.append(" ".join(f"{i+1:02d}" for i in game))
        rolling_hits.append(float(x[t, game].sum()))
    rolling_hits = np.asarray(rolling_hits)

    # Persistence of the 25-number deviation vector into the genuinely new data.
    p_hold = hold.mean(axis=0)
    pear = stats.pearsonr(p_train - 0.6, p_hold - 0.6)
    spear = stats.spearmanr(p_train, p_hold)

    rng = np.random.default_rng(SEED)
    fixed_mc_p = empirical_mean_hits_p(float(fixed_hits.mean()), n_hold, rng)
    rolling_mc_p = empirical_mean_hits_p(float(rolling_hits.mean()), n_hold, rng)

    # Current AXION 0.3 nested temporal outputs, restricted to the same genuine holdout.
    outer = pd.read_csv(OUTER)
    outer_hold = outer[outer.contest.astype(int) > FREEZE_CONTEST].copy()
    if outer_hold.empty:
        raise RuntimeError("outer_predictions.csv has no post-freeze contests")
    # Guard against accidental missing genuine-holdout contests.
    expected = set(hold_df.contest.astype(int).tolist())
    observed_outer = set(outer_hold.contest.astype(int).tolist())
    missing_outer = sorted(expected - observed_outer)

    axion_hits = outer_hold.hits_single.to_numpy(float)
    axion_brier = outer_hold.brier.to_numpy(float)
    port_diff = (outer_hold.best_portfolio10 - outer_hold.random_portfolio10_mean).to_numpy(float)
    axion_mc_p = empirical_mean_hits_p(float(axion_hits.mean()), len(axion_hits), rng)

    hypotheses = [
        ("fixed_top15_hits", fixed_mc_p),
        ("rolling1000_top15_hits", rolling_mc_p),
        ("bias_vector_pearson", float(pear.pvalue)),
        ("axion_single_hits", axion_mc_p),
        ("axion_portfolio_vs_random", float(stats.ttest_1samp(port_diff, 0.0).pvalue)),
    ]
    qvals = bh_adjust([p for _, p in hypotheses])
    tests = [
        {"test": name, "p": float(p), "q_bh": float(q)}
        for (name, p), q in zip(hypotheses, qvals)
    ]

    rows = hold_df[["contest", "date"]].copy()
    rows["fixed_hits"] = fixed_hits.astype(int)
    rows["rolling1000_hits"] = rolling_hits.astype(int)
    rows["rolling1000_game"] = rolling_games
    rows.to_csv(OUT / "genuine_holdout_frequency_predictions.csv", index=False)
    outer_hold.to_csv(OUT / "genuine_holdout_axion_outer_predictions.csv", index=False)

    number_rows = pd.DataFrame({
        "number": np.arange(1, 26),
        "pre3436_frequency": p_train,
        "post3435_frequency": p_hold,
        "pre3436_deviation": p_train - 0.6,
        "post3435_deviation": p_hold - 0.6,
        "fixed_top15": [int(i in set(fixed_game.tolist())) for i in range(25)],
    })
    number_rows.to_csv(OUT / "genuine_holdout_number_persistence.csv", index=False)

    summary = {
        "module": "AXION genuine post-3435 holdout validation",
        "freeze_contest": FREEZE_CONTEST,
        "freeze_date": str(df.iloc[freeze_idx - 1].date),
        "holdout_first_contest": int(hold_df.iloc[0].contest),
        "holdout_last_contest": int(hold_df.iloc[-1].contest),
        "holdout_last_date": str(hold_df.iloc[-1].date),
        "n_holdout": int(n_hold),
        "fixed_top15": [int(i + 1) for i in fixed_game],
        "fixed_top15_mean_hits": float(fixed_hits.mean()),
        "fixed_top15_t_p_vs9": float(stats.ttest_1samp(fixed_hits, 9.0).pvalue),
        "fixed_top15_mc_p_ge": float(fixed_mc_p),
        "fixed_probability_brier": float(fixed_brier.mean()),
        "fixed_probability_brier_p_vs_0_24": float(stats.ttest_1samp(fixed_brier, 0.24).pvalue),
        "rolling1000_mean_hits": float(rolling_hits.mean()),
        "rolling1000_t_p_vs9": float(stats.ttest_1samp(rolling_hits, 9.0).pvalue),
        "rolling1000_mc_p_ge": float(rolling_mc_p),
        "bias_vector_pearson_r": float(pear.statistic),
        "bias_vector_pearson_p": float(pear.pvalue),
        "bias_vector_spearman_rho": float(spear.statistic),
        "bias_vector_spearman_p": float(spear.pvalue),
        "axion_outer_n": int(len(outer_hold)),
        "axion_outer_missing_holdout_contests": missing_outer,
        "axion_single_mean_hits": float(axion_hits.mean()),
        "axion_single_t_p_vs9": float(stats.ttest_1samp(axion_hits, 9.0).pvalue),
        "axion_single_mc_p_ge": float(axion_mc_p),
        "axion_mean_brier": float(axion_brier.mean()),
        "axion_brier_p_vs_0_24": float(stats.ttest_1samp(axion_brier, 0.24).pvalue),
        "axion_portfolio10_mean": float(outer_hold.best_portfolio10.mean()),
        "random_portfolio10_mean": float(outer_hold.random_portfolio10_mean.mean()),
        "portfolio_paired_difference": float(port_diff.mean()),
        "portfolio_paired_t_p": float(stats.ttest_1samp(port_diff, 0.0).pvalue),
        "multiple_test_control": tests,
        "mc_replicates_per_hits_test": MC_B,
        "seed": SEED,
        "decision_rule": "A pre-freeze signal is considered replicated only if it remains directionally consistent in the post-3435 holdout and survives multiplicity control. No result is converted automatically into a betting rule.",
    }
    (OUT / "genuine_holdout_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    report = [
        "# AXION - Genuine post-3435 holdout validation",
        "",
        f"Freeze: contest {FREEZE_CONTEST}, {summary['freeze_date']}.",
        f"Genuine holdout: contests {summary['holdout_first_contest']} to {summary['holdout_last_contest']} ({summary['n_holdout']} draws).",
        "",
        "## Frequency persistence",
        f"- Fixed pre-freeze top-15: {summary['fixed_top15_mean_hits']:.4f} mean hits, empirical p={summary['fixed_top15_mc_p_ge']:.6g}.",
        f"- Rolling 1000: {summary['rolling1000_mean_hits']:.4f} mean hits, empirical p={summary['rolling1000_mc_p_ge']:.6g}.",
        f"- Bias-vector Pearson correlation pre vs holdout: r={summary['bias_vector_pearson_r']:.4f}, p={summary['bias_vector_pearson_p']:.6g}.",
        f"- Fixed pre-freeze probability Brier: {summary['fixed_probability_brier']:.6f}, compared with 0.24 baseline.",
        "",
        "## AXION 0.3 genuine holdout",
        f"- Single game: {summary['axion_single_mean_hits']:.4f} mean hits, empirical p={summary['axion_single_mc_p_ge']:.6g}.",
        f"- Brier: {summary['axion_mean_brier']:.6f}.",
        f"- Portfolio 10: {summary['axion_portfolio10_mean']:.4f} vs random {summary['random_portfolio10_mean']:.4f}; paired difference {summary['portfolio_paired_difference']:.4f}, p={summary['portfolio_paired_t_p']:.6g}.",
        "",
        "## Multiplicity",
    ]
    for t in tests:
        report.append(f"- {t['test']}: p={t['p']:.6g}, BH q={t['q_bh']:.6g}.")
    report += [
        "",
        "## Governance",
        "These observations are a falsification test of a signal specified before the post-3435 holdout was inspected. Statistical significance alone does not establish a causal mechanism or future advantage. Results remain experimental until replicated on additional future contests and checked against source/data-quality explanations.",
    ]
    (OUT / "genuine_holdout_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
