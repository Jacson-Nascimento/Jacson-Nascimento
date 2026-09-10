#!/usr/bin/env python3
"""Prospective validation registry for AXION.

Governance
----------
Baseline manifests are immutable once created. The registry is reconstructed from
those manifests and the observed Lotofacil history. New manifests are created only
when every preregistered strategy is available, including a valid AXION prediction
manifest generated from the immediately preceding observed contest.

Primary endpoint
----------------
Single-game hits for a 15-number game.

Locked review horizons
----------------------
25, 50, 100 and 250 evaluated contests.

Inference
---------
At locked horizons, the one-sided test versus the fair 15/25 model is computed
from the exact convolution of Hypergeometric(25, 15, 15) overlap distributions.
Benjamini-Hochberg correction is applied across the four preregistered strategies.
Pairwise differences versus the deterministic random control are reported only
descriptively in this engine version, avoiding an unjustified exact-independence
assumption for adaptive strategies.
"""
from __future__ import annotations

import hashlib
import json
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
PROTOCOL_VERSION = "axion-prospective-v1"
REGISTRY_ENGINE_VERSION = "1.1"
STRATEGIES = [
    "axion_top_game",
    "fixed_pre3436_top15",
    "rolling1000_top15",
    "deterministic_random_control",
]


def validate_history(df: pd.DataFrame) -> None:
    required = {"contest", "date", *[f"n{i}" for i in range(1, 16)]}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise RuntimeError(f"history missing required columns: {missing}")
    if df.empty:
        raise RuntimeError("history is empty")

    contests = df["contest"].astype(int).to_numpy()
    if len(np.unique(contests)) != len(contests):
        raise RuntimeError("history contains duplicate contest identifiers")
    if np.any(np.diff(contests) != 1):
        raise RuntimeError("history must contain a continuous sequence of contest identifiers")

    nums = df[[f"n{i}" for i in range(1, 16)]].to_numpy(int)
    if np.any((nums < 1) | (nums > 25)):
        raise RuntimeError("history contains lottery numbers outside 1..25")
    for idx, row in enumerate(nums):
        if len(set(int(v) for v in row)) != 15:
            raise RuntimeError(f"contest row {idx} does not contain 15 unique numbers")


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
    if end <= start:
        raise RuntimeError("insufficient history for rolling game")
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


def validate_game(game: object, label: str) -> list[int]:
    if not isinstance(game, list) or len(game) != 15:
        raise RuntimeError(f"{label} is not a 15-number list")
    vals = [int(v) for v in game]
    if len(set(vals)) != 15 or min(vals) < 1 or max(vals) > 25:
        raise RuntimeError(f"{label} must contain 15 unique numbers in 1..25")
    return sorted(vals)


def load_axion_game(
    contest: int, last_observed: int
) -> tuple[list[int] | None, str | None, str | None]:
    """Return AXION game, source SHA256 and a pending reason. Fail closed."""
    path = axion_manifest_path(contest)
    if not path.exists():
        return None, None, f"waiting_for_prediction_{contest}_manifest"

    raw = path.read_bytes()
    try:
        obj = json.loads(raw.decode("utf-8"))
        if int(obj.get("next_contest")) != contest:
            return None, None, f"prediction_manifest_next_contest_mismatch:{obj.get('next_contest')}"
        if int(obj.get("last_observed_contest")) != last_observed:
            return None, None, (
                "prediction_manifest_last_observed_mismatch:"
                f"{obj.get('last_observed_contest')}"
            )
        game = validate_game(obj.get("top_game"), "axion_top_game")
    except Exception as exc:
        return None, None, f"invalid_prediction_manifest:{type(exc).__name__}:{exc}"

    return game, hashlib.sha256(raw).hexdigest(), None


def create_baseline_manifest(
    df: pd.DataFrame, x: np.ndarray, contest: int
) -> tuple[dict | None, str | None]:
    if contest < START_PROSPECTIVE_CONTEST:
        return None, "before_prospective_start"

    p = manifest_path(contest)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")), None

    last_observed = int(df.contest.max())
    if contest != last_observed + 1:
        return None, f"contest_not_next_after_observed:{last_observed}"

    axion_game, axion_manifest_sha, pending = load_axion_game(contest, last_observed)
    if pending:
        return None, pending

    fixed = fixed_pre3436_game(df, x)
    rolling = rolling_game(x, len(x))
    control = deterministic_control(contest)

    manifest = {
        "protocol_version": PROTOCOL_VERSION,
        "registry_engine_version": REGISTRY_ENGINE_VERSION,
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
        "governance": (
            "Games are fixed before the target contest result is available. "
            "Past manifests are never rewritten by this script."
        ),
    }
    body = json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    p.write_text(body, encoding="utf-8")
    return manifest, None


def exact_single_game_sum_distribution(n: int) -> np.ndarray:
    """Distribution of total hits across n fair 15/25 draws for a fixed/predictable game."""
    if n <= 0:
        return np.array([1.0], dtype=float)

    single = np.zeros(16, dtype=float)
    single[:] = stats.hypergeom.pmf(np.arange(16), 25, 15, 15)
    dist = np.array([1.0], dtype=float)
    for _ in range(n):
        dist = np.convolve(dist, single)
    dist /= dist.sum()
    return dist


def exact_tail_sum_hits(observed_sum: int, n: int) -> float:
    dist = exact_single_game_sum_distribution(n)
    observed_sum = int(observed_sum)
    if observed_sum <= 0:
        return 1.0
    if observed_sum >= len(dist):
        return 0.0
    return float(dist[observed_sum:].sum())


def bh_adjust(tests: list[dict], p_key: str, q_key: str = "q_bh") -> None:
    if not tests:
        return

    pvals = np.array([float(t[p_key]) for t in tests], dtype=float)
    order = np.argsort(pvals)
    q = np.empty(len(pvals), dtype=float)
    running = 1.0
    for rev in range(len(pvals) - 1, -1, -1):
        idx = order[rev]
        rank = rev + 1
        running = min(running, pvals[idx] * len(pvals) / rank)
        q[idx] = min(1.0, running)
    for t, qv in zip(tests, q):
        t[q_key] = float(qv)


def evaluate(df: pd.DataFrame) -> pd.DataFrame:
    result_map = {
        int(r.contest): set(int(r[f"n{i}"]) for i in range(1, 16))
        for _, r in df.iterrows()
    }
    rows = []

    for p in sorted(OUT.glob("baseline_manifest_*.json")):
        raw = p.read_bytes()
        obj = json.loads(raw.decode("utf-8"))
        contest = int(obj["contest"])
        if contest not in result_map:
            continue

        actual = result_map[contest]
        manifest_sha = hashlib.sha256(raw).hexdigest()
        for strategy in STRATEGIES:
            game = obj["strategies"].get(strategy)
            if not game:
                continue
            vals = validate_game(game, f"{p.name}:{strategy}")
            rows.append(
                {
                    "contest": contest,
                    "strategy": strategy,
                    "hits": len(actual.intersection(vals)),
                    "game": " ".join(f"{v:02d}" for v in vals),
                    "manifest": p.name,
                    "manifest_sha256": manifest_sha,
                }
            )

    return pd.DataFrame(rows)


def summarize(ledger: pd.DataFrame) -> dict:
    out = {
        "protocol_version": PROTOCOL_VERSION,
        "registry_engine_version": REGISTRY_ENGINE_VERSION,
        "start_contest": START_PROSPECTIVE_CONTEST,
        "locked_horizons": HORIZONS,
        "primary_endpoint": "single_game_hits",
        "primary_null": "exact convolution of Hypergeometric(25,15,15)",
        "benchmark_mean_hits": 9.0,
        "strategy_results": {},
        "locked_horizon_reviews": [],
    }

    if ledger.empty:
        out["n_evaluated_contests"] = 0
        out["next_locked_horizon"] = HORIZONS[0]
        return out

    contests = sorted(int(v) for v in ledger.contest.unique().tolist())
    out["n_evaluated_contests"] = len(contests)
    out["first_evaluated_contest"] = contests[0]
    out["last_evaluated_contest"] = contests[-1]

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
            "ge14": int((z.hits >= 14).sum()),
            "eq15": int((z.hits == 15).sum()),
        }

    for h in HORIZONS:
        if len(contests) < h:
            continue

        first_h = set(contests[:h])
        primary_tests = []
        for strategy in STRATEGIES:
            z = ledger[
                (ledger.strategy == strategy) & (ledger.contest.isin(first_h))
            ].sort_values("contest")
            if len(z) != h:
                continue

            observed_sum = int(z.hits.sum())
            primary_tests.append(
                {
                    "strategy": strategy,
                    "n": h,
                    "sum_hits": observed_sum,
                    "mean_hits": float(z.hits.mean()),
                    "p_one_sided_vs_fair_exact": exact_tail_sum_hits(observed_sum, h),
                }
            )
        bh_adjust(primary_tests, "p_one_sided_vs_fair_exact")

        control = ledger[
            (ledger.strategy == "deterministic_random_control")
            & (ledger.contest.isin(first_h))
        ][["contest", "hits"]].rename(columns={"hits": "control_hits"})

        descriptive_vs_control = []
        if len(control) == h:
            for strategy in STRATEGIES:
                if strategy == "deterministic_random_control":
                    continue
                z = ledger[
                    (ledger.strategy == strategy) & (ledger.contest.isin(first_h))
                ][["contest", "hits"]]
                if len(z) != h:
                    continue
                paired = z.merge(control, on="contest", how="inner")
                if len(paired) != h:
                    continue
                diff = paired.hits - paired.control_hits
                descriptive_vs_control.append(
                    {
                        "strategy": strategy,
                        "n": h,
                        "mean_hit_difference_vs_control": float(diff.mean()),
                        "sum_hit_difference_vs_control": int(diff.sum()),
                        "wins": int((diff > 0).sum()),
                        "ties": int((diff == 0).sum()),
                        "losses": int((diff < 0).sum()),
                        "inferential_status": "descriptive_only",
                    }
                )

        out["locked_horizon_reviews"].append(
            {
                "horizon": h,
                "primary_vs_fair": primary_tests,
                "descriptive_vs_random_control": descriptive_vs_control,
            }
        )

    pending = [h for h in HORIZONS if len(contests) < h]
    out["next_locked_horizon"] = pending[0] if pending else None
    return out


def write_manifest_index() -> None:
    rows = []
    for p in sorted(OUT.glob("baseline_manifest_*.json")):
        raw = p.read_bytes()
        obj = json.loads(raw.decode("utf-8"))
        rows.append(
            {
                "contest": int(obj["contest"]),
                "manifest": p.name,
                "manifest_sha256": hashlib.sha256(raw).hexdigest(),
                "created_after_observing_contest": int(
                    obj["created_after_observing_contest"]
                ),
                "axion_prediction_manifest_sha256": obj.get(
                    "axion_prediction_manifest_sha256"
                ),
                "protocol_version": obj.get("protocol_version"),
                "registry_engine_version": obj.get("registry_engine_version", "1.0"),
            }
        )

    columns = [
        "contest",
        "manifest",
        "manifest_sha256",
        "created_after_observing_contest",
        "axion_prediction_manifest_sha256",
        "protocol_version",
        "registry_engine_version",
    ]
    pd.DataFrame(rows, columns=columns).to_csv(OUT / "manifest_index.csv", index=False)


def write_checksums() -> None:
    names = [
        "prospective_ledger.csv",
        "prospective_summary.json",
        "prospective_status.json",
        "manifest_index.csv",
    ]
    names += [p.name for p in sorted(OUT.glob("baseline_manifest_*.json"))]

    lines = []
    for name in names:
        p = OUT / name
        if p.exists():
            lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {name}")
    (OUT / "CHECKSUMS.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_check_exact_null() -> None:
    dist = exact_single_game_sum_distribution(25)
    if not np.isclose(dist.sum(), 1.0, atol=1e-12):
        raise RuntimeError("exact null distribution does not sum to 1")
    grid = np.arange(len(dist), dtype=float)
    if not np.isclose(float(np.dot(grid, dist)), 25 * 9.0, atol=1e-10):
        raise RuntimeError("exact null distribution has incorrect expectation")


def main() -> None:
    df = pd.read_csv(DATA).sort_values("contest").reset_index(drop=True)
    df["contest"] = df["contest"].astype(int)
    validate_history(df)
    self_check_exact_null()
    x = binary_matrix(df)

    # Evaluate immutable manifests before attempting to preregister the next contest.
    ledger = evaluate(df)
    if ledger.empty:
        ledger = pd.DataFrame(
            columns=[
                "contest",
                "strategy",
                "hits",
                "game",
                "manifest",
                "manifest_sha256",
            ]
        )
    ledger.to_csv(OUT / "prospective_ledger.csv", index=False)

    summary = summarize(ledger)
    (OUT / "prospective_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    next_contest = int(df.contest.max()) + 1
    manifest, pending_reason = create_baseline_manifest(df, x, next_contest)

    status = {
        "protocol_version": PROTOCOL_VERSION,
        "registry_engine_version": REGISTRY_ENGINE_VERSION,
        "last_observed_contest": int(df.contest.max()),
        "next_contest": next_contest,
        "baseline_manifest_ready": bool(manifest),
        "pending_reason": pending_reason,
        "evaluated_contests": int(summary.get("n_evaluated_contests", 0)),
        "next_locked_horizon": summary.get("next_locked_horizon"),
    }
    (OUT / "prospective_status.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    write_manifest_index()
    write_checksums()
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
