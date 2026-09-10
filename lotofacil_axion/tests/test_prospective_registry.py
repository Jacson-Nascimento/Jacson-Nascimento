#!/usr/bin/env python3
"""Integrity and statistical tests for the AXION prospective registry."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "nasa_layer" / "prospective_registry.py"
SPEC = importlib.util.spec_from_file_location("prospective_registry", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to import {SCRIPT}")
pr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pr)

EXPECTED_MANIFEST_3780_SHA256 = (
    "b326eb0238b1d26ba2bdcc871992dd5b77f9a6233abf346d4dede74b1471dc36"
)
EXPECTED_AXION_SOURCE_3780_SHA256 = (
    "1e708a87fd0aaccee974e8076835c9ed38defece8cafd3001c3d6c6c957528eb"
)
EXPECTED_AXION_GAME_3780 = [2, 3, 4, 5, 9, 10, 11, 13, 14, 15, 17, 20, 21, 24, 25]
EXPECTED_RANDOM_CONTROL_3780 = [1, 2, 3, 5, 6, 8, 9, 11, 13, 16, 18, 20, 23, 24, 25]


class ExactNullTests(unittest.TestCase):
    def test_single_draw_distribution(self) -> None:
        dist = pr.exact_single_game_sum_distribution(1)
        grid = np.arange(len(dist), dtype=float)
        self.assertAlmostEqual(float(dist.sum()), 1.0, places=12)
        self.assertAlmostEqual(float(np.dot(grid, dist)), 9.0, places=12)
        variance = float(np.dot((grid - 9.0) ** 2, dist))
        self.assertAlmostEqual(variance, 1.5, places=12)

    def test_locked_horizon_25_expectation(self) -> None:
        dist = pr.exact_single_game_sum_distribution(25)
        grid = np.arange(len(dist), dtype=float)
        self.assertAlmostEqual(float(dist.sum()), 1.0, places=12)
        self.assertAlmostEqual(float(np.dot(grid, dist)), 225.0, places=10)

    def test_tail_probability_is_monotone(self) -> None:
        p225 = pr.exact_tail_sum_hits(225, 25)
        p230 = pr.exact_tail_sum_hits(230, 25)
        p240 = pr.exact_tail_sum_hits(240, 25)
        self.assertGreaterEqual(p225, p230)
        self.assertGreaterEqual(p230, p240)
        self.assertGreaterEqual(p240, 0.0)
        self.assertLessEqual(p225, 1.0)


class GovernanceTests(unittest.TestCase):
    def test_deterministic_control_3780_is_frozen(self) -> None:
        self.assertEqual(pr.deterministic_control(3780), EXPECTED_RANDOM_CONTROL_3780)

    def test_manifest_3780_hash_is_frozen(self) -> None:
        path = ROOT / "results" / "nasa_layer" / "prospective_registry" / "baseline_manifest_3780.json"
        raw = path.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), EXPECTED_MANIFEST_3780_SHA256)

    def test_manifest_3780_references_frozen_axion_source(self) -> None:
        path = ROOT / "results" / "nasa_layer" / "prospective_registry" / "baseline_manifest_3780.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(int(obj["contest"]), 3780)
        self.assertEqual(int(obj["created_after_observing_contest"]), 3779)
        self.assertEqual(obj["strategies"]["axion_top_game"], EXPECTED_AXION_GAME_3780)
        self.assertEqual(obj["axion_prediction_manifest_sha256"], EXPECTED_AXION_SOURCE_3780_SHA256)

    def test_validate_game_rejects_duplicates(self) -> None:
        bad = [1] * 15
        with self.assertRaises(RuntimeError):
            pr.validate_game(bad, "duplicate-test")

    def test_missing_prediction_fails_closed(self) -> None:
        impossible = Path("/tmp/axion-test-no-prediction-manifest.json")
        if impossible.exists():
            impossible.unlink()
        with mock.patch.object(pr, "axion_manifest_path", return_value=impossible):
            game, sha, reason = pr.load_axion_game(9999, 9998)
        self.assertIsNone(game)
        self.assertIsNone(sha)
        self.assertEqual(reason, "waiting_for_prediction_9999_manifest")

    def test_bh_adjustment_never_below_raw_p(self) -> None:
        tests = [{"p": 0.01}, {"p": 0.03}, {"p": 0.20}, {"p": 0.80}]
        pr.bh_adjust(tests, "p")
        for row in tests:
            self.assertGreaterEqual(row["q_bh"], row["p"])
            self.assertLessEqual(row["q_bh"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
