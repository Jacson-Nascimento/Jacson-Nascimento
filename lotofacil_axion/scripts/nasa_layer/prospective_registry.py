#!/usr/bin/env python3
"""Append-only-by-reconstruction prospective validation ledger for AXION.

Purpose
-------
After the genuine post-3435 holdout failed Gate G5, future evidence must be
collected prospectively. This script preregisters comparison games before the
result exists and later evaluates them from immutable manifests.

Strategies
----------
1. axion_top_game: top game already saved by the AXION prediction manifest.
2. fixed_pre3436_top15: top 15 cumulative frequencies frozen at contest 3435.
3. rolling1000_top15: top 15 frequencies from the immediately prior 1000 draws.
4. deterministic_random_control: uniform 15-number control generated only from
   the contest number and a fixed public salt.

Primary endpoint: mean hits per single 15-number game.
Locked review horizons: 25, 50, 100 and 250 evaluated contests. No inference is
promoted between horizons.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "lotofacil_history.csv"
RESULTS = ROOT / "results"
OUT = RESULTS / "nasa_layer" / "prospective_registry"
OUT.mkdir(parents=True, exist_ok=True)

FREEZE_CONTEST = 3435
START_PROSPECTIVE_CONTEST = 3780
HORIZONS = [25, 50, 100, 250]
CONTROL_SALT = "AXION-PROSPECTIVE-CONTROL-v1"
STRATEGIES = [
    "axion_top_game",
    "fixed_pre3436_top15",
    "rolling1000_top15",
    "deterministic_random_control",
]


def binary_matrix(df: pd.DataFrame) -> np.ndarray:
    nums = df[[f"n{i}" for i in range(1, 16)]].to_numpy(int) - 1
    x = np.zeros((len(df), 25), dtype=np.uint8)
    x[np.arange(len(df))[:, None], nums] = 1
    return x


def fixed_pre3436_game(df: pd.DataFrame, x: np.ndarray) -> list[int]:
    idx = np.where(df.contest.to_numpy(int) == FREEZE_CONTEST)[0]
    if len(idx) != 1:
        raise RuntimeError(f"freeze contest {FREEZE_CONTEST} not found exactly once")
    train = x[: int(idx[0]) + 1]
    game = np.sort(np.argsort(train.mean(axis=0))[-15:]) + 1
    return [int(v) for v in game]


def rolling_game(x: np.ndarray, end: int) -> list[int]:
    start = max(0, end - 1000)
    p = x[start:end].mean(axis=0)
    game = np.sort(np.argsort(p)[-15:]) + 1
    return [int(v) for v in game]


def deterministic_control(contest: int) -> list[int]:
    digest = hashlib.sha256(f"{CONTROL_SALT}:{contest}".encode("utf-8")).digest()
    seed = int.from_bytes(digest[:8], "big", signed=False)
    rng = np.random.default_rng(seed)
    return sorted(int(v) for v in rng.choice(np.arange(1, 26), size=15, replace=False))


def manifest_path(contest: int) -> Path:
    return OUT / f"baseline_manifest_{contest}.json"


def axion_manifest_path(contest: int) -> Path:
    return RESULTS / f"prediction_{contest}_manifest.json"


def create_baseline_manifest(df: pd.DataFrame, x: np.ndarray, contest: int) -> dict | None:
    if contest < START_PROSPECTIVE_CONTEST:
        return None
    p = manifest_path(contest)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))

    # Contest must be exactly next after the latest observed draw at creation time.
    last_observed = int(df.contest.max())
    if contest != last_observed + 1:
        return None

    axion_path = axion_manifest_path(contest)
    axion_game = None
    axion_manifest_sha = None
    if axion_path.exists():
        raw = axion_path.read_bytes()
        obj = json.loads(raw.decode("utf-8"))
        axion_game = [int(v) for v in obj.get("top_game", [])]
        axion_manifest_sha = hashlib.sha256(raw).hexdigest()
        if len(axion_game) != 15:
            axion_game = None

    fixed = fixed_pre3436_game(df, x)
    rolling = rolling_game(x, len(x))
    control = deterministic_control(contest)
    manifest = {
        "protocol_version": "axion-prospective-v1",
        "contest": contest,
        "created_after_observing_contest": last_observed,
        "data_last_date": str(df.iloc[-1].date),
        "primary_endpoint": "single_game_hits",
        "locked_horizons": HORIZONS,
        "strategies": {
            "axion_top_game": axion_game,
            "fixed_pre3436_top15": fixed,
            "rolling1000_top15": rolling,
            "deterministic_random_control": control,
        },
        "axion_prediction_manifest_sha256": axion_manifest_sha,
        "control_salt": CONTROL_SALT,
        "governance": "Games are fixed before the target contest result is available. Past manifests are never rewritten by this script.",
    }
    body = json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    p.write_text(body, encoding="utf-8")
    return manifest


def hypergeom_tail_ge_mean(mean_hits: float, n: int) -> float:
    # Normal approximation to the sum of iid Hypergeometric(25,15,15) overlaps.
    # Exact per-game mean=9, variance=1.5. Used only at locked horizons.
    if n <= 0:
        return float("nan")
    z = (mean_hits - 9.0) / math.sqrt(1.5 / n)
    return float(stats.norm.sf(z))


def evaluate(df: pd.DataFrame) -> pd.DataFrame:
    result_map = {
        int(r.contest): set(int(r[f"n{i}"]) for i in range(1, 16))
        for _, r in df.iterrows()
    }
    rows = []
    for p in sorted(OUT.glob("baseline_manifest_*.json")):
        obj = json.loads(p.read_text(encoding="utf-8"))
        contest = int(obj["contest"])
        if contest not in result_map:
            continue
        actual = result_map[contest]
        for strategy in STRATEGIES:
            game = obj["strategies"].get(strategy)
            if not game or len(game) != 15:
                continue
            rows.append({
                "contest": contest,
                "strategy": strategy,
                "hits": len(actual.intersection(int(v) for v in game)),
                "game": " ".join(f"{int(v):02d}" for v in game),
                "manifest": p.name,
            })
    return pd.DataFrame(rows)


def summarize(ledger: pd.DataFrame) -> dict:
    out = {
        "protocol_version": "axion-prospective-v1",
        "start_contest": START_PROSPECTIVE_CONTEST,
        "locked_horizons": HORIZONS,
        "primary_endpoint": "single_game_hits",
        "strategy_results": {},
        "locked_horizon_reviews": [],
    }
    if ledger.empty:
        out["n_evaluated_contests"] = 0
        out["next_locked_horizon"] = HORIZONS[0]
        return out

    contests = sorted(ledger.contest.unique().tolist())
    out["n_evaluated_contests"] = len(contests)
    out["first_evaluated_contest"] = int(contests[0])
    out["last_evaluated_contest"] = int(contests[-1])

    for strategy in STRATEGIES:
        z = ledger[ledger.strategy == strategy].sort_values("contest")
        if z.empty:
            continue
        out["strategy_results"][strategy] = {
            "n": int(len(z)),
            "mean_hits": float(z.hits.mean()),
            "ge11": int((z.hits >= 11).sum()),
            "ge12": int((z.hits >= 12).sum()),
            "ge13": int((z.hits >= 13).sum()),
        }

    for h in HORIZONS:
        if len(contests) < h:
            continue
        first_h = set(contests[:h])
        tests = []
        for strategy in STRATEGIES:
            z = ledger[(ledger.strategy == strategy) & (ledger.contest.isin(first_h))]
            if len(z) != h:
                continue
            p = hypergeom_tail_ge_mean(float(z.hits.mean()), h)
            tests.append({"strategy": strategy, "mean_hits": float(z.hits.mean()), "p_one_sided_vs_fair": p})
        if tests:
            # BH across the four preregistered strategies at each locked horizon.
            pvals = np.array([t["p_one_sided_vs_fair"] for t in tests])
            order = np.argsort(pvals)
            q = np.empty(len(pvals)); running = 1.0
            for rev in range(len(pvals)-1, -1, -1):
                idx = order[rev]; rank = rev + 1
                running = min(running, pvals[idx] * len(pvals) / rank)
                q[idx] = min(1.0, running)
            for t, qv in zip(tests, q):
                t["q_bh"] = float(qv)
            out["locked_horizon_reviews"].append({"horizon": h, "tests": tests})

    pending = [h for h in HORIZONS if len(contests) < h]
    out["next_locked_horizon"] = pending[0] if pending else None
    return out


def main() -> None:
    df = pd.read_csv(DATA).sort_values("contest").reset_index(drop=True)
    df["contest"] = df["contest"].astype(int)
    x = binary_matrix(df)

    # Evaluate only immutable manifests already present before generating the next one.
    ledger = evaluate(df)
    if ledger.empty:
        ledger = pd.DataFrame(columns=["contest", "strategy", "hits", "game", "manifest"])
    ledger.to_csv(OUT / "prospective_ledger.csv", index=False)
    summary = summarize(ledger)
    (OUT / "prospective_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    next_contest = int(df.contest.max()) + 1
    manifest = create_baseline_manifest(df, x, next_contest)

    status = {
        "last_observed_contest": int(df.contest.max()),
        "next_contest": next_contest,
        "baseline_manifest_ready": bool(manifest),
        "evaluated_contests": int(summary.get("n_evaluated_contests", 0)),
        "next_locked_horizon": summary.get("next_locked_horizon"),
    }
    (OUT / "prospective_status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
