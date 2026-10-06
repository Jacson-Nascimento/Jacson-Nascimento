from __future__ import annotations

import csv
from math import floor
from pathlib import Path


def largest_remainder(values: dict[str, int], target_total: int) -> dict[str, int]:
    """Allocate target_total proportionally while preserving the exact total."""
    if target_total < 0:
        raise ValueError("target_total must be non-negative")
    if not values:
        return {}
    if any(value < 0 for value in values.values()):
        raise ValueError("weights must be non-negative")
    weight_total = sum(values.values())
    if weight_total <= 0:
        raise ValueError("sum of weights must be positive")

    quotas = {key: value * target_total / weight_total for key, value in values.items()}
    allocated = {key: floor(quota) for key, quota in quotas.items()}
    remaining = target_total - sum(allocated.values())
    order = sorted(values, key=lambda key: (-(quotas[key] - allocated[key]), key))
    for key in order[:remaining]:
        allocated[key] += 1
    return allocated


def contribution_bounds(
    employee_count: int,
    minimum: float,
    maximum: float,
    union_share: float,
) -> dict[str, float]:
    """Return aggregate lower and upper bounds, without assuming a mean salary."""
    if employee_count < 0:
        raise ValueError("employee_count must be non-negative")
    if minimum < 0 or maximum < minimum:
        raise ValueError("invalid contribution limits")
    if not 0 <= union_share <= 1:
        raise ValueError("union_share must be between 0 and 1")
    gross_min = round(employee_count * minimum, 2)
    gross_max = round(employee_count * maximum, 2)
    return {
        "gross_min": gross_min,
        "gross_max": gross_max,
        "union_min": round(gross_min * union_share, 2),
        "union_max": round(gross_max * union_share, 2),
    }


def read_uf_baseline(path: Path) -> dict[str, int]:
    with path.open(encoding="utf-8", newline="") as handle:
        return {
            row["uf"]: int(row["employees_representation_base"])
            for row in csv.DictReader(handle)
        }


def read_target_total(path: Path, reference_date: str = "2026-06-30") -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["reference_date"] == reference_date:
                return int(row["employees"])
    raise ValueError(f"reference date not found: {reference_date}")


def write_uf_estimates(root: Path) -> None:
    raw = root / "data" / "raw"
    out = root / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    historical = read_uf_baseline(raw / "uf_conecef_2017.csv")
    target = read_target_total(raw / "national_totals.csv")
    allocation = largest_remainder(historical, target)
    historical_total = sum(historical.values())

    path = out / "uf_estimate_2026.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "uf", "historical_representation_base", "historical_share",
            "estimated_employees_2026_06", "evidence_grade",
            "gross_salary_contribution_min", "gross_salary_contribution_max",
            "union_share_min", "union_share_max",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for uf in sorted(historical):
            bounds = contribution_bounds(allocation[uf], 63.00, 310.00, 0.70)
            writer.writerow({
                "uf": uf,
                "historical_representation_base": historical[uf],
                "historical_share": f"{historical[uf] / historical_total:.8f}",
                "estimated_employees_2026_06": allocation[uf],
                "evidence_grade": "C",
                "gross_salary_contribution_min": f"{bounds['gross_min']:.2f}",
                "gross_salary_contribution_max": f"{bounds['gross_max']:.2f}",
                "union_share_min": f"{bounds['union_min']:.2f}",
                "union_share_max": f"{bounds['union_max']:.2f}",
            })


def write_base_estimates(root: Path) -> None:
    raw = root / "data" / "raw"
    out = root / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    source_path = raw / "base_counts_2026.csv"
    target_path = out / "base_estimate_2026.csv"

    with source_path.open(encoding="utf-8", newline="") as source, target_path.open(
        "w", encoding="utf-8", newline=""
    ) as target:
        fields = [
            "base_id", "uf", "base_name", "aptos", "evidence_grade", "is_approximate",
            "source_id", "gross_salary_contribution_min", "gross_salary_contribution_max",
            "union_share_min", "union_share_max",
        ]
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for row in csv.DictReader(source):
            if not row.get("aptos"):
                continue
            aptos = int(row["aptos"])
            bounds = contribution_bounds(aptos, 63.00, 310.00, 0.70)
            writer.writerow({
                "base_id": row["base_id"],
                "uf": row["uf"],
                "base_name": row["base_name"],
                "aptos": aptos,
                "evidence_grade": row["evidence_grade"],
                "is_approximate": row["is_approximate"],
                "source_id": row["source_id"],
                "gross_salary_contribution_min": f"{bounds['gross_min']:.2f}",
                "gross_salary_contribution_max": f"{bounds['gross_max']:.2f}",
                "union_share_min": f"{bounds['union_min']:.2f}",
                "union_share_max": f"{bounds['union_max']:.2f}",
            })


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    write_uf_estimates(root)
    write_base_estimates(root)


if __name__ == "__main__":
    main()
