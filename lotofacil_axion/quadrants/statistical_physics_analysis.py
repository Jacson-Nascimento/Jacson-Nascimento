#!/usr/bin/env python3
"""Validacao de campos fisico-espaciais no universo exato da Lotofacil.

Autor: Jacson Cruz do Nascimento

Cada jogo e tratado como um estado binario com 15 particulas em uma rede 5x5.
O universo de referencia contem todas as C(25, 15) configuracoes. O historico
e confrontado com esse universo por modelos de maxima entropia (campos de
Gibbs) e por validacao temporal walk-forward. O modulo nao presume que uma
boa aderencia dentro da amostra implique capacidade preditiva.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
from scipy.stats import norm

N = 25
K = 15
SPACE_SIZE = math.comb(N, K)
FEATURE_NAMES = (
    "dipole_power",
    "radial_moment",
    "quadrupole_power",
    "line_imbalance",
    "boundary_energy",
    "perimeter_occupancy",
    "diagonal_contacts",
)
MODEL_GROUPS = {
    "geometry": (0, 1, 2, 3, 5),
    "interface": (4, 6),
    "full_physical": tuple(range(len(FEATURE_NAMES))),
}


def read_history(path: Path) -> tuple[np.ndarray, np.ndarray, list[str]]:
    contests: list[int] = []
    dates: list[str] = []
    masks: list[int] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            numbers = sorted(int(row[f"n{i}"]) for i in range(1, K + 1))
            if len(numbers) != K or len(set(numbers)) != K or numbers[0] < 1 or numbers[-1] > N:
                raise ValueError(f"concurso invalido: {row.get('contest')}")
            contests.append(int(row["contest"]))
            dates.append(row.get("date", ""))
            masks.append(sum(1 << (v - 1) for v in numbers))
    if contests != sorted(contests) or len(contests) != len(set(contests)):
        raise ValueError("concursos devem ser unicos e estar em ordem crescente")
    return np.asarray(contests, dtype=np.int32), np.asarray(masks, dtype=np.uint32), dates


def _orthogonal_edges() -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for row in range(5):
        for col in range(5):
            i = 5 * row + col
            if col < 4:
                edges.append((i, i + 1))
            if row < 4:
                edges.append((i, i + 5))
    return edges


def _diagonal_edges() -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for row in range(4):
        for col in range(4):
            i = 5 * row + col
            edges.extend(((i, i + 6), (i + 1, i + 5)))
    return edges


ORTHOGONAL_EDGES = _orthogonal_edges()
DIAGONAL_EDGES = _diagonal_edges()


def physical_features(masks: np.ndarray) -> np.ndarray:
    """Calcula sete invariantes da ocupacao da rede 5x5 para cada mascara."""
    masks = np.asarray(masks, dtype=np.uint32)
    size = len(masks)
    dx = np.zeros(size, dtype=np.int16)
    dy = np.zeros(size, dtype=np.int16)
    radial = np.zeros(size, dtype=np.int16)
    q_axis = np.zeros(size, dtype=np.int16)
    q_shear = np.zeros(size, dtype=np.int16)
    perimeter = np.zeros(size, dtype=np.int16)
    row_counts = np.zeros((size, 5), dtype=np.int8)
    col_counts = np.zeros((size, 5), dtype=np.int8)

    for i in range(N):
        row, col = divmod(i, 5)
        x, y = col - 2, row - 2
        occupied = ((masks >> i) & 1).astype(np.int16)
        dx += x * occupied
        dy += y * occupied
        radial += (x * x + y * y) * occupied
        q_axis += (x * x - y * y) * occupied
        q_shear += (x * y) * occupied
        if row in (0, 4) or col in (0, 4):
            perimeter += occupied
        row_counts[:, row] += occupied.astype(np.int8)
        col_counts[:, col] += occupied.astype(np.int8)

    boundary = np.zeros(size, dtype=np.int16)
    for i, j in ORTHOGONAL_EDGES:
        boundary += (((masks >> i) ^ (masks >> j)) & 1).astype(np.int16)

    diagonal = np.zeros(size, dtype=np.int16)
    for i, j in DIAGONAL_EDGES:
        diagonal += (((masks >> i) & 1) & ((masks >> j) & 1)).astype(np.int16)

    dipole_power = dx.astype(np.int32) ** 2 + dy.astype(np.int32) ** 2
    quadrupole_power = q_axis.astype(np.int32) ** 2 + 4 * q_shear.astype(np.int32) ** 2
    line_imbalance = (
        np.sum((row_counts.astype(np.int16) - 3) ** 2, axis=1)
        + np.sum((col_counts.astype(np.int16) - 3) ** 2, axis=1)
    )
    return np.column_stack(
        (dipole_power, radial, quadrupole_power, line_imbalance,
         boundary, perimeter, diagonal)
    ).astype(np.int32)


def compress_feature_space(features: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    unique, counts = np.unique(features, axis=0, return_counts=True)
    if int(counts.sum()) != SPACE_SIZE:
        raise ValueError("o mapa fornecido nao contem o universo combinatorio completo")
    return unique.astype(np.float64), counts.astype(np.int64)


def exact_standardization(unique: np.ndarray, counts: np.ndarray):
    weights = counts / counts.sum()
    mean = weights @ unique
    centered = unique - mean
    variance = weights @ (centered * centered)
    if np.any(variance <= 0):
        raise ValueError("feature constante encontrada")
    scale = np.sqrt(variance)
    return mean, scale, centered / scale


def gibbs_fit(
    support_z: np.ndarray,
    support_counts: np.ndarray,
    history_z: np.ndarray,
    prior_precision: float = 1.0,
) -> dict:
    """MLE penalizado do log-densidade relativo ao universo uniforme."""
    n = len(history_z)
    log_base = np.log(support_counts.astype(np.float64)) - math.log(float(support_counts.sum()))
    target_mean = history_z.mean(axis=0)
    ridge = prior_precision / max(1, n)

    def objective(theta: np.ndarray):
        logits = log_base + support_z @ theta
        log_partition = float(logsumexp(logits))
        prob = np.exp(logits - log_partition)
        expected = support_z.T @ prob
        value = log_partition - float(target_mean @ theta) + 0.5 * ridge * float(theta @ theta)
        gradient = expected - target_mean + ridge * theta
        return value, gradient

    result = minimize(
        objective,
        np.zeros(history_z.shape[1], dtype=np.float64),
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": 200, "ftol": 1e-12, "gtol": 1e-9},
    )
    theta = result.x
    log_partition = float(logsumexp(log_base + support_z @ theta))
    return {
        "theta": theta,
        "log_partition": log_partition,
        "converged": bool(result.success),
        "iterations": int(result.nit),
        "message": str(result.message),
    }


def expanding_block_gains(
    support_z: np.ndarray,
    support_counts: np.ndarray,
    history_z: np.ndarray,
    burn: int,
    block: int,
) -> tuple[np.ndarray, list[dict]]:
    gains = np.empty(len(history_z) - burn, dtype=np.float64)
    fits: list[dict] = []
    cursor = 0
    for start in range(burn, len(history_z), block):
        end = min(len(history_z), start + block)
        fit = gibbs_fit(support_z, support_counts, history_z[:start])
        gains[cursor:cursor + end - start] = history_z[start:end] @ fit["theta"] - fit["log_partition"]
        fits.append({
            "train_end_index": start,
            "test_start_index": start,
            "test_end_index": end,
            "theta": fit["theta"].tolist(),
            "converged": fit["converged"],
        })
        cursor += end - start
    return gains, fits


def overlap_support() -> tuple[np.ndarray, np.ndarray, float, float]:
    values = np.arange(5, 16, dtype=np.float64)
    counts = np.asarray(
        [math.comb(K, int(k)) * math.comb(N - K, K - int(k)) for k in values],
        dtype=np.int64,
    )
    mean = float(np.average(values, weights=counts))
    scale = float(np.sqrt(np.average((values - mean) ** 2, weights=counts)))
    return ((values - mean) / scale)[:, None], counts, mean, scale


def overlap_history(masks: np.ndarray) -> np.ndarray:
    return np.asarray(
        [int(int(a & b).bit_count()) for a, b in zip(masks[:-1], masks[1:])],
        dtype=np.float64,
    )


def moving_block_sample_indices(n: int, block: int, reps: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    starts = np.arange(max(1, n - block + 1))
    needed = math.ceil(n / block)
    out = np.empty((reps, n), dtype=np.int32)
    offsets = np.arange(block)
    for r in range(reps):
        chosen = rng.choice(starts, size=needed, replace=True)
        out[r] = (chosen[:, None] + offsets).ravel()[:n]
    return out


def bootstrap_diagnostics(gain_matrix: np.ndarray, names: list[str], reps: int, block: int):
    n = gain_matrix.shape[1]
    indices = moving_block_sample_indices(n, block, reps, 9023778)
    means = gain_matrix.mean(axis=1)
    sampled_means = gain_matrix[:, indices].mean(axis=2)
    intervals = np.quantile(sampled_means, [0.025, 0.975], axis=1).T

    centered = gain_matrix - means[:, None]
    centered_means = centered[:, indices].mean(axis=2)
    observed_max = math.sqrt(n) * max(0.0, float(means.max()))
    boot_max = math.sqrt(n) * np.maximum(0.0, centered_means.max(axis=0))
    reality_p = float((1 + np.count_nonzero(boot_max >= observed_max)) / (reps + 1))

    rows = []
    for i, name in enumerate(names):
        p_one_sided = float(
            (1 + np.count_nonzero(centered_means[i] >= means[i])) / (reps + 1)
        )
        rows.append({
            "model": name,
            "n_predictions": n,
            "mean_log_probability_gain_nats": float(means[i]),
            "geometric_probability_ratio": float(math.exp(means[i])),
            "block_bootstrap_95ci": intervals[i].tolist(),
            "one_sided_block_bootstrap_p": p_one_sided,
        })
    return rows, {
        "candidate_count": len(names),
        "block_length": block,
        "bootstrap_repetitions": reps,
        "best_observed_model": names[int(np.argmax(means))],
        "best_observed_gain_nats": float(means.max()),
        "white_reality_check_p": reality_p,
    }


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(a @ b / denom) if denom > 0 else 0.0


def bh_adjust(pvalues: np.ndarray) -> np.ndarray:
    order = np.argsort(pvalues)
    ranked = np.asarray(pvalues, dtype=float)[order]
    adjusted = np.minimum.accumulate(
        (ranked * len(ranked) / np.arange(1, len(ranked) + 1))[::-1]
    )[::-1]
    out = np.empty_like(adjusted)
    out[order] = np.minimum(1.0, adjusted)
    return out


def stability_fits(support_z, support_counts, history_z):
    thirds = np.array_split(np.arange(len(history_z)), 3)
    theta = [gibbs_fit(support_z, support_counts, history_z[idx])["theta"] for idx in thirds]
    return {
        "third_coefficients": [v.tolist() for v in theta],
        "cosine_first_middle": cosine_similarity(theta[0], theta[1]),
        "cosine_first_last": cosine_similarity(theta[0], theta[2]),
        "cosine_middle_last": cosine_similarity(theta[1], theta[2]),
    }


def mask_to_numbers(mask: int) -> str:
    return " ".join(f"{i + 1:02d}" for i in range(N) if (int(mask) >> i) & 1)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def analyze(
    history_path: Path,
    space_map_path: Path,
    output_dir: Path,
    prediction_contest: int,
    burn: int = 1000,
    refit_block: int = 250,
    bootstrap_reps: int = 2000,
    bootstrap_block: int = 25,
    top_k: int = 100,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    contests, history_masks, dates = read_history(history_path)
    if prediction_contest != int(contests[-1]) + 1:
        raise ValueError("prediction_contest deve ser o concurso imediatamente seguinte")

    with np.load(space_map_path) as archive:
        space_masks = np.asarray(archive["mask"], dtype=np.uint32)
    if len(space_masks) != SPACE_SIZE or len(np.unique(space_masks)) != SPACE_SIZE:
        raise ValueError("mapa de mascaras incompleto ou duplicado")

    raw_space = physical_features(space_masks)
    raw_history = physical_features(history_masks)
    unique, counts = compress_feature_space(raw_space)
    mean, scale, support_z = exact_standardization(unique, counts)
    history_z = (raw_history - mean) / scale

    descriptive_p = 2 * norm.sf(np.abs(history_z.mean(axis=0) * math.sqrt(len(history_z))))
    descriptive_q = bh_adjust(descriptive_p)
    feature_diagnostics = [
        {
            "feature": name,
            "universe_mean": float(mean[i]),
            "universe_sd": float(scale[i]),
            "history_mean": float(raw_history[:, i].mean()),
            "standardized_mean_difference": float(history_z[:, i].mean()),
            "iid_z_statistic_descriptive": float(history_z[:, i].mean() * math.sqrt(len(history_z))),
            "iid_p_value_descriptive": float(descriptive_p[i]),
            "bh_q_value_descriptive": float(descriptive_q[i]),
        }
        for i, name in enumerate(FEATURE_NAMES)
    ]

    candidate_names: list[str] = []
    candidate_gains: list[np.ndarray] = []
    final_models: dict[str, dict] = {}
    stability: dict[str, dict] = {}

    for name, index_tuple in MODEL_GROUPS.items():
        idx = np.asarray(index_tuple, dtype=int)
        gains, _ = expanding_block_gains(
            support_z[:, idx], counts, history_z[:, idx], burn, refit_block
        )
        final = gibbs_fit(support_z[:, idx], counts, history_z[:, idx])
        candidate_names.append(name)
        candidate_gains.append(gains)
        final_models[name] = {
            "features": [FEATURE_NAMES[i] for i in idx],
            "theta_per_space_sd": final["theta"].tolist(),
            "log_partition": final["log_partition"],
            "converged": final["converged"],
            "iterations": final["iterations"],
        }
        stability[name] = stability_fits(support_z[:, idx], counts, history_z[:, idx])

    overlap = overlap_history(history_masks)
    overlap_z_support, overlap_counts, overlap_mean, overlap_scale = overlap_support()
    overlap_z = ((overlap - overlap_mean) / overlap_scale)[:, None]
    overlap_gains, _ = expanding_block_gains(
        overlap_z_support, overlap_counts, overlap_z, burn - 1, refit_block
    )
    overlap_final = gibbs_fit(overlap_z_support, overlap_counts, overlap_z)
    overlap_z_stat = float(overlap_z.mean() * math.sqrt(len(overlap_z)))
    candidate_names.append("johnson_inertia")
    candidate_gains.append(overlap_gains)
    final_models["johnson_inertia"] = {
        "features": ["overlap_with_previous"],
        "theta_per_space_sd": overlap_final["theta"].tolist(),
        "beta_per_repeated_number": float(overlap_final["theta"][0] / overlap_scale),
        "log_partition": overlap_final["log_partition"],
        "uniform_overlap_mean": overlap_mean,
        "uniform_overlap_sd": overlap_scale,
        "historical_overlap_mean": float(overlap.mean()),
        "converged": overlap_final["converged"],
    }
    stability["johnson_inertia"] = stability_fits(
        overlap_z_support, overlap_counts, overlap_z
    )

    gain_matrix = np.vstack(candidate_gains)
    diagnostics, reality_check = bootstrap_diagnostics(
        gain_matrix, candidate_names, bootstrap_reps, bootstrap_block
    )
    best_name = reality_check["best_observed_model"]
    best_row = next(r for r in diagnostics if r["model"] == best_name)
    validated = bool(
        reality_check["white_reality_check_p"] < 0.05
        and best_row["block_bootstrap_95ci"][0] > 0
    )

    coefficient_rows: list[dict] = []
    for name, model in final_models.items():
        for feature, theta in zip(model["features"], model["theta_per_space_sd"]):
            coefficient_rows.append({"model": name, "feature": feature, "theta_per_space_sd": theta})
    write_csv(
        output_dir / "physics_coefficients.csv",
        ["model", "feature", "theta_per_space_sd"],
        coefficient_rows,
    )
    write_csv(
        output_dir / "physics_feature_diagnostics.csv",
        list(feature_diagnostics[0]),
        feature_diagnostics,
    )

    score_rows = []
    for offset, contest_index in enumerate(range(burn, len(contests))):
        row = {"contest": int(contests[contest_index]), "date": dates[contest_index]}
        for model_index, name in enumerate(candidate_names):
            row[f"gain_{name}"] = float(gain_matrix[model_index, offset])
        score_rows.append(row)
    write_csv(
        output_dir / "physics_oos_scores.csv",
        ["contest", "date"] + [f"gain_{name}" for name in candidate_names],
        score_rows,
    )
    oos_era_means = {
        name: [float(part.mean()) for part in np.array_split(gain_matrix[i], 3)]
        for i, name in enumerate(candidate_names)
    }

    # Ranking prospectivo privado. Sem validacao, permanece apenas exploratorio.
    rank_model = best_name if best_name != "johnson_inertia" else "full_physical"
    idx = np.asarray(MODEL_GROUPS[rank_model], dtype=int)
    theta = np.asarray(final_models[rank_model]["theta_per_space_sd"])
    all_z = (raw_space[:, idx] - mean[idx]) / scale[idx]
    all_scores = all_z @ theta - final_models[rank_model]["log_partition"]
    take = min(top_k, len(all_scores))
    top_index = np.argpartition(all_scores, -take)[-take:]
    top_index = top_index[np.argsort(all_scores[top_index])[::-1]]
    ranking_rows = [
        {
            "rank": rank + 1,
            "contest": prediction_contest,
            "game": mask_to_numbers(int(space_masks[i])),
            "model": rank_model,
            "phi_log_density_ratio": float(all_scores[i]),
            "relative_density": float(math.exp(min(700.0, all_scores[i]))),
            "validated_signal": validated,
        }
        for rank, i in enumerate(top_index)
    ]
    write_csv(
        output_dir / f"physics_ranking_{prediction_contest}.csv",
        ["rank", "contest", "game", "model", "phi_log_density_ratio", "relative_density", "validated_signal"],
        ranking_rows,
    )

    summary = {
        "author": "Jacson Cruz do Nascimento",
        "method": "exact-universe Gibbs fields with expanding-window out-of-sample validation",
        "space_size": SPACE_SIZE,
        "history_first_contest": int(contests[0]),
        "history_last_contest": int(contests[-1]),
        "history_size": int(len(contests)),
        "prediction_contest": prediction_contest,
        "feature_names": list(FEATURE_NAMES),
        "exact_space_feature_mean": dict(zip(FEATURE_NAMES, mean.tolist())),
        "exact_space_feature_sd": dict(zip(FEATURE_NAMES, scale.tolist())),
        "compressed_feature_states": int(len(unique)),
        "descriptive_feature_tests": feature_diagnostics,
        "overlap_descriptive_test": {
            "uniform_mean": overlap_mean,
            "historical_mean": float(overlap.mean()),
            "standardized_mean_difference": float(overlap_z.mean()),
            "iid_z_statistic_descriptive": overlap_z_stat,
            "iid_p_value_descriptive": float(2 * norm.sf(abs(overlap_z_stat))),
        },
        "validation": {
            "burn_in_contests": burn,
            "refit_block": refit_block,
            "n_out_of_sample": int(gain_matrix.shape[1]),
            "candidate_results": diagnostics,
            "out_of_sample_gain_by_chronological_third": oos_era_means,
            "multiple_testing": reality_check,
            "validated_predictive_parameter": validated,
        },
        "final_models": final_models,
        "era_stability": stability,
        "selected_exploratory_parameter": {
            "name": best_name,
            "definition": "Phi(c)=theta' z(c)-log E_uniform[exp(theta' z(C))]",
            "validated": validated,
        },
        "governance": {
            "results_are_exploratory": True,
            "ranking_file_is_prospective": True,
            "no_guarantee_of_predictive_advantage": True,
        },
    }
    (output_dir / "physics_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", type=Path, required=True)
    parser.add_argument("--space-map", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prediction-contest", type=int, required=True)
    parser.add_argument("--burn", type=int, default=1000)
    parser.add_argument("--refit-block", type=int, default=250)
    parser.add_argument("--bootstrap-reps", type=int, default=2000)
    parser.add_argument("--bootstrap-block", type=int, default=25)
    parser.add_argument("--top-k", type=int, default=100)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = analyze(
        args.history,
        args.space_map,
        args.output,
        args.prediction_contest,
        burn=args.burn,
        refit_block=args.refit_block,
        bootstrap_reps=args.bootstrap_reps,
        bootstrap_block=args.bootstrap_block,
        top_k=args.top_k,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
