#!/usr/bin/env python3
"""Orquestra captura, validação, consolidação e análise acumulada PNCP para meses restantes de 2025.

Uso local/CI:
  python scripts/executar_pncp_meses_restantes_2025.py --start-month 8 --end-month 12

Características:
- divide cada mês em janelas de até 4 dias;
- reaproveita checkpoints existentes;
- duas tentativas por partição, com espera entre tentativas;
- consolida cada mês com o validador oficial;
- recalcula o acumulado global após cada mês;
- não altera a especificação estatística vigente.

A persistência Git é responsabilidade do workflow, para manter commits auditáveis por mês.
"""
from __future__ import annotations

import argparse
import calendar
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results" / "pncp_mensal"


def run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def partitions(month: int):
    last = calendar.monthrange(2025, month)[1]
    start = 1
    while start <= last:
        end = min(start + 3, last)
        yield start, end
        start = end + 1


def collect(month: int, day1: int, day2: int, retries: int, wait_seconds: int) -> None:
    label = f"2025-{month:02d}-d{day1:02d}-d{day2:02d}"
    data = DATA / f"pncp_{label}_municipal_pj.csv.gz"
    summary = RES / f"{label}_resumo.json"
    if data.exists() and summary.exists():
        print(f"{label}: checkpoint existente, coleta ignorada.", flush=True)
        return

    start = f"2025{month:02d}{day1:02d}"
    end = f"2025{month:02d}{day2:02d}"
    for attempt in range(1, retries + 1):
        try:
            run(sys.executable, "scripts/coletar_pncp_periodo.py", "--start", start, "--end", end, "--label", label)
            return
        except subprocess.CalledProcessError:
            if attempt == retries:
                raise
            print(f"{label}: tentativa {attempt}/{retries} falhou; aguardando {wait_seconds}s.", flush=True)
            time.sleep(wait_seconds)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-month", type=int, default=8, choices=range(1, 13))
    ap.add_argument("--end-month", type=int, default=12, choices=range(1, 13))
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--wait-seconds", type=int, default=60)
    args = ap.parse_args()
    if args.start_month > args.end_month:
        ap.error("--start-month deve ser <= --end-month")

    for month in range(args.start_month, args.end_month + 1):
        print(f"\n=== PNCP 2025-{month:02d} ===", flush=True)
        for d1, d2 in partitions(month):
            collect(month, d1, d2, args.retries, args.wait_seconds)
        run(sys.executable, "scripts/consolidar_mes_pncp_2025.py", "--month", str(month))
        run(sys.executable, "scripts/analisar_acumulado_2025_global.py", "--month", str(month))


if __name__ == "__main__":
    main()
