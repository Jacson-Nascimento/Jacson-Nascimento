#!/usr/bin/env python3
"""Recover the legacy AXION runner source for audit, without executing it.

This utility uses the repository's existing repair logic, writes the recovered
Python source to a requested output path, and emits a small JSON manifest with
its SHA-256 and recovery metadata. It does not execute the recovered runner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from repair_runner import extract_payload, recover_single_missing_char


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="runner_source.py")
    ap.add_argument("--manifest", default="runner_source_manifest.json")
    args = ap.parse_args()

    legacy = ROOT / "run_full_cycle.py"
    payload = extract_payload(legacy)
    source, position, char = recover_single_missing_char(payload)

    out = Path(args.out)
    out.write_text(source, encoding="utf-8")
    manifest = {
        "legacy_path": str(legacy),
        "recovery_position": position,
        "recovery_character": char,
        "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "source_bytes": len(source.encode("utf-8")),
        "executed": False,
    }
    Path(args.manifest).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
