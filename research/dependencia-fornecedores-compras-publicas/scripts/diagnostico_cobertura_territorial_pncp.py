#!/usr/bin/env python3
"""Diagnóstico de presença territorial do PNCP contra o universo municipal do IBGE.

A ausência de um município em determinado mês NÃO é tratada como prova de falha
de cobertura: pode refletir ausência real de instrumentos publicados. Por isso o
indicador é denominado presença/continuidade observacional.

Uso:
  python scripts/diagnostico_cobertura_territorial_pncp.py --month 6
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results"
IBGE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"


def clean_code(s):
    x = s.astype("string").str.replace(r"\D", "", regex=True)
    return x.str.zfill(7)


def fetch_ibge():
    r = requests.get(IBGE_URL, timeout=120, headers={"User-Agent":"Pesquisa-Academica-PNCP-Cobertura/1.0"})
    r.raise_for_status()
    rows = r.json()
    out = []
    for x in rows:
        mic = x.get("microrregiao") or {}
        meso = mic.get("mesorregiao") or {}
        uf = meso.get("UF") or {}
        reg = uf.get("regiao") or {}
        out.append({
            "municipio_ibge": str(x.get("id", "")),
            "municipio_ibge_nome": x.get("nome"),
            "uf": uf.get("sigla"),
            "uf_nome": uf.get("nome"),
            "regiao": reg.get("nome"),
        })
    d = pd.DataFrame(out)
    d["municipio_ibge"] = clean_code(d["municipio_ibge"])
    return d.drop_duplicates("municipio_ibge")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--month", type=int, required=True, choices=range(1, 13))
    args = p.parse_args()
    mfinal = args.month
    out = RES / f"cobertura_territorial_pncp_2025_{mfinal:02d}"
    out.mkdir(parents=True, exist_ok=True)

    ibge = fetch_ibge()
    ibge.to_csv(out / "universo_municipios_ibge_snapshot.csv", index=False, encoding="utf-8-sig")
    universe = set(ibge.municipio_ibge.dropna().astype(str))

    frames = []
    month_rows = []
    for m in range(1, mfinal + 1):
        path = DATA / f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        if not path.exists():
            raise FileNotFoundError(path)
        d = pd.read_csv(path, dtype={"municipio_ibge":"string","orgao_cnpj":"string"}, low_memory=False)
        d["municipio_ibge"] = clean_code(d["municipio_ibge"])
        d["ano_assinatura"] = pd.to_numeric(d["ano_assinatura"], errors="coerce")
        d["mes_publicacao_ref"] = m
        signed = d[d.ano_assinatura.eq(2025)].copy()
        frames.append(signed)
        mun = set(signed.municipio_ibge.dropna().astype(str))
        valid = mun & universe
        outside = mun - universe
        month_rows.append({
            "mes": m,
            "instrumentos_pj_assinados_2025": int(len(signed)),
            "compradores_unicos": int(signed.orgao_cnpj.nunique()),
            "municipios_observados": int(len(mun)),
            "municipios_validos_ibge": int(len(valid)),
            "municipios_fora_universo_ibge": int(len(outside)),
            "presenca_universo_pct": len(valid) / max(len(universe), 1) * 100,
        })

    allx = pd.concat(frames, ignore_index=True)
    allx["municipio_ibge"] = clean_code(allx["municipio_ibge"])
    observed = set(allx.municipio_ibge.dropna().astype(str))
    valid_obs = observed & universe
    outside_obs = observed - universe

    # Presença observacional por município ao longo das janelas de publicação.
    pm = (allx[allx.municipio_ibge.isin(universe)]
          .groupby(["municipio_ibge","mes_publicacao_ref"], dropna=False)
          .agg(instrumentos=("id_contrato","nunique"), compradores=("orgao_cnpj","nunique"))
          .reset_index())
    continuity = (pm.groupby("municipio_ibge")
                  .agg(meses_observados=("mes_publicacao_ref","nunique"),
                       primeiro_mes=("mes_publicacao_ref","min"),
                       ultimo_mes=("mes_publicacao_ref","max"),
                       instrumentos=("instrumentos","sum"),
                       compradores_mes_soma=("compradores","sum"))
                  .reset_index())
    continuity = ibge.merge(continuity, on="municipio_ibge", how="left")
    for c in ["meses_observados","instrumentos","compradores_mes_soma"]:
        continuity[c] = continuity[c].fillna(0).astype(int)
    continuity.to_csv(out / "presenca_observacional_municipios.csv", index=False, encoding="utf-8-sig")

    # Cobertura observada por UF em relação ao universo IBGE do próprio estado.
    seen = continuity[continuity.meses_observados.gt(0)].copy()
    den = ibge.groupby(["uf","regiao"], dropna=False).size().rename("municipios_universo").reset_index()
    num = seen.groupby(["uf","regiao"], dropna=False).size().rename("municipios_observados").reset_index()
    uf = den.merge(num, on=["uf","regiao"], how="left")
    uf["municipios_observados"] = uf.municipios_observados.fillna(0).astype(int)
    uf["presenca_pct"] = uf.municipios_observados / uf.municipios_universo * 100
    uf.to_csv(out / "presenca_por_uf.csv", index=False, encoding="utf-8-sig")

    dist = (continuity.groupby("meses_observados").size().rename("municipios").reset_index())
    dist["pct_universo"] = dist.municipios / len(ibge) * 100
    dist.to_csv(out / "distribuicao_meses_observados.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(month_rows).to_csv(out / "presenca_por_mes.csv", index=False, encoding="utf-8-sig")

    # Entrantes observacionais: primeira aparição em cada mês de publicação.
    entrants = (continuity[continuity.meses_observados.gt(0)]
                .groupby("primeiro_mes").size().rename("novos_municipios_observados").reset_index())
    entrants.to_csv(out / "primeira_aparicao_por_mes.csv", index=False, encoding="utf-8-sig")

    n = len(ibge)
    obs = continuity.meses_observados
    summary = {
        "mes_final_publicacao": f"2025-{mfinal:02d}",
        "universo_ibge_municipios": int(n),
        "municipios_observados_ao_menos_1_mes": int((obs >= 1).sum()),
        "presenca_universo_ao_menos_1_mes_pct": float((obs >= 1).sum() / n * 100),
        "municipios_observados_ao_menos_metade_meses": int((obs >= ((mfinal + 1)//2)).sum()),
        "municipios_observados_todos_meses": int((obs == mfinal).sum()),
        "pct_observados_todos_meses_universo": float((obs == mfinal).sum() / n * 100),
        "mediana_meses_observados_entre_municipios_presentes": None if not (obs > 0).any() else float(obs[obs > 0].median()),
        "municipios_pncp_fora_universo_ibge": sorted(outside_obs),
        "n_municipios_pncp_fora_universo_ibge": int(len(outside_obs)),
        "instrumentos_pj_assinados_2025_acumulados": int(len(allx)),
        "compradores_institucionais_acumulados": int(allx.orgao_cnpj.nunique()),
        "nota_metodologica": "Presença mensal no PNCP não equivale a completude de reporte. Município sem instrumento em um mês pode simplesmente não ter contratação publicada. O indicador é uma medida de presença/continuidade observacional e um limite inferior para avaliação de cobertura.",
        "fonte_universo": IBGE_URL,
    }
    (out / "resumo_cobertura_territorial.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
