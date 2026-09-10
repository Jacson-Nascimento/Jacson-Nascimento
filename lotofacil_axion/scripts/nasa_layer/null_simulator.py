#!/usr/bin/env python3
"""
AXION NASA Signal Analysis Layer
Etapa 2: modelo nulo uniforme 15/25 + Monte Carlo.

Gera histórias sintéticas com o mesmo número de concursos da base observada,
calcula métricas agregadas e compara o histórico real à distribuição empírica.
"""

from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23}
BORDER = {
    n for n in range(1, 26)
    if ((n - 1) // 5 + 1) in (1, 5) or ((n - 1) % 5 + 1) in (1, 5)
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_history(path: Path):
    contests, dates, draws = [], [], []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = ["contest", "date"] + [f"n{i}" for i in range(1, 16)]
        missing = [c for c in required if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Colunas ausentes: {missing}")
        for row in reader:
            contests.append(int(row["contest"]))
            dates.append(row["date"])
            draws.append([int(row[f"n{i}"]) for i in range(1, 16)])
    return np.asarray(contests, dtype=np.int64), dates, np.asarray(draws, dtype=np.int16)


def bh_adjust(p_values):
    p = np.asarray(p_values, dtype=float)
    order = np.argsort(p)
    m = len(p)
    q = np.empty(m, dtype=float)
    running = 1.0
    for rev in range(m - 1, -1, -1):
        idx = order[rev]
        rank = rev + 1
        running = min(running, p[idx] * m / rank)
        q[idx] = min(1.0, running)
    return q


def actual_metrics(draws):
    n = len(draws)
    binary = np.zeros((n, 25), dtype=np.bool_)
    for i, nums in enumerate(draws):
        binary[i, nums - 1] = True

    vals = np.arange(1, 26, dtype=np.int16)
    expected = n * 0.6
    freq = binary.sum(axis=0)
    sums = (binary * vals).sum(axis=1)
    even_mask = vals % 2 == 0
    prime_mask = np.asarray([int(v) in PRIMES for v in vals], dtype=np.bool_)
    border_mask = np.asarray([int(v) in BORDER for v in vals], dtype=np.bool_)

    consecutive = (binary[:, :-1] & binary[:, 1:]).sum(axis=1)
    repeats = (binary[1:, :] & binary[:-1, :]).sum(axis=1)

    return {
        "freq_sd": float(freq.std(ddof=1)),
        "freq_range": float(freq.max() - freq.min()),
        "freq_chi2": float(np.sum((freq - expected) ** 2 / expected)),
        "sum_mean": float(sums.mean()),
        "sum_sd": float(sums.std(ddof=1)),
        "even_mean": float((binary & even_mask).sum(axis=1).mean()),
        "prime_mean": float((binary & prime_mask).sum(axis=1).mean()),
        "border_mean": float((binary & border_mask).sum(axis=1).mean()),
        "consecutive_pairs_mean": float(consecutive.mean()),
        "repeat_prev_mean": float(repeats.mean()),
    }


def write_rows(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(PROJECT_ROOT / "data" / "lotofacil_history.csv"))
    ap.add_argument("--output-dir", default=str(PROJECT_ROOT / "results" / "nasa_layer" / "null_distributions"))
    ap.add_argument("--simulations", type=int, default=10000)
    ap.add_argument("--batch-size", type=int, default=50)
    ap.add_argument("--seed", type=int, default=20260910)
    args = ap.parse_args()

    input_path = Path(args.input)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    contests, dates, draws = load_history(input_path)
    n = len(draws)
    B = args.simulations
    batch_size = args.batch_size
    rng = np.random.default_rng(args.seed)

    actual = actual_metrics(draws)
    metric_names = list(actual.keys())
    null = {k: np.empty(B, dtype=np.float64) for k in metric_names}

    vals = np.arange(1, 26, dtype=np.int16)
    even_mask = vals % 2 == 0
    prime_mask = np.asarray([int(v) in PRIMES for v in vals], dtype=np.bool_)
    border_mask = np.asarray([int(v) in BORDER for v in vals], dtype=np.bool_)
    expected = n * 0.6

    out_i = 0
    for start in range(0, B, batch_size):
        b = min(batch_size, B - start)

        scores = rng.random((b, n, 25), dtype=np.float32)
        idx = np.argpartition(scores, 15, axis=2)[:, :, :15]
        sel = np.zeros((b, n, 25), dtype=np.bool_)
        np.put_along_axis(sel, idx, True, axis=2)

        counts = sel.sum(axis=1)
        null["freq_sd"][out_i:out_i+b] = counts.std(axis=1, ddof=1)
        null["freq_range"][out_i:out_i+b] = counts.max(axis=1) - counts.min(axis=1)
        null["freq_chi2"][out_i:out_i+b] = ((counts - expected) ** 2 / expected).sum(axis=1)

        sums = (sel * vals).sum(axis=2)
        null["sum_mean"][out_i:out_i+b] = sums.mean(axis=1)
        null["sum_sd"][out_i:out_i+b] = sums.std(axis=1, ddof=1)

        null["even_mean"][out_i:out_i+b] = (sel & even_mask).sum(axis=2).mean(axis=1)
        null["prime_mean"][out_i:out_i+b] = (sel & prime_mask).sum(axis=2).mean(axis=1)
        null["border_mean"][out_i:out_i+b] = (sel & border_mask).sum(axis=2).mean(axis=1)

        consecutive = (sel[:, :, :-1] & sel[:, :, 1:]).sum(axis=2)
        null["consecutive_pairs_mean"][out_i:out_i+b] = consecutive.mean(axis=1)

        repeats = (sel[:, 1:, :] & sel[:, :-1, :]).sum(axis=2)
        null["repeat_prev_mean"][out_i:out_i+b] = repeats.mean(axis=1)

        out_i += b

    dist_rows = []
    for i in range(B):
        rec = {"simulation_id": i + 1}
        rec.update({k: float(null[k][i]) for k in metric_names})
        dist_rows.append(rec)
    write_rows(
        out / f"null_distribution_B{B}.csv",
        dist_rows,
        ["simulation_id"] + metric_names,
    )

    raw_p = []
    summary_rows = []
    for k in metric_names:
        arr = null[k]
        center = float(arr.mean())
        observed = actual[k]
        p = (np.sum(np.abs(arr - center) >= abs(observed - center)) + 1) / (B + 1)
        raw_p.append(float(p))
        summary_rows.append({
            "metric": k,
            "actual": observed,
            "null_mean": float(arr.mean()),
            "null_sd": float(arr.std(ddof=1)),
            "q025": float(np.quantile(arr, 0.025)),
            "q50": float(np.quantile(arr, 0.50)),
            "q975": float(np.quantile(arr, 0.975)),
            "z": float((observed - arr.mean()) / arr.std(ddof=1)),
            "p_empirical_two_sided": float(p),
        })

    q = bh_adjust(raw_p)
    for rec, qq in zip(summary_rows, q):
        rec["q_bh_metrics"] = float(qq)
        rec["triage_flag_q_lt_0_05"] = bool(qq < 0.05)

    write_rows(
        out / f"null_summary_B{B}.csv",
        summary_rows,
        [
            "metric", "actual", "null_mean", "null_sd", "q025", "q50", "q975",
            "z", "p_empirical_two_sided", "q_bh_metrics", "triage_flag_q_lt_0_05",
        ],
    )

    metadata = {
        "stage": "AXION NASA Signal Analysis Layer - Etapa 2",
        "input": str(input_path),
        "input_sha256": sha256_file(input_path),
        "n_contests": n,
        "first_contest": int(contests[0]),
        "last_contest": int(contests[-1]),
        "first_date": dates[0],
        "last_date": dates[-1],
        "simulations": B,
        "batch_size": batch_size,
        "seed": args.seed,
        "generator": "uniform random 15-subset of 25 via random scores + argpartition",
        "interpretation_rule": (
            "Flags são apenas triagem. Integração ao AXION exige estabilidade temporal, "
            "correção por múltiplos testes e validação fora da amostra."
        ),
    }
    with (out / f"null_run_metadata_B{B}.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "ok",
        "simulations": B,
        "seed": args.seed,
        "flagged_metrics": [r["metric"] for r in summary_rows if r["triage_flag_q_lt_0_05"]],
        "output_dir": str(out),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
