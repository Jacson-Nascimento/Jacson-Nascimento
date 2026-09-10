#!/usr/bin/env python3
"""
AXION NASA Signal Analysis Layer
Etapas 0 e 1:
- congela e mede o baseline histórico;
- valida integridade da base;
- constrói matriz binária concurso x 25;
- constrói feature matrix multidimensional.

Sem capacidade preditiva presumida. As métricas são descritivas e servem
como entrada para comparação posterior com o modelo nulo.
"""

from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23}
BORDER = {
    n for n in range(1, 26)
    if ((n - 1) // 5 + 1) in (1, 5) or ((n - 1) % 5 + 1) in (1, 5)
}
CENTER = set(range(1, 26)) - BORDER


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


def data_quality(contests, draws):
    return {
        "n_concursos": int(len(contests)),
        "concurso_min": int(contests.min()),
        "concurso_max": int(contests.max()),
        "concursos_unicos": int(len(np.unique(contests))),
        "lacunas_na_sequencia_concursos": int(np.sum(np.diff(contests) != 1)),
        "linhas_com_dezenas_duplicadas": int(sum(len(set(map(int, r))) != 15 for r in draws)),
        "linhas_com_dezenas_fora_1_25": int(sum(np.any((r < 1) | (r > 25)) for r in draws)),
        "linhas_nao_ordenadas": int(sum(not np.all(np.diff(r) > 0) for r in draws)),
    }


def max_run(nums):
    diffs = np.diff(nums)
    best = cur = 1
    for d in diffs:
        if d == 1:
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
    return int(best)


def build_matrices(contests, dates, draws):
    n = len(draws)
    binary = np.zeros((n, 25), dtype=np.int8)
    features = []
    prev = None

    for i, nums0 in enumerate(draws):
        nums = np.asarray(nums0, dtype=np.int16)
        binary[i, nums - 1] = 1
        diffs = np.diff(nums)

        gap_counts = Counter(map(int, diffs))
        probs = np.asarray(list(gap_counts.values()), dtype=float) / len(diffs)
        gap_entropy = float(-(probs * np.log2(probs)).sum())

        pairwise = np.abs(nums[:, None] - nums[None, :])
        mean_pairwise = float(pairwise[np.triu_indices(15, 1)].mean())

        repeat_prev = "" if prev is None else int(len(set(map(int, nums)) & set(map(int, prev))))
        if prev is None:
            jaccard = ""
        else:
            union = len(set(map(int, nums)) | set(map(int, prev)))
            jaccard = repeat_prev / union

        row_counts = [
            int(np.sum((nums >= 1 + 5 * (r - 1)) & (nums <= 5 * r)))
            for r in range(1, 6)
        ]
        col_counts = [
            int(np.sum(((nums - 1) % 5) == (c - 1)))
            for c in range(1, 6)
        ]

        rec = {
            "contest": int(contests[i]),
            "date": dates[i],
            "sum": int(nums.sum()),
            "mean": float(nums.mean()),
            "sd": float(nums.std(ddof=1)),
            "min": int(nums.min()),
            "max": int(nums.max()),
            "range": int(nums.max() - nums.min()),
            "even": int(np.sum(nums % 2 == 0)),
            "odd": int(np.sum(nums % 2 == 1)),
            "prime": int(sum(int(x) in PRIMES for x in nums)),
            "low_1_13": int(np.sum(nums <= 13)),
            "high_14_25": int(np.sum(nums >= 14)),
            "border": int(sum(int(x) in BORDER for x in nums)),
            "center": int(sum(int(x) in CENTER for x in nums)),
            "consecutive_pairs": int(np.sum(diffs == 1)),
            "max_run": max_run(nums),
            "gap_mean": float(diffs.mean()),
            "gap_sd": float(diffs.std(ddof=1)),
            "gap_max": int(diffs.max()),
            "gap_entropy": gap_entropy,
            "mean_pairwise_distance": mean_pairwise,
            "repeat_prev": repeat_prev,
            "jaccard_prev": jaccard,
        }
        for r, x in enumerate(row_counts, 1):
            rec[f"row_{r}"] = x
        for c, x in enumerate(col_counts, 1):
            rec[f"col_{c}"] = x
        features.append(rec)
        prev = nums.copy()

    return binary, features


def write_dict_rows(path: Path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(PROJECT_ROOT / "data" / "lotofacil_history.csv"))
    ap.add_argument("--output-dir", default=str(PROJECT_ROOT / "results" / "nasa_layer" / "baseline"))
    args = ap.parse_args()

    input_path = Path(args.input)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    contests, dates, draws = load_history(input_path)
    dq = data_quality(contests, draws)
    if any(dq[k] for k in (
        "lacunas_na_sequencia_concursos",
        "linhas_com_dezenas_duplicadas",
        "linhas_com_dezenas_fora_1_25",
        "linhas_nao_ordenadas",
    )):
        raise ValueError(f"Falha de integridade: {dq}")

    binary, features = build_matrices(contests, dates, draws)
    n = len(draws)

    binary_rows = []
    for i in range(n):
        rec = {"contest": int(contests[i]), "date": dates[i]}
        rec.update({f"d{d:02d}": int(binary[i, d - 1]) for d in range(1, 26)})
        binary_rows.append(rec)
    write_dict_rows(out / "binary_matrix.csv", binary_rows)

    write_dict_rows(out / "feature_matrix.csv", features)

    freq = binary.sum(axis=0)
    expected = n * 15 / 25
    denom = math.sqrt(n * 0.6 * 0.4)
    p_values = [
        binomtest(int(freq[i]), n, 0.6, alternative="two-sided").pvalue
        for i in range(25)
    ]
    q_values = bh_adjust(p_values)
    freq_rows = []
    for i in range(25):
        freq_rows.append({
            "number": i + 1,
            "frequency": int(freq[i]),
            "relative_frequency": float(freq[i] / n),
            "expected_frequency": float(expected),
            "deviation": float(freq[i] - expected),
            "z_approx": float((freq[i] - expected) / denom),
            "p_binomial_two_sided": float(p_values[i]),
            "q_bh_25_numbers": float(q_values[i]),
        })
    write_dict_rows(out / "frequency_by_number.csv", freq_rows)

    sums = np.asarray([r["sum"] for r in features], dtype=float)
    evens = np.asarray([r["even"] for r in features], dtype=float)
    primes = np.asarray([r["prime"] for r in features], dtype=float)
    borders = np.asarray([r["border"] for r in features], dtype=float)
    consecutives = np.asarray([r["consecutive_pairs"] for r in features], dtype=float)
    repeats = np.asarray(
        [np.nan if r["repeat_prev"] == "" else r["repeat_prev"] for r in features],
        dtype=float,
    )

    baseline = [
        {"metric": "n_contests", "value": float(n), "reference": ""},
        {"metric": "freq_sd", "value": float(freq.std(ddof=1)), "reference": "uniform 15/25; validate via null simulation"},
        {"metric": "freq_range", "value": float(freq.max() - freq.min()), "reference": "uniform 15/25; validate via null simulation"},
        {"metric": "freq_chi2", "value": float(np.sum((freq - expected) ** 2 / expected)), "reference": "uniform 15/25; validate via null simulation"},
        {"metric": "sum_mean", "value": float(sums.mean()), "reference": "theoretical mean 195"},
        {"metric": "sum_sd", "value": float(sums.std(ddof=1)), "reference": "theoretical sd approx 18.0278"},
        {"metric": "even_mean", "value": float(evens.mean()), "reference": "theoretical mean 7.2"},
        {"metric": "prime_mean", "value": float(primes.mean()), "reference": "theoretical mean 5.4"},
        {"metric": "border_mean", "value": float(borders.mean()), "reference": "theoretical mean 9.6"},
        {"metric": "consecutive_pairs_mean", "value": float(consecutives.mean()), "reference": "validate via null simulation"},
        {"metric": "repeat_prev_mean", "value": float(np.nanmean(repeats)), "reference": "theoretical mean 9"},
    ]
    write_dict_rows(out / "baseline_metrics.csv", baseline)

    metadata = {
        "stage": "AXION NASA Signal Analysis Layer - Etapas 0 e 1",
        "input": str(input_path),
        "input_sha256": sha256_file(input_path),
        "n_contests": n,
        "first_contest": int(contests[0]),
        "last_contest": int(contests[-1]),
        "first_date": dates[0],
        "last_date": dates[-1],
        "data_quality": dq,
        "notes": [
            "Baseline descritivo; não implica previsibilidade.",
            "Testes individuais de frequência são triagem e exigem validação temporal e modelo nulo.",
        ],
    }
    with (out / "baseline_metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "ok",
        "n_contests": n,
        "output_dir": str(out),
        "freq_sd": float(freq.std(ddof=1)),
        "sum_mean": float(sums.mean()),
        "repeat_prev_mean": float(np.nanmean(repeats)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
