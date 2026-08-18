#!/usr/bin/env python3
"""Consolida a trajetória dos coeficientes até junho de 2025.

Objetivo: documentar convergência/instabilidade sem selecionar especificações
retrospectivamente. HHI usa cinco janelas comparáveis (jan-fev a jan-jun).
Gap valor-contagem e exposição Strength usam quatro janelas (jan-mar a jan-jun).
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = RES / "convergencia_coeficientes_jan_jun_2025"
OUT.mkdir(parents=True, exist_ok=True)

KEY = ["log_populacao", "log_despesa_pc", "log_n_fornecedores", "log_instr_por_forn"]
SOURCES = {
    "jan_fev": RES / "robustez_modelos_regiao_fractional_jan_fev_2025" / "coeficientes_robustez.csv",
    "jan_mar": RES / "modelos_associativos_jan_mar_2025" / "coeficientes_modelos.csv",
    "jan_abr": RES / "modelos_associativos_jan_abr_2025" / "coeficientes_modelos.csv",
    "jan_mai": RES / "modelos_associativos_jan_mai_2025" / "coeficientes_modelos.csv",
    "jan_jun": RES / "modelos_associativos_jan_jun_2025" / "coeficientes_modelos.csv",
}
ORDER = {"jan_fev": 2, "jan_mar": 3, "jan_abr": 4, "jan_mai": 5, "jan_jun": 6}


def load_all() -> pd.DataFrame:
    frames=[]
    for janela,path in SOURCES.items():
        if not path.exists():
            raise FileNotFoundError(path)
        d=pd.read_csv(path, low_memory=False)
        d["janela"]=janela
        d["mes_final"]=ORDER[janela]
        d["coef"]=pd.to_numeric(d["coef"],errors="coerce")
        d["p"]=pd.to_numeric(d["p"],errors="coerce")
        frames.append(d)
    return pd.concat(frames, ignore_index=True, sort=False)


def sign(v: float) -> int:
    if pd.isna(v) or abs(v) < 1e-12:
        return 0
    return 1 if v > 0 else -1


def summarize(panel: pd.DataFrame, family: str) -> pd.DataFrame:
    rows=[]
    for (model,term),g in panel.groupby(["modelo","termo"], sort=False):
        g=g.sort_values("mes_final")
        coefs=g["coef"].astype(float).tolist()
        ps=g["p"].astype(float).tolist()
        signs=[sign(v) for v in coefs]
        nonzero=[s for s in signs if s != 0]
        sign_changes=sum(1 for a,b in zip(nonzero,nonzero[1:]) if a != b)
        prev=coefs[-2] if len(coefs)>=2 else np.nan
        last=coefs[-1] if coefs else np.nan
        first=coefs[0] if coefs else np.nan
        rows.append({
            "familia":family,
            "modelo":model,
            "termo":term,
            "n_janelas":len(g),
            "janelas":"|".join(g["janela"].astype(str)),
            "coeficientes":"|".join(f"{v:.12g}" for v in coefs),
            "p_values":"|".join(f"{v:.12g}" for v in ps),
            "sinais":"|".join(str(s) for s in signs),
            "mudancas_sinal":sign_changes,
            "coef_primeira":first,
            "coef_penultima":prev,
            "coef_ultima":last,
            "delta_ultima_vs_penultima":None if len(coefs)<2 else last-prev,
            "razao_abs_ultima_penultima":None if len(coefs)<2 or abs(prev)<1e-12 else abs(last)/abs(prev),
            "razao_abs_ultima_primeira":None if abs(first)<1e-12 else abs(last)/abs(first),
            "n_significativo_5pct":sum(p < .05 for p in ps),
            "mesmo_sinal_nao_nulo":bool(len(set(nonzero)) <= 1),
        })
    return pd.DataFrame(rows)


def get_row(summary: pd.DataFrame, model: str, term: str) -> dict | None:
    z=summary[(summary.modelo==model)&(summary.termo==term)]
    if z.empty:return None
    r=z.iloc[0]
    return {
        "coef_primeira":float(r.coef_primeira),
        "coef_ultima":float(r.coef_ultima),
        "delta_ultima_vs_penultima":None if pd.isna(r.delta_ultima_vs_penultima) else float(r.delta_ultima_vs_penultima),
        "razao_abs_ultima_penultima":None if pd.isna(r.razao_abs_ultima_penultima) else float(r.razao_abs_ultima_penultima),
        "mudancas_sinal":int(r.mudancas_sinal),
        "n_significativo_5pct":int(r.n_significativo_5pct),
        "n_janelas":int(r.n_janelas),
    }


def main():
    d=load_all()
    hhi=d[d["modelo"].isin(["O2_HHI_norm_regiao","F2_HHI_norm_regiao"]) & d["termo"].isin(KEY)].copy()
    hhi=hhi.sort_values(["modelo","termo","mes_final"])
    hhi.to_csv(OUT/"painel_hhi_coeficientes.csv",index=False,encoding="utf-8-sig")

    later=d[d["janela"].isin(["jan_mar","jan_abr","jan_mai","jan_jun"])].copy()
    exposure=later[(later["modelo"]=="O4_Exposicao_strength_regiao") & later["termo"].isin(KEY)].copy()
    gap=later[(later["modelo"]=="O3_Gap_regiao") & later["termo"].isin(KEY)].copy()
    exposure.sort_values(["termo","mes_final"]).to_csv(OUT/"painel_exposicao_strength_coeficientes.csv",index=False,encoding="utf-8-sig")
    gap.sort_values(["termo","mes_final"]).to_csv(OUT/"painel_gap_coeficientes.csv",index=False,encoding="utf-8-sig")

    summaries=pd.concat([
        summarize(hhi,"hhi_norm"),
        summarize(exposure,"exposicao_strength"),
        summarize(gap,"gap_valor_contagem"),
    ],ignore_index=True)
    summaries.to_csv(OUT/"resumo_convergencia_coeficientes.csv",index=False,encoding="utf-8-sig")

    summary={
        "natureza":"Diagnóstico descritivo de trajetória de coeficientes; não altera especificação nem produz inferência causal adicional.",
        "janelas_hhi":["jan_fev","jan_mar","jan_abr","jan_mai","jan_jun"],
        "janelas_exposicao_gap":["jan_mar","jan_abr","jan_mai","jan_jun"],
        "hhi_ols_populacao":get_row(summaries,"O2_HHI_norm_regiao","log_populacao"),
        "hhi_ols_n_fornecedores":get_row(summaries,"O2_HHI_norm_regiao","log_n_fornecedores"),
        "hhi_ols_despesa_pc":get_row(summaries,"O2_HHI_norm_regiao","log_despesa_pc"),
        "hhi_ols_recorrencia":get_row(summaries,"O2_HHI_norm_regiao","log_instr_por_forn"),
        "hhi_fractional_populacao":get_row(summaries,"F2_HHI_norm_regiao","log_populacao"),
        "hhi_fractional_n_fornecedores":get_row(summaries,"F2_HHI_norm_regiao","log_n_fornecedores"),
        "hhi_fractional_recorrencia":get_row(summaries,"F2_HHI_norm_regiao","log_instr_por_forn"),
        "exposicao_recorrencia":get_row(summaries,"O4_Exposicao_strength_regiao","log_instr_por_forn"),
        "exposicao_n_fornecedores":get_row(summaries,"O4_Exposicao_strength_regiao","log_n_fornecedores"),
        "gap_recorrencia":get_row(summaries,"O3_Gap_regiao","log_instr_por_forn"),
        "regra_interpretacao":"Descrever trajetórias, mudanças de sinal, persistência de significância e variação entre janelas; não definir estabilidade por limiar pós-hoc."
    }
    (OUT/"resumo_convergencia.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
