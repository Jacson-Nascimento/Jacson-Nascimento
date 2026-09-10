#!/usr/bin/env python3
"""Prospective power analysis for the AXION locked-horizon protocol.

This is a design analysis, not a prediction model. It is computed before any
prospective result is evaluated.

The fair single-game overlap distribution is Hypergeometric(25, 15, 15).
For standardized alternatives, the fair distribution is exponentially tilted
until it has a requested mean hit rate. This provides a smooth one-parameter
family for asking how much mean improvement would be detectable at the locked
horizons without claiming that any such alternative is the true data-generating
process.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "nasa_layer" / "prospective_power"
OUT.mkdir(parents=True, exist_ok=True)

HORIZONS = [25, 50, 100, 250]
TARGET_MEANS = [9.1, 9.2, 9.3, 9.4, 9.5, 9.75, 10.0]
ALPHAS = {
    "nominal_0.05": 0.05,
    "conservative_4test_0.0125": 0.0125,
}
TARGET_POWER = 0.80

K = np.arange(16, dtype=float)
P0 = stats.hypergeom.pmf(K, 25, 15, 15)
P0 = P0 / P0.sum()


def tilted_distribution(target_mean: float) -> np.ndarray:
    if np.isclose(target_mean, 9.0):
        return P0.copy()

    def mean_at(theta: float) -> float:
        logw = theta * K
        logw -= np.max(logw)
        w = P0 * np.exp(logw)
        w /= w.sum()
        return float(np.dot(K, w))

    theta = brentq(lambda t: mean_at(t) - target_mean, -20.0, 20.0)
    logw = theta * K
    logw -= np.max(logw)
    w = P0 * np.exp(logw)
    return w / w.sum()


def convolve_n(p: np.ndarray, n: int) -> np.ndarray:
    d = np.array([1.0])
    for _ in range(n):
        d = np.convolve(d, p)
    return d / d.sum()


def critical_total(n: int, alpha: float) -> tuple[int, float]:
    d = convolve_n(P0, n)
    tails = np.flip(np.cumsum(np.flip(d)))
    for c in range(len(d)):
        if tails[c] <= alpha:
            return c, float(tails[c])
    return len(d), 0.0


def power_at(n: int, alpha: float, target_mean: float) -> float:
    c, _ = critical_total(n, alpha)
    d = convolve_n(tilted_distribution(target_mean), n)
    return float(d[c:].sum())


def mean_for_target_power(n: int, alpha: float, target_power: float) -> float:
    def objective(mu: float) -> float:
        return power_at(n, alpha, mu) - target_power

    return float(brentq(objective, 9.000000001, 12.0))


def main() -> None:
    null_mean = float(np.dot(K, P0))
    null_var = float(np.dot((K - null_mean) ** 2, P0))
    if not np.isclose(null_mean, 9.0, atol=1e-12):
        raise RuntimeError("unexpected null mean")
    if not np.isclose(null_var, 1.5, atol=1e-12):
        raise RuntimeError("unexpected null variance")

    rows = []
    critical_rows = []
    for n in HORIZONS:
        for alpha_label, alpha in ALPHAS.items():
            critical, actual_alpha = critical_total(n, alpha)
            critical_rows.append(
                {
                    "horizon": n,
                    "alpha_label": alpha_label,
                    "alpha_target": alpha,
                    "critical_total_hits": critical,
                    "critical_mean_hits": critical / n,
                    "actual_null_tail_probability": actual_alpha,
                }
            )
            for mu in TARGET_MEANS:
                rows.append(
                    {
                        "horizon": n,
                        "alpha_label": alpha_label,
                        "alpha_target": alpha,
                        "alternative_mean_hits": mu,
                        "power": power_at(n, alpha, mu),
                    }
                )

    mde_rows = []
    for n in HORIZONS:
        for alpha_label, alpha in ALPHAS.items():
            mu80 = mean_for_target_power(n, alpha, TARGET_POWER)
            mde_rows.append(
                {
                    "horizon": n,
                    "alpha_label": alpha_label,
                    "alpha_target": alpha,
                    "target_power": TARGET_POWER,
                    "mean_hits_for_80pct_power": mu80,
                    "increment_over_fair_mean": mu80 - 9.0,
                }
            )

    def write_csv(name: str, records: list[dict]) -> None:
        with (OUT / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)

    write_csv("critical_values.csv", critical_rows)
    write_csv("power_grid.csv", rows)
    write_csv("mde_80.csv", mde_rows)

    summary = {
        "analysis": "AXION prospective locked-horizon power analysis",
        "null": "Hypergeometric(25,15,15)",
        "null_mean_hits": null_mean,
        "null_variance_hits": null_var,
        "locked_horizons": HORIZONS,
        "target_means": TARGET_MEANS,
        "alpha_levels": ALPHAS,
        "target_power": TARGET_POWER,
        "alternative_family": "exponential tilt of the fair hypergeometric overlap distribution",
        "interpretation": (
            "Design sensitivity only. The tilted family is not asserted to be the true "
            "data-generating process. The 0.0125 threshold is a conservative four-test "
            "reference, not the exact Benjamini-Hochberg cutoff."
        ),
        "critical_values": critical_rows,
        "mde_80": mde_rows,
    }
    (OUT / "power_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    md = [
        "# AXION prospective power analysis",
        "",
        "Design analysis registered before any prospective contest is evaluated.",
        "",
        "The fair overlap for a predeclared 15-number game is `Hypergeometric(25,15,15)`, "
        "with mean 9 and variance 1.5. Alternatives are generated by exponential tilting "
        "of this exact null distribution to specified mean hit rates. This is a sensitivity "
        "device, not a claim about the true alternative distribution.",
        "",
        "## 80% power: minimum mean hit rate under the standardized alternative",
        "",
        "| Horizon | alpha 0.05 | conservative alpha 0.0125 |",
        "|---:|---:|---:|",
    ]
    mde_lookup = {(r["horizon"], r["alpha_label"]): r for r in mde_rows}
    for n in HORIZONS:
        a = mde_lookup[(n, "nominal_0.05")]["mean_hits_for_80pct_power"]
        b = mde_lookup[(n, "conservative_4test_0.0125")]["mean_hits_for_80pct_power"]
        md.append(f"| {n} | {a:.3f} | {b:.3f} |")

    md += [
        "",
        "## Interpretation",
        "",
        "The 25-contest horizon is an early diagnostic, not a strong confirmation horizon. "
        "Under this standardized alternative it needs a relatively large improvement in "
        "mean hits to reach 80% power. The 100- and 250-contest horizons are materially more "
        "sensitive to modest effects.",
        "",
        "The conservative alpha 0.0125 column approximates the difficult case in which one "
        "of four strategies must carry most of the multiplicity burden. The protocol itself "
        "will continue to apply Benjamini-Hochberg to the four preregistered strategy tests.",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
