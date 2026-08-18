#!/usr/bin/env python3
"""Sensibilidade dos critérios mínimos de elegibilidade dos compradores.

Compara combinações de número mínimo de fornecedores e instrumentos usando as
métricas já calculadas para janeiro-fevereiro de 2025. Acrescenta HHI
normalizado pelo número de fornecedores para separar a concentração além do
mínimo mecânico 1/N.

Para N > 1:
    HHI_norm = (HHI - 1/N) / (1 - 1/N)

HHI_norm = 0 quando os valores estão igualmente distribuídos entre os N
fornecedores observados; aproxima-se de 1 quando um fornecedor domina a carteira.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"results"
INP=RES/"carteira_jan_fev_2025_diagnostico"/"metricas_compradores_jan_fev.csv"
OUT=RES/"robustez_elegibilidade_jan_fev_2025"
OUT.mkdir(parents=True,exist_ok=True)
CRITERIA=[(3,5),(5,10),(5,20),(10,20)]


def corr(g,a,b):
    z=g[[a,b]].replace([np.inf,-np.inf],np.nan).dropna()
    if len(z)<3:return (np.nan,np.nan)
    return spearmanr(z[a],z[b])


def normalized_hhi(hhi,n):
    h=pd.to_numeric(hhi,errors="coerce")
    nn=pd.to_numeric(n,errors="coerce")
    floor=1/nn
    den=1-floor
    out=(h-floor)/den
    return out.where(nn>1).clip(lower=0,upper=1)


def main():
    d=pd.read_csv(INP,dtype={"orgao_cnpj":"string"},low_memory=False)
    d["portfolio_hhi_normalizado"]=normalized_hhi(d["portfolio_hhi"],d["n_fornecedores"])
    d["count_hhi_normalizado"]=normalized_hhi(d["count_hhi"],d["n_fornecedores"])
    d["hhi_normalizado_gap_valor_frequencia"]=d["portfolio_hhi_normalizado"]-d["count_hhi_normalizado"]

    rows=[]
    membership=[]
    for nf,ni in CRITERIA:
        g=d[(d["n_fornecedores"]>=nf)&(d["n_instrumentos"]>=ni)].copy()
        label=f"nforn>={nf}_ninstr>={ni}"
        qh=g["portfolio_hhi"].quantile(.75); qe=g["exposicao_strength"].quantile(.75)
        rho_pc,p_pc=corr(g,"portfolio_hhi","count_hhi")
        rho_pe,p_pe=corr(g,"portfolio_hhi","exposicao_strength")
        rho_np,p_np=corr(g,"portfolio_hhi_normalizado","exposicao_strength")
        rows.append({
            "criterio":label,"min_fornecedores":nf,"min_instrumentos":ni,"n_compradores":len(g),
            "portfolio_hhi_media":g["portfolio_hhi"].mean(),"portfolio_hhi_mediana":g["portfolio_hhi"].median(),
            "portfolio_hhi_p25":g["portfolio_hhi"].quantile(.25),"portfolio_hhi_p75":qh,
            "portfolio_hhi_normalizado_mediana":g["portfolio_hhi_normalizado"].median(),
            "portfolio_hhi_normalizado_p25":g["portfolio_hhi_normalizado"].quantile(.25),
            "portfolio_hhi_normalizado_p75":g["portfolio_hhi_normalizado"].quantile(.75),
            "count_hhi_mediana":g["count_hhi"].median(),
            "count_hhi_normalizado_mediana":g["count_hhi_normalizado"].median(),
            "portfolio_neff_mediana":g["portfolio_neff"].median(),
            "portfolio_cr1_mediana":g["portfolio_cr1"].median(),"portfolio_cr4_mediana":g["portfolio_cr4"].median(),
            "spearman_hhi_count":rho_pc,"p_hhi_count":p_pc,
            "spearman_hhi_exposure_strength":rho_pe,"p_hhi_exposure_strength":p_pe,
            "spearman_hhi_norm_exposure_strength":rho_np,"p_hhi_norm_exposure_strength":p_np,
            "hhi_maior_count_n":int((g["portfolio_hhi"]>g["count_hhi"]).sum()),
            "hhi_maior_count_pct":float((g["portfolio_hhi"]>g["count_hhi"]).mean()*100) if len(g) else np.nan,
            "hhi_norm_maior_count_norm_pct":float((g["portfolio_hhi_normalizado"]>g["count_hhi_normalizado"]).mean()*100) if len(g) else np.nan,
            "hhi_baixo_exposicao_alta_n":int(((g["portfolio_hhi"]<qh)&(g["exposicao_strength"]>=qe)).sum()),
            "hhi_baixo_exposicao_alta_pct":float(((g["portfolio_hhi"]<qh)&(g["exposicao_strength"]>=qe)).mean()*100) if len(g) else np.nan,
            "hhi_alto_exposicao_alta_n":int(((g["portfolio_hhi"]>=qh)&(g["exposicao_strength"]>=qe)).sum()),
        })
        tmp=g[["orgao_cnpj","portfolio_hhi","portfolio_hhi_normalizado","count_hhi","count_hhi_normalizado"]].copy()
        tmp["criterio"]=label; membership.append(tmp)
    result=pd.DataFrame(rows)
    result.to_csv(OUT/"sensibilidade_criterios.csv",index=False,encoding="utf-8-sig")
    pd.concat(membership,ignore_index=True).to_csv(OUT/"membros_por_criterio.csv.gz",index=False,compression="gzip")

    base=result.iloc[0]
    changes=[]
    for _,r in result.iterrows():
        changes.append({
            "criterio":r["criterio"],
            "delta_hhi_mediana_vs_3_5":float(r["portfolio_hhi_mediana"]-base["portfolio_hhi_mediana"]),
            "delta_hhi_normalizado_mediana_vs_3_5":float(r["portfolio_hhi_normalizado_mediana"]-base["portfolio_hhi_normalizado_mediana"]),
            "delta_neff_mediana_vs_3_5":float(r["portfolio_neff_mediana"]-base["portfolio_neff_mediana"]),
            "delta_cr1_mediana_vs_3_5":float(r["portfolio_cr1_mediana"]-base["portfolio_cr1_mediana"]),
            "delta_cr4_mediana_vs_3_5":float(r["portfolio_cr4_mediana"]-base["portfolio_cr4_mediana"]),
        })
    pd.DataFrame(changes).to_csv(OUT/"deltas_vs_criterio_base.csv",index=False,encoding="utf-8-sig")

    summary={
        "criterio_base":"nforn>=3_ninstr>=5",
        "formula_hhi_normalizado":"(HHI - 1/N) / (1 - 1/N)",
        "criterios":result.to_dict(orient="records"),
        "regra_decisao":"O HHI bruto pode cair mecanicamente em carteiras maiores. HHI normalizado, divergência valor-frequência e exposição estrutural devem ser avaliados conjuntamente antes de fixar o corte principal.",
    }
    (OUT/"resumo_robustez_elegibilidade.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(result.to_string(index=False))

if __name__=="__main__":main()
