#!/usr/bin/env python3
"""Reanálise validada do acumulado janeiro-março de 2025.

Não coleta dados. Usa as bases mensais já consolidadas de janeiro, fevereiro e
março e aplica as decisões metodológicas posteriores aos primeiros diagnósticos:

- PortfolioHHI e CountHHI bruto + normalizado pelo piso 1/N;
- centralidade/exposição calculadas na rede GLOBAL observada;
- Strength global como ordenação principal dos choques;
- Degree global como especificação complementar;
- 1.000 remoções aleatórias por cenário, semente fixa;
- critérios de elegibilidade 3 fornecedores / 5 instrumentos apenas como corte
  diagnóstico base, acompanhado de estabilidade 3/5, 5/10, 5/20 e 10/20.

Os resultados continuam sendo coorte parcial de PUBLICAÇÃO e não equivalem ao
ano completo de contratos assinados em 2025.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results"
OUT = RES / "carteira_acumulada_2025_03_validada"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260818
DRAWS = 1000
CRITERIA = [(3,5),(5,10),(5,20),(10,20)]


def parse_mixed(s):
    try:
        return pd.to_datetime(s, errors="coerce", format="mixed")
    except TypeError:
        return pd.to_datetime(s, errors="coerce")


def load_month(m: int):
    p = DATA / f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
    if not p.exists():
        raise FileNotFoundError(p)
    d = pd.read_csv(
        p,
        dtype={"id_contrato":"string","orgao_cnpj":"string","fornecedor_id_limpo":"string","municipio_ibge":"string"},
        low_memory=False,
    )
    d["ano_assinatura"] = pd.to_numeric(d["ano_assinatura"], errors="coerce")
    d["valorInicial"] = pd.to_numeric(d["valorInicial"], errors="coerce")
    d["lag_publicacao_dias"] = pd.to_numeric(d["lag_publicacao_dias"], errors="coerce")
    d["data_publicacao"] = parse_mixed(d["data_publicacao"])
    d["mes_publicacao"] = m
    return d


def hhi_norm(hhi, n):
    h = pd.to_numeric(hhi, errors="coerce")
    nn = pd.to_numeric(n, errors="coerce")
    floor = 1.0 / nn
    return ((h - floor) / (1.0 - floor)).where(nn > 1).clip(0,1)


def build_metrics(acc):
    x = acc[acc["ano_assinatura"].eq(2025) & acc["valorInicial"].gt(0)].copy()
    rel = (
        x.groupby(["orgao_cnpj","fornecedor_id_limpo"], dropna=False)
        .agg(valor_relacao=("valorInicial","sum"), n_instrumentos=("id_contrato","nunique"))
        .reset_index()
    )
    rel["share_valor"] = rel["valor_relacao"] / rel.groupby("orgao_cnpj")["valor_relacao"].transform("sum")
    rel["share_contagem"] = rel["n_instrumentos"] / rel.groupby("orgao_cnpj")["n_instrumentos"].transform("sum")

    rows=[]
    for buyer,g in rel.groupby("orgao_cnpj", sort=False):
        sv=g["share_valor"].sort_values(ascending=False)
        sc=g["share_contagem"].sort_values(ascending=False)
        hv=float((sv**2).sum()); hc=float((sc**2).sum()); n=len(g)
        rows.append({
            "orgao_cnpj":buyer,
            "valor_total":float(g["valor_relacao"].sum()),
            "n_instrumentos":int(g["n_instrumentos"].sum()),
            "n_fornecedores":int(n),
            "portfolio_hhi":hv,
            "count_hhi":hc,
            "portfolio_cr1":float(sv.iloc[0]),
            "portfolio_cr4":float(sv.iloc[:4].sum()),
            "portfolio_neff":1.0/hv if hv>0 else np.nan,
        })
    buyers=pd.DataFrame(rows)
    buyers["portfolio_hhi_norm"] = hhi_norm(buyers["portfolio_hhi"], buyers["n_fornecedores"])
    buyers["count_hhi_norm"] = hhi_norm(buyers["count_hhi"], buyers["n_fornecedores"])
    buyers["hhi_gap_value_count"] = buyers["portfolio_hhi"] - buyers["count_hhi"]
    buyers["hhi_norm_gap_value_count"] = buyers["portfolio_hhi_norm"] - buyers["count_hhi_norm"]

    # Centralidade GLOBAL: usa toda a rede rel, antes de qualquer corte de elegibilidade.
    suppliers = (
        rel.groupby("fornecedor_id_limpo")
        .agg(degree=("orgao_cnpj","nunique"), strength=("valor_relacao","sum"))
        .reset_index()
    )
    nb=max(int(rel["orgao_cnpj"].nunique()),1)
    suppliers["reach"] = suppliers["degree"] / nb
    suppliers["system_share"] = suppliers["strength"] / suppliers["strength"].sum()
    suppliers["pct_degree_global"] = suppliers["degree"].rank(pct=True, method="average")
    suppliers["pct_strength_global"] = suppliers["strength"].rank(pct=True, method="average")

    z=rel.merge(
        suppliers[["fornecedor_id_limpo","pct_degree_global","pct_strength_global"]],
        on="fornecedor_id_limpo", how="left"
    )
    z["ed_piece"] = z["share_valor"] * z["pct_degree_global"]
    z["es_piece"] = z["share_valor"] * z["pct_strength_global"]
    exposure = (
        z.groupby("orgao_cnpj")
        .agg(exposicao_degree_global=("ed_piece","sum"), exposicao_strength_global=("es_piece","sum"))
        .reset_index()
    )
    buyers=buyers.merge(exposure,on="orgao_cnpj",how="left")
    return x, rel, buyers, suppliers


def spearman(a,b):
    z=pd.DataFrame({"a":a,"b":b}).replace([np.inf,-np.inf],np.nan).dropna()
    if len(z)<3:
        return {"rho":None,"p":None,"n":len(z)}
    rho,p=spearmanr(z["a"],z["b"])
    return {"rho":float(rho),"p":float(p),"n":int(len(z))}


def simulate_global(rel, suppliers, eligible_buyers):
    # Universo aleatório e ranking: TODOS os fornecedores da rede global.
    full=rel.copy()
    full["orgao_cnpj"] = full["orgao_cnpj"].astype(str)
    full["fornecedor_id_limpo"] = full["fornecedor_id_limpo"].astype(str)
    eligible_ids=sorted(set(eligible_buyers.astype(str)))
    slist=sorted(suppliers["fornecedor_id_limpo"].astype(str).unique())
    bi={v:i for i,v in enumerate(eligible_ids)}
    si={v:i for i,v in enumerate(slist)}
    A=np.zeros((len(eligible_ids),len(slist)),dtype=np.float32)
    r=full[full["orgao_cnpj"].isin(set(eligible_ids))]
    for row in r.itertuples(index=False):
        A[bi[str(row.orgao_cnpj)],si[str(row.fornecedor_id_limpo)]] += float(row.share_valor)

    sup=suppliers.copy()
    sup["fornecedor_id_limpo"] = sup["fornecedor_id_limpo"].astype(str)
    sup["idx"] = sup["fornecedor_id_limpo"].map(si)
    rng=np.random.default_rng(SEED)
    rows=[]
    for pct in [.01,.05,.10]:
        k=max(1,int(math.ceil(len(slist)*pct)))
        rnd_loss=[]; rnd_sev={.25:[],.50:[],.75:[]}
        for _ in range(DRAWS):
            idx=rng.choice(len(slist),size=k,replace=False)
            loss=A[:,idx].sum(axis=1)
            rnd_loss.append(float(loss.mean()))
            for t in rnd_sev:
                rnd_sev[t].append(float((loss>=t).mean()))
        for strategy in ["strength","degree"]:
            idx=sup.nlargest(k,strategy)["idx"].astype(int).to_numpy()
            loss=A[:,idx].sum(axis=1)
            for t in [.25,.50,.75]:
                rr=np.asarray(rnd_sev[t]); rl=np.asarray(rnd_loss)
                rows.append({
                    "estrategia":strategy,
                    "papel":"principal" if strategy=="strength" else "complementar",
                    "ranking_scope":"global",
                    "pct_fornecedores_removidos":pct,
                    "k_fornecedores_removidos":k,
                    "limiar_perda":t,
                    "share_severos_direcionado":float((loss>=t).mean()),
                    "share_severos_aleatorio_media":float(rr.mean()),
                    "share_severos_aleatorio_p025":float(np.quantile(rr,.025)),
                    "share_severos_aleatorio_p975":float(np.quantile(rr,.975)),
                    "excesso_vs_aleatorio":float((loss>=t).mean()-rr.mean()),
                    "perda_media_direcionada":float(loss.mean()),
                    "perda_media_aleatoria_media":float(rl.mean()),
                    "perda_media_aleatoria_p025":float(np.quantile(rl,.025)),
                    "perda_media_aleatoria_p975":float(np.quantile(rl,.975)),
                })
    return pd.DataFrame(rows)


def criterion_summary(buyers,nf,ni,label):
    g=buyers[(buyers["n_fornecedores"]>=nf)&(buyers["n_instrumentos"]>=ni)].copy()
    qh=float(g["portfolio_hhi"].quantile(.75)); qe=float(g["exposicao_strength_global"].quantile(.75))
    return {
        "criterio":label,"min_fornecedores":nf,"min_instrumentos":ni,"n":int(len(g)),
        "portfolio_hhi_mediana":float(g["portfolio_hhi"].median()),
        "portfolio_hhi_norm_mediana":float(g["portfolio_hhi_norm"].median()),
        "count_hhi_mediana":float(g["count_hhi"].median()),
        "count_hhi_norm_mediana":float(g["count_hhi_norm"].median()),
        "portfolio_neff_mediana":float(g["portfolio_neff"].median()),
        "portfolio_cr1_mediana":float(g["portfolio_cr1"].median()),
        "portfolio_cr4_mediana":float(g["portfolio_cr4"].median()),
        "portfolio_hhi_maior_count_hhi_pct":float((g["portfolio_hhi"]>g["count_hhi"]).mean()*100),
        "hidden_exposure_pct":float(((g["portfolio_hhi"]<qh)&(g["exposicao_strength_global"]>=qe)).mean()*100),
        "spearman_hhi_norm_exposure_strength_global":spearman(g["portfolio_hhi_norm"],g["exposicao_strength_global"]),
    }


def main():
    frames=[load_month(m) for m in [1,2,3]]
    acc=pd.concat(frames,ignore_index=True)
    dup=acc.duplicated("id_contrato",keep=False)
    if dup.any():
        raise RuntimeError(f"IDs duplicados entre meses: {acc.loc[dup,'id_contrato'].nunique()}")

    cohort,rel,buyers,suppliers=build_metrics(acc)
    eligible=buyers[(buyers["n_fornecedores"]>=3)&(buyers["n_instrumentos"]>=5)].copy()
    sims=simulate_global(rel,suppliers,eligible["orgao_cnpj"])

    rel.to_csv(OUT/"relacoes_acumuladas_assinados_2025.csv.gz",index=False,compression="gzip")
    buyers.to_csv(OUT/"metricas_compradores_validada.csv",index=False,encoding="utf-8-sig")
    suppliers.to_csv(OUT/"metricas_fornecedores_rede_global.csv",index=False,encoding="utf-8-sig")
    eligible.to_csv(OUT/"compradores_elegiveis_3_5.csv",index=False,encoding="utf-8-sig")
    sims.to_csv(OUT/"simulacoes_ranking_global.csv",index=False,encoding="utf-8-sig")

    sens=[]
    for nf,ni in CRITERIA:
        sens.append(criterion_summary(buyers,nf,ni,f"{nf}/{ni}"))
    pd.DataFrame(sens).to_csv(OUT/"sensibilidade_elegibilidade.csv",index=False,encoding="utf-8-sig")

    # Estabilidade acumulada 1 -> 2 -> 3 meses sob a mesma definição de HHI.
    stab=[]
    for m in [1,2,3]:
        sub=acc[acc["mes_publicacao"]<=m].copy()
        _,_,bb,_=build_metrics(sub)
        ee=bb[(bb["n_fornecedores"]>=3)&(bb["n_instrumentos"]>=5)].copy()
        stab.append({
            "mes_final":m,"n_elegiveis":len(ee),
            "hhi_mediana":ee["portfolio_hhi"].median(),
            "hhi_norm_mediana":ee["portfolio_hhi_norm"].median(),
            "count_hhi_mediana":ee["count_hhi"].median(),
            "count_hhi_norm_mediana":ee["count_hhi_norm"].median(),
            "neff_mediana":ee["portfolio_neff"].median(),
            "cr1_mediana":ee["portfolio_cr1"].median(),
            "cr4_mediana":ee["portfolio_cr4"].median(),
        })
    pd.DataFrame(stab).to_csv(OUT/"estabilidade_jan_fev_mar.csv",index=False,encoding="utf-8-sig")

    qh=float(eligible["portfolio_hhi"].quantile(.75)); qe=float(eligible["exposicao_strength_global"].quantile(.75))
    strength50=sims[(sims["estrategia"]=="strength")&(sims["limiar_perda"]==.5)].to_dict(orient="records")
    degree50=sims[(sims["estrategia"]=="degree")&(sims["limiar_perda"]==.5)].to_dict(orient="records")
    summary={
        "status":"reanálise validada; substitui as simulações restritas da primeira execução de março para fins interpretativos",
        "advertencia":"Coorte de publicações até março; não interpretar como resultado anual de 2025.",
        "registros_pj_acumulados":int(len(acc)),
        "instrumentos_unicos":int(acc["id_contrato"].nunique()),
        "assinados_2025":int(acc["ano_assinatura"].eq(2025).sum()),
        "compradores_metricas":int(len(buyers)),
        "compradores_elegiveis_3_5":int(len(eligible)),
        "fornecedores_rede_global":int(len(suppliers)),
        "portfolio_hhi_mediana":float(eligible["portfolio_hhi"].median()),
        "portfolio_hhi_norm_mediana":float(eligible["portfolio_hhi_norm"].median()),
        "count_hhi_mediana":float(eligible["count_hhi"].median()),
        "count_hhi_norm_mediana":float(eligible["count_hhi_norm"].median()),
        "portfolio_neff_mediana":float(eligible["portfolio_neff"].median()),
        "portfolio_cr1_mediana":float(eligible["portfolio_cr1"].median()),
        "portfolio_cr4_mediana":float(eligible["portfolio_cr4"].median()),
        "spearman_hhi_count":spearman(eligible["portfolio_hhi"],eligible["count_hhi"]),
        "spearman_hhi_norm_exposure_strength_global":spearman(eligible["portfolio_hhi_norm"],eligible["exposicao_strength_global"]),
        "q75_hhi":qh,"q75_exposicao_strength_global":qe,
        "hhi_baixo_exposicao_alta_n":int(((eligible["portfolio_hhi"]<qh)&(eligible["exposicao_strength_global"]>=qe)).sum()),
        "hhi_baixo_exposicao_alta_pct":float(((eligible["portfolio_hhi"]<qh)&(eligible["exposicao_strength_global"]>=qe)).mean()*100),
        "hhi_alto_exposicao_alta_n":int(((eligible["portfolio_hhi"]>=qh)&(eligible["exposicao_strength_global"]>=qe)).sum()),
        "portfolio_hhi_maior_count_hhi_n":int((eligible["portfolio_hhi"]>eligible["count_hhi"]).sum()),
        "portfolio_hhi_maior_count_hhi_pct":float((eligible["portfolio_hhi"]>eligible["count_hhi"]).mean()*100),
        "lag_negativo_n":int((acc["lag_publicacao_dias"]<0).sum()),
        "simulacao":{"ranking_principal":"strength_global","degree":"complementar","random_draws":DRAWS,"seed":SEED,"strength_limiar_50pct":strength50,"degree_limiar_50pct":degree50},
        "sensibilidade_elegibilidade":sens,
        "estabilidade_mensal":stab,
    }
    (OUT/"resumo_validado.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
