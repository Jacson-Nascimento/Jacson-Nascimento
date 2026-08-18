#!/usr/bin/env python3
"""Bootstrap condicional dos padrões diagnósticos janeiro-fevereiro de 2025.

Objetivo: quantificar a estabilidade estatística, dentro da amostra observada,
de medianas e proporções centrais do artigo.

IMPORTANTE: os intervalos bootstrap são condicionais à amostra PNCP observada.
Eles não corrigem viés de cobertura, seleção de compradores ou publicações
tardias e não devem ser descritos como intervalos de representatividade
nacional.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"results"
INP=RES/"carteira_jan_fev_2025_diagnostico"/"metricas_compradores_jan_fev.csv"
OUT=RES/"bootstrap_jan_fev_2025"
OUT.mkdir(parents=True,exist_ok=True)
SEED=20260818
B=5000


def hhi_norm(hhi,n):
    n=np.asarray(n,dtype=float); h=np.asarray(hhi,dtype=float)
    floor=1/n; den=1-floor
    out=np.where(n>1,(h-floor)/den,np.nan)
    return np.clip(out,0,1)


def summary_stat(g):
    qh=np.quantile(g["portfolio_hhi"],.75)
    qe=np.quantile(g["exposicao_strength"],.75)
    return {
        "hhi_mediana":float(np.median(g["portfolio_hhi"])),
        "hhi_norm_mediana":float(np.nanmedian(g["portfolio_hhi_normalizado"])),
        "count_hhi_mediana":float(np.median(g["count_hhi"])),
        "neff_mediana":float(np.median(g["portfolio_neff"])),
        "cr1_mediana":float(np.median(g["portfolio_cr1"])),
        "cr4_mediana":float(np.median(g["portfolio_cr4"])),
        "share_hhi_maior_count":float(np.mean(g["portfolio_hhi"]>g["count_hhi"])),
        "share_exposicao_oculta":float(np.mean((g["portfolio_hhi"]<qh)&(g["exposicao_strength"]>=qe))),
        "share_hhi_alto_exposicao_alta":float(np.mean((g["portfolio_hhi"]>=qh)&(g["exposicao_strength"]>=qe))),
    }


def main():
    d=pd.read_csv(INP,low_memory=False)
    g=d[(d["n_fornecedores"]>=3)&(d["n_instrumentos"]>=5)].copy().reset_index(drop=True)
    g["portfolio_hhi_normalizado"]=hhi_norm(g["portfolio_hhi"],g["n_fornecedores"])
    point=summary_stat(g)
    rng=np.random.default_rng(SEED)
    rows=[]
    n=len(g)
    for b in range(B):
        idx=rng.integers(0,n,size=n)
        s=g.iloc[idx]
        z=summary_stat(s); z["replicacao"]=b+1; rows.append(z)
    boot=pd.DataFrame(rows)
    boot.to_csv(OUT/"replicacoes_bootstrap.csv.gz",index=False,compression="gzip")
    ci=[]
    for metric,val in point.items():
        x=boot[metric].dropna()
        ci.append({
            "metrica":metric,"estimativa_pontual":val,
            "bootstrap_media":float(x.mean()),"bootstrap_desvio":float(x.std(ddof=1)),
            "ci95_p025":float(x.quantile(.025)),"ci95_p975":float(x.quantile(.975)),
            "B":B,"n_compradores":n,
        })
    cidf=pd.DataFrame(ci)
    cidf.to_csv(OUT/"intervalos_bootstrap.csv",index=False,encoding="utf-8-sig")
    resumo={
        "escopo":"Compradores jan-fev 2025 com >=3 fornecedores e >=5 instrumentos.",
        "n_compradores":n,"replicacoes":B,"seed":SEED,
        "natureza_intervalos":"Condicionais à amostra PNCP observada; não corrigem cobertura/seleção.",
        "intervalos":ci,
    }
    (OUT/"resumo_bootstrap.json").write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding="utf-8")
    print(cidf.to_string(index=False))

if __name__=="__main__":main()
