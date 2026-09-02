#!/usr/bin/env python3
"""Mapeamento exato do espaco Lotofacil em quadrantes e validacao temporal.

Autor: Jacson Cruz do Nascimento

O modulo separa representacao descritiva de evidencia preditiva. Todos os
3.268.760 jogos sao enumerados para obter as probabilidades de referencia.
Qualquer sinal temporal e avaliado fora da amostra por walk-forward.
"""
from __future__ import annotations

import argparse
import csv
import itertools as it
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import chi2_contingency, chisquare

N, K = 25, 15
SPACE_SIZE = math.comb(N, K)
MAP_NAMES = ("spatial", "structural")


def enumerate_space() -> dict[str, np.ndarray]:
    masks = np.empty(SPACE_SIZE, dtype=np.uint32)
    grid_x = np.empty(SPACE_SIZE, dtype=np.int8)
    grid_y = np.empty(SPACE_SIZE, dtype=np.int8)
    sums = np.empty(SPACE_SIZE, dtype=np.uint16)
    adjacency = np.empty(SPACE_SIZE, dtype=np.uint8)
    for i, combo in enumerate(it.combinations(range(1, N + 1), K)):
        arr = np.asarray(combo, dtype=np.int16)
        masks[i] = sum(1 << (int(v) - 1) for v in combo)
        grid_x[i] = int(np.sum((arr - 1) % 5 - 2))
        grid_y[i] = int(np.sum((arr - 1) // 5 - 2))
        sums[i] = int(arr.sum())
        adjacency[i] = int(np.count_nonzero(np.diff(arr) == 1))
    return {
        "mask": masks,
        "grid_x": grid_x,
        "grid_y": grid_y,
        "sum": sums,
        "adjacency": adjacency,
    }


def quadrant(a: np.ndarray, b: np.ndarray, a_cut: float, b_cut: float) -> np.ndarray:
    # As massas sobre os eixos permanecem explicitamente no lado <= mediana.
    # As probabilidades exatas de cada quadrante corrigem essa assimetria.
    return (1 + 2 * (a > a_cut) + (b > b_cut)).astype(np.uint8)


def map_space(space: dict[str, np.ndarray]) -> tuple[dict[str, np.ndarray], dict]:
    cuts = {
        "spatial": {"axis_a": float(np.median(space["grid_x"])), "axis_b": float(np.median(space["grid_y"]))},
        "structural": {"axis_a": float(np.median(space["sum"])), "axis_b": float(np.median(space["adjacency"]))},
    }
    maps = {
        "spatial": quadrant(space["grid_x"], space["grid_y"], **{
            "a_cut": cuts["spatial"]["axis_a"], "b_cut": cuts["spatial"]["axis_b"]}),
        "structural": quadrant(space["sum"], space["adjacency"], **{
            "a_cut": cuts["structural"]["axis_a"], "b_cut": cuts["structural"]["axis_b"]}),
    }
    return maps, cuts


def read_history(path: Path, append_contest: int | None, append_numbers: list[int] | None):
    contests, dates, games = [], [], []
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            contests.append(int(row["contest"]))
            dates.append(row.get("date", ""))
            games.append(tuple(sorted(int(row[f"n{i}"]) for i in range(1, K + 1))))
    if append_contest is not None:
        if len(append_numbers or []) != K or len(set(append_numbers or [])) != K:
            raise ValueError("--append-numbers deve conter 15 dezenas distintas")
        if append_contest in contests:
            raise ValueError(f"concurso {append_contest} ja existe no historico")
        contests.append(append_contest)
        dates.append("")
        games.append(tuple(sorted(append_numbers)))
    return np.asarray(contests), dates, games


def features_for_games(games):
    grid_x, grid_y, sums, adjacency = [], [], [], []
    for combo in games:
        arr = np.asarray(combo, dtype=np.int16)
        grid_x.append(int(np.sum((arr - 1) % 5 - 2)))
        grid_y.append(int(np.sum((arr - 1) // 5 - 2)))
        sums.append(int(arr.sum()))
        adjacency.append(int(np.count_nonzero(np.diff(arr) == 1)))
    return {k: np.asarray(v) for k, v in {
        "grid_x": grid_x, "grid_y": grid_y, "sum": sums, "adjacency": adjacency}.items()}


def bh_adjust(pvalues: list[float]) -> list[float]:
    p = np.asarray(pvalues, dtype=float)
    order = np.argsort(p)
    ranked = p[order]
    adjusted = np.minimum.accumulate((ranked * len(p) / np.arange(1, len(p) + 1))[::-1])[::-1]
    out = np.empty_like(adjusted)
    out[order] = np.clip(adjusted, 0, 1)
    return out.tolist()


def lag_tests(q: np.ndarray, max_lag: int = 20):
    rows = []
    for lag in range(1, max_lag + 1):
        tab = np.zeros((4, 4), dtype=int)
        for a, b in zip(q[:-lag], q[lag:]):
            tab[a - 1, b - 1] += 1
        chi2, p, _, _ = chi2_contingency(tab, correction=False)
        n = tab.sum()
        v = math.sqrt(chi2 / (n * 3))
        rows.append({"lag": lag, "chi2": chi2, "p_value": p, "cramers_v": v})
    return rows


def moving_block_ci(values: np.ndarray, seed: int, reps: int = 1000, block: int = 25):
    rng = np.random.default_rng(seed)
    n = len(values)
    means = np.empty(reps)
    starts = np.arange(max(1, n - block + 1))
    blocks_needed = math.ceil(n / block)
    for r in range(reps):
        draw = np.concatenate([values[s:s + block] for s in rng.choice(starts, blocks_needed)])[:n]
        means[r] = draw.mean()
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def walk_forward(q: np.ndarray, baseline: np.ndarray, prior_strength: float = 50.0, burn: int = 500):
    transitions = np.zeros((4, 4), dtype=float)
    for a, b in zip(q[:burn - 1], q[1:burn]):
        transitions[a - 1, b - 1] += 1
    model_loss, base_loss, model_brier, base_brier = [], [], [], []
    model_hit, base_hit = [], []
    eps = 1e-15
    for t in range(burn, len(q)):
        prev, actual = q[t - 1] - 1, q[t] - 1
        prob = (transitions[prev] + prior_strength * baseline) / (transitions[prev].sum() + prior_strength)
        onehot = np.eye(4)[actual]
        model_loss.append(-math.log(max(eps, prob[actual])))
        base_loss.append(-math.log(max(eps, baseline[actual])))
        model_brier.append(float(np.sum((prob - onehot) ** 2)))
        base_brier.append(float(np.sum((baseline - onehot) ** 2)))
        model_hit.append(int(np.argmax(prob) == actual))
        base_hit.append(int(np.argmax(baseline) == actual))
        transitions[prev, actual] += 1
    dl = np.asarray(model_loss) - np.asarray(base_loss)
    db = np.asarray(model_brier) - np.asarray(base_brier)
    log_ci = moving_block_ci(dl, 3778)
    brier_ci = moving_block_ci(db, 4778)
    validated = bool(log_ci[1] < 0 and brier_ci[1] < 0)
    return {
        "n_predictions": len(model_loss),
        "prior_strength": prior_strength,
        "model_log_loss": float(np.mean(model_loss)),
        "baseline_log_loss": float(np.mean(base_loss)),
        "log_loss_difference": float(dl.mean()),
        "log_loss_difference_block_bootstrap_95ci": log_ci,
        "model_brier": float(np.mean(model_brier)),
        "baseline_brier": float(np.mean(base_brier)),
        "brier_difference": float(db.mean()),
        "brier_difference_block_bootstrap_95ci": brier_ci,
        "model_accuracy": float(np.mean(model_hit)),
        "baseline_accuracy": float(np.mean(base_hit)),
        "validated_predictive_signal": validated,
        "final_transition_counts": transitions.astype(int).tolist(),
    }


def walk_forward_marginal(q: np.ndarray, baseline: np.ndarray, prior_strength: float = 50.0, burn: int = 500):
    counts = np.bincount(q[:burn], minlength=5)[1:].astype(float)
    model_loss, base_loss, model_brier, base_brier = [], [], [], []
    model_hit, base_hit = [], []
    eps = 1e-15
    for t in range(burn, len(q)):
        actual = q[t] - 1
        prob = (counts + prior_strength * baseline) / (counts.sum() + prior_strength)
        onehot = np.eye(4)[actual]
        model_loss.append(-math.log(max(eps, prob[actual])))
        base_loss.append(-math.log(max(eps, baseline[actual])))
        model_brier.append(float(np.sum((prob - onehot) ** 2)))
        base_brier.append(float(np.sum((baseline - onehot) ** 2)))
        model_hit.append(int(np.argmax(prob) == actual))
        base_hit.append(int(np.argmax(baseline) == actual))
        counts[actual] += 1
    dl = np.asarray(model_loss) - np.asarray(base_loss)
    db = np.asarray(model_brier) - np.asarray(base_brier)
    log_ci = moving_block_ci(dl, 5778)
    brier_ci = moving_block_ci(db, 6778)
    validated = bool(log_ci[1] < 0 and brier_ci[1] < 0)
    final_prob = (counts + prior_strength * baseline) / (counts.sum() + prior_strength)
    return {
        "n_predictions": len(model_loss), "prior_strength": prior_strength,
        "model_log_loss": float(np.mean(model_loss)), "baseline_log_loss": float(np.mean(base_loss)),
        "log_loss_difference": float(dl.mean()),
        "log_loss_difference_block_bootstrap_95ci": log_ci,
        "model_brier": float(np.mean(model_brier)), "baseline_brier": float(np.mean(base_brier)),
        "brier_difference": float(db.mean()),
        "brier_difference_block_bootstrap_95ci": brier_ci,
        "model_accuracy": float(np.mean(model_hit)), "baseline_accuracy": float(np.mean(base_hit)),
        "validated_predictive_signal": validated,
        "final_counts": counts.astype(int).tolist(),
        "next_probabilities": {str(i + 1): float(final_prob[i]) for i in range(4)},
        "lift_ratio": {str(i + 1): float(final_prob[i] / baseline[i]) for i in range(4)},
        "top_quadrant": int(np.argmax(final_prob) + 1),
    }


def period_diagnostics(q: np.ndarray, baseline: np.ndarray):
    periods = []
    n = len(q)
    specs = [("first_third", 0, n // 3), ("middle_third", n // 3, 2 * n // 3),
             ("last_third", 2 * n // 3, n), ("last_1000", max(0, n - 1000), n),
             ("last_500", max(0, n - 500), n), ("last_250", max(0, n - 250), n)]
    for label, start, end in specs:
        obs = np.bincount(q[start:end], minlength=5)[1:]
        chi2, p = chisquare(obs, (end - start) * baseline)
        periods.append({"period": label, "start_index": start, "end_index": end,
                        "n": end - start, "counts": obs.tolist(), "chi2": float(chi2),
                        "p_value_descriptive": float(p)})
    return periods


def forecast(q: np.ndarray, baseline: np.ndarray, transitions: list, prior_strength: float):
    tr = np.asarray(transitions, dtype=float)
    prev = int(q[-1] - 1)
    prob = (tr[prev] + prior_strength * baseline) / (tr[prev].sum() + prior_strength)
    return {
        "last_quadrant": prev + 1,
        "next_probabilities": {str(i + 1): float(prob[i]) for i in range(4)},
        "baseline_probabilities": {str(i + 1): float(baseline[i]) for i in range(4)},
        "lift_ratio": {str(i + 1): float(prob[i] / baseline[i]) for i in range(4)},
        "top_quadrant": int(np.argmax(prob) + 1),
    }


def analyze(history_path: Path, output_dir: Path, append_contest=None, append_numbers=None, write_map=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    space = enumerate_space()
    maps, cuts = map_space(space)
    contests, dates, games = read_history(history_path, append_contest, append_numbers)
    hf = features_for_games(games)
    hmaps = {
        "spatial": quadrant(hf["grid_x"], hf["grid_y"], cuts["spatial"]["axis_a"], cuts["spatial"]["axis_b"]),
        "structural": quadrant(hf["sum"], hf["adjacency"], cuts["structural"]["axis_a"], cuts["structural"]["axis_b"]),
    }
    summary = {"author": "Jacson Cruz do Nascimento", "space_size": SPACE_SIZE,
               "history_first_contest": int(contests[0]), "history_last_contest": int(contests[-1]),
               "history_size": len(contests), "maps": {}}
    all_lags = []
    for mi, name in enumerate(MAP_NAMES):
        baseline_counts = np.bincount(maps[name], minlength=5)[1:]
        baseline = baseline_counts / SPACE_SIZE
        obs = np.bincount(hmaps[name], minlength=5)[1:]
        chi2, p = chisquare(obs, len(hmaps[name]) * baseline)
        lags = lag_tests(hmaps[name])
        for row in lags:
            row["map"] = name
            all_lags.append(row)
        wf = walk_forward(hmaps[name], baseline)
        wfm = walk_forward_marginal(hmaps[name], baseline)
        fc = forecast(hmaps[name], baseline, wf["final_transition_counts"], wf["prior_strength"])
        summary["maps"][name] = {
            "cuts": cuts[name], "space_counts": baseline_counts.tolist(),
            "space_probabilities": baseline.tolist(), "history_counts": obs.tolist(),
            "goodness_of_fit_chi2": float(chi2), "goodness_of_fit_p_value": float(p),
            "period_diagnostics": period_diagnostics(hmaps[name], baseline),
            "walk_forward_transition": wf, "walk_forward_marginal": wfm,
            "forecast_transition": fc,
        }
    adj = bh_adjust([r["p_value"] for r in all_lags])
    for row, qv in zip(all_lags, adj):
        row["p_value_bh_40_tests"] = qv
    with (output_dir / "lag_tests.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_lags[0]))
        w.writeheader(); w.writerows(all_lags)
    with (output_dir / "history_quadrants.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["contest", "date", "spatial_quadrant", "structural_quadrant", "grid_x", "grid_y", "sum", "adjacency"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for i in range(len(contests)):
            w.writerow({"contest": contests[i], "date": dates[i],
                        "spatial_quadrant": hmaps["spatial"][i],
                        "structural_quadrant": hmaps["structural"][i],
                        "grid_x": hf["grid_x"][i], "grid_y": hf["grid_y"][i],
                        "sum": hf["sum"][i], "adjacency": hf["adjacency"][i]})
    summary["lag_tests_significant_after_bh_5pct"] = [r for r in all_lags if r["p_value_bh_40_tests"] < 0.05]
    (output_dir / "quadrant_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    if write_map:
        np.savez_compressed(output_dir / "full_combination_map.npz", **space,
                            spatial_quadrant=maps["spatial"], structural_quadrant=maps["structural"])
    return summary


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--history", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--append-contest", type=int)
    p.add_argument("--append-numbers", nargs="*", type=int)
    p.add_argument("--write-map", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    a = parse_args()
    s = analyze(a.history, a.output_dir, a.append_contest, a.append_numbers, a.write_map)
    print(json.dumps(s, indent=2))
