#!/usr/bin/env python3
"""Compatibility runner for the legacy Axion payload.

The original run_full_cycle.py contains a zlib-compressed Python program encoded
as Base64. One Base64 data character was lost in the committed payload. This
runner reconstructs that single missing character deterministically by accepting
only a candidate that:
  1. is valid Base64,
  2. is a valid zlib stream,
  3. decodes as UTF-8 Python source, and
  4. compiles successfully.

No lottery result or model output is altered by this compatibility layer.
"""
from __future__ import annotations

import base64
import re
import zlib
from pathlib import Path

BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def extract_payload(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r'_PAYLOAD\s*=\s*"""(?P<payload>.*?)"""',
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise RuntimeError(f"_PAYLOAD not found in {path}")
    return "".join(match.group("payload").split())


def validate_candidate(payload: str) -> str | None:
    try:
        compressed = base64.b64decode(payload, validate=True)
        source_bytes = zlib.decompress(compressed)
        source = source_bytes.decode("utf-8")
        compile(source, "run_full_cycle.py", "exec")
        return source
    except Exception:
        return None


def recover_single_missing_char(payload: str) -> tuple[str, int, str]:
    direct = validate_candidate(payload)
    if direct is not None:
        return direct, -1, ""

    data = payload.rstrip("=")
    if len(data) % 4 != 1:
        raise RuntimeError(
            "Legacy payload is invalid, but its Base64 length does not match "
            "the known single-character-loss signature."
        )

    repaired_padding = "=="
    total = len(data) + 1
    for pos in range(total):
        prefix = data[:pos]
        suffix = data[pos:]
        for char in BASE64_ALPHABET:
            candidate = prefix + char + suffix + repaired_padding
            source = validate_candidate(candidate)
            if source is not None:
                return source, pos, char

        if pos and pos % 1000 == 0:
            print(f"[Axion repair] tested {pos}/{total} insertion positions", flush=True)

    raise RuntimeError(
        "Unable to reconstruct the legacy payload by restoring one Base64 character."
    )


def main() -> None:
    legacy_path = Path(__file__).with_name("run_full_cycle.py")
    payload = extract_payload(legacy_path)
    source, position, char = recover_single_missing_char(payload)

    if position >= 0:
        print(
            f"[Axion repair] recovered legacy payload at Base64 position "
            f"{position} using character {char!r}.",
            flush=True,
        )
    else:
        print("[Axion repair] legacy payload is already valid.", flush=True)

    namespace = {
        "__name__": "__main__",
        "__file__": str(legacy_path),
        "__package__": None,
    }
    exec(compile(source, str(legacy_path), "exec"), namespace, namespace)


if __name__ == "__main__":
    main()
