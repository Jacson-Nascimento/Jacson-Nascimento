#!/usr/bin/env python3
"""Gera partições resilientes de 4 dias para um mês de 2025.

Uso:
  python scripts/planejar_particoes_mes_2025.py --month 8

Saída TSV: data_inicial, data_final, label.
"""
from __future__ import annotations
import argparse
import calendar


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--month", type=int, required=True, choices=range(1, 13))
    a = p.parse_args()
    m = a.month
    last = calendar.monthrange(2025, m)[1]
    for start in range(1, last + 1, 4):
        end = min(start + 3, last)
        ini = f"2025{m:02d}{start:02d}"
        fim = f"2025{m:02d}{end:02d}"
        label = f"2025-{m:02d}-d{start:02d}-d{end:02d}"
        print(f"{ini}\t{fim}\t{label}")


if __name__ == "__main__":
    main()
