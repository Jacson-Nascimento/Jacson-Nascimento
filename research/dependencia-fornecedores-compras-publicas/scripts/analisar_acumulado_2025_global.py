#!/usr/bin/env python3
"""Análise acumulada mensal de 2025 com especificação metodológica vigente.

Uso:
    python scripts/analisar_acumulado_2025_global.py --month 4

Requisitos:
- arquivos mensais consolidados `pncp_2025-MM_publicacoes_municipal_pj.csv.gz`
  disponíveis de janeiro até o mês solicitado;
- não acessa APIs externas;
- comprador = CNPJ institucional;
- fornecedores PJ na base pública;
- métricas econômicas sobre instrumentos assinados em 2025 e valorInicial > 0.

Especificação:
- HHI bruto + normalizado;
- CountHHI bruto + normalizado;
- centralidade/exposição na rede GLOBAL;
- Strength global = choque principal;
- Degree global = complementar;
- 1.000 remoções aleatórias por cenário;
- sensibilidade 3/5, 5/10, 5/20 e 10/20.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"processed"/"pncp_mensal"
RES=ROOT/"results"
SEED=20260818
DRAWS=1000
CRITERIA=[(3,5),(5,10),(5,20),(10,20)]


def parse_mixed(s):
    try:return pd.to_datetime(s,errors="coerce",format="mixed")
    except TypeError:return pd.to_datetime(s,errors="coerce")


def load_month(m):
    p=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
    if not p.exists():raise FileNotFoundError(p)
    d=pd.read_csv(p,dtype={"id_contrato":"string","orgao_cnpj":"string","fornecedor_id_limpo":"string","municipio_ibge":"string"},low_memory=False)
    d["ano_assinatura"]=pd.to_numeric(d["ano_assinatura"],errors="coerce")
    d["valorInicial"]=pd.to_numeric(d["valorInicial"],errors="coerce")
    d["lag_publicacao_dias"]=pd.to_numeric(d["lag_publicacao_dias"],errors="coerce")
    d["data_publicacao"]=parse_mixed(d["data_publicacao"])
    d["mes_publicacao"]=m
    return d


def hhi_norm(hhi,n):
    h=pd.to_numeric(hhi,errors="coerce"); nn=pd.to_numeric(n,errors="coerce"); floor=1/nn
    return ((h-floor)/(1-floor)).where(nn>1).clip(0,1)


def spearman(a,b):
    z=pd.DataFrame({"a":a,"b":b}).replace([np.inf,-np.inf],np.nan).dropna()
    if len(z)<3:return {"rho":None,"p":None,"n":len(z)}
    rho,p=spearmanr(z.a,z.b); return {"rho":float(rho),"p":float(p),"n":int(len(z))}


def build_metrics(acc):
    x=acc[acc.ano_assinatura.eq(2025)&acc.valorInicial.gt(0)].copy()
    rel=x.groupby(["orgao_cnpj","fornecedor_id_limpo"],dropna=False).agg(valor_relacao=("valorInicial","sum"),n_instrumentos=("id_contrato","nunique")).reset_index()
    rel["share_valor"]=rel.valor_relacao/rel.groupby("orgao_cnpj").valor_relacao.transform("sum")
    rel["share_contagem"]=rel.n_instrumentos/rel.groupby("orgao_cnpj").n_instrumentos.transform("sum")
    rows=[]
    for buyer,g in rel.groupby("orgao_cnpj",sort=False):
        sv=g.share_valor.sort_values(ascending=False); sc=g.share_contagem.sort_values(ascending=False)
        hv=float((sv**2).sum()); hc=float((sc**2).sum()); n=len(g)
        rows.append({"orgao_cnpj":buyer,"valor_total":float(g.valor_relacao.sum()),"n_instrumentos":int(g.n_instrumentos.sum()),"n_fornecedores":n,"portfolio_hhi":hv,"count_hhi":hc,"portfolio_cr1":float(sv.iloc[0]),"portfolio_cr4":float(sv.iloc[:4].sum()),"portfolio_neff":1/hv if hv>0 else np.nan})
    buyers=pd.DataFrame(rows)
    buyers["portfolio_hhi_norm"]=hhi_norm(buyers.portfolio_hhi,buyers.n_fornecedores)
    buyers["count_hhi_norm"]=hhi_norm(buyers.count_hhi,buyers.n_fornecedores)
    buyers["hhi_gap_value_count"]=buyers.portfolio_hhi-buyers.count_hhi
    buyers["hhi_norm_gap_value_count"]=buyers.portfolio_hhi_norm-buyers.count_hhi_norm

    suppliers=rel.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"),strength=("valor_relacao","sum")).reset_index()
    nb=max(int(rel.orgao_cnpj.nunique()),1)
    suppliers["reach"]=suppliers.degree/nb
    suppliers["system_share"]=suppliers.strength/suppliers.strength.sum()
    suppliers["pct_degree_global"]=suppliers.degree.rank(pct=True,method="average")
    suppliers["pct_strength_global"]=suppliers.strength.rank(pct=True,method="average")
    z=rel.merge(suppliers[["fornecedor_id_limpo","pct_degree_global","pct_strength_global"]],on="fornecedor_id_limpo",how="left")
    z["ed_piece"]=z.share_valor*z.pct_degree_global; z["es_piece"]=z.share_valor*z.pct_strength_global
    exp=z.groupby("orgao_cnpj").agg(exposicao_degree_global=("ed_piece","sum"),exposicao_strength_global=("es_piece","sum")).reset_index()
    buyers=buyers.merge(exp,on="orgao_cnpj",how="left")
    return x,rel,buyers,suppliers


def simulate_global(rel,suppliers,eligible_buyers):
    full=rel.copy(); full["orgao_cnpj"]=full.orgao_cnpj.astype(str); full["fornecedor_id_limpo"]=full.fornecedor_id_limpo.astype(str)
    bids=sorted(set(eligible_buyers.astype(str))); slist=sorted(suppliers.fornecedor_id_limpo.astype(str).unique())
    bi={v:i for i,v in enumerate(bids)}; si={v:i for i,v in enumerate(slist)}
    A=np.zeros((len(bids),len(slist)),dtype=np.float32)
    for row in full[full.orgao_cnpj.isin(set(bids))].itertuples(index=False):A[bi[str(row.orgao_cnpj)],si[str(row.fornecedor_id_limpo)]]+=float(row.share_valor)
    sup=suppliers.copy(); sup["fornecedor_id_limpo"]=sup.fornecedor_id_limpo.astype(str); sup["idx"]=sup.fornecedor_id_limpo.map(si)
    rng=np.random.default_rng(SEED); rows=[]
    for pct in [.01,.05,.10]:
        k=max(1,int(math.ceil(len(slist)*pct))); rnd_loss=[]; rnd={.25:[],.5:[],.75:[]}
        for _ in range(DRAWS):
            idx=rng.choice(len(slist),size=k,replace=False); loss=A[:,idx].sum(axis=1); rnd_loss.append(float(loss.mean()))
            for t in rnd:rnd[t].append(float((loss>=t).mean()))
        for strategy in ["strength","degree"]:
            idx=sup.nlargest(k,strategy).idx.astype(int).to_numpy(); loss=A[:,idx].sum(axis=1)
            for t in [.25,.5,.75]:
                rr=np.asarray(rnd[t]); rl=np.asarray(rnd_loss)
                rows.append({"estrategia":strategy,"papel":"principal" if strategy=="strength" else "complementar","ranking_scope":"global","pct_fornecedores_removidos":pct,"k_fornecedores_removidos":k,"limiar_perda":t,"share_severos_direcionado":float((loss>=t).mean()),"share_severos_aleatorio_media":float(rr.mean()),"share_severos_aleatorio_p025":float(np.quantile(rr,.025)),"share_severos_aleatorio_p975":float(np.quantile(rr,.975)),"excesso_vs_aleatorio":float((loss>=t).mean()-rr.mean()),"perda_media_direcionada":float(loss.mean()),"perda_media_aleatoria_media":float(rl.mean()),"perda_media_aleatoria_p025":float(np.quantile(rl,.025)),"perda_media_aleatoria_p975":float(np.quantile(rl,.975))})
    return pd.DataFrame(rows)


def criterion_summary(buyers,nf,ni):
    g=buyers[(buyers.n_fornecedores>=nf)&(buyers.n_instrumentos>=ni)].copy(); qh=float(g.portfolio_hhi.quantile(.75)); qe=float(g.exposicao_strength_global.quantile(.75))
    return {"criterio":f"{nf}/{ni}","n":int(len(g)),"portfolio_hhi_mediana":float(g.portfolio_hhi.median()),"portfolio_hhi_norm_mediana":float(g.portfolio_hhi_norm.median()),"count_hhi_mediana":float(g.count_hhi.median()),"count_hhi_norm_mediana":float(g.count_hhi_norm.median()),"portfolio_neff_mediana":float(g.portfolio_neff.median()),"portfolio_cr1_mediana":float(g.portfolio_cr1.median()),"portfolio_cr4_mediana":float(g.portfolio_cr4.median()),"portfolio_hhi_maior_count_hhi_pct":float((g.portfolio_hhi>g.count_hhi).mean()*100),"hidden_exposure_pct":float(((g.portfolio_hhi<qh)&(g.exposicao_strength_global>=qe)).mean()*100),"spearman_hhi_norm_exposure_strength_global":spearman(g.portfolio_hhi_norm,g.exposicao_strength_global)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--month",type=int,required=True,choices=range(1,13)); args=ap.parse_args(); month=args.month
    frames=[load_month(m) for m in range(1,month+1)]; acc=pd.concat(frames,ignore_index=True)
    dup=acc.duplicated("id_contrato",keep=False)
    if dup.any():raise RuntimeError(f"IDs duplicados entre meses: {acc.loc[dup,'id_contrato'].nunique()}")
    cohort,rel,buyers,suppliers=build_metrics(acc); eligible=buyers[(buyers.n_fornecedores>=3)&(buyers.n_instrumentos>=5)].copy(); sims=simulate_global(rel,suppliers,eligible.orgao_cnpj)
    OUT=RES/f"carteira_acumulada_2025_{month:02d}_global"; OUT.mkdir(parents=True,exist_ok=True)
    rel.to_csv(OUT/"relacoes.csv.gz",index=False,compression="gzip"); buyers.to_csv(OUT/"metricas_compradores.csv",index=False,encoding="utf-8-sig"); suppliers.to_csv(OUT/"metricas_fornecedores_global.csv",index=False,encoding="utf-8-sig"); eligible.to_csv(OUT/"compradores_elegiveis_3_5.csv",index=False,encoding="utf-8-sig"); sims.to_csv(OUT/"simulacoes_global.csv",index=False,encoding="utf-8-sig")
    sens=[criterion_summary(buyers,nf,ni) for nf,ni in CRITERIA]; pd.DataFrame(sens).to_csv(OUT/"sensibilidade_elegibilidade.csv",index=False,encoding="utf-8-sig")
    stab=[]
    for m in range(1,month+1):
        sub=acc[acc.mes_publicacao<=m]; _,_,bb,_=build_metrics(sub); ee=bb[(bb.n_fornecedores>=3)&(bb.n_instrumentos>=5)]
        stab.append({"mes_final":m,"n_elegiveis":len(ee),"hhi_mediana":ee.portfolio_hhi.median(),"hhi_norm_mediana":ee.portfolio_hhi_norm.median(),"count_hhi_mediana":ee.count_hhi.median(),"count_hhi_norm_mediana":ee.count_hhi_norm.median(),"neff_mediana":ee.portfolio_neff.median(),"cr1_mediana":ee.portfolio_cr1.median(),"cr4_mediana":ee.portfolio_cr4.median()})
    pd.DataFrame(stab).to_csv(OUT/"estabilidade_mensal.csv",index=False,encoding="utf-8-sig")
    qh=float(eligible.portfolio_hhi.quantile(.75)); qe=float(eligible.exposicao_strength_global.quantile(.75))
    summary={"mes_final":month,"advertencia":"Coorte de publicações acumuladas; não representa o ano completo até a coleta e janela tardia serem concluídas.","registros_pj_acumulados":int(len(acc)),"instrumentos_unicos":int(acc.id_contrato.nunique()),"assinados_2025":int(acc.ano_assinatura.eq(2025).sum()),"compradores_metricas":int(len(buyers)),"compradores_elegiveis_3_5":int(len(eligible)),"fornecedores_rede_global":int(len(suppliers)),"portfolio_hhi_mediana":float(eligible.portfolio_hhi.median()),"portfolio_hhi_norm_mediana":float(eligible.portfolio_hhi_norm.median()),"count_hhi_mediana":float(eligible.count_hhi.median()),"count_hhi_norm_mediana":float(eligible.count_hhi_norm.median()),"portfolio_neff_mediana":float(eligible.portfolio_neff.median()),"portfolio_cr1_mediana":float(eligible.portfolio_cr1.median()),"portfolio_cr4_mediana":float(eligible.portfolio_cr4.median()),"spearman_hhi_count":spearman(eligible.portfolio_hhi,eligible.count_hhi),"spearman_hhi_norm_exposure_strength_global":spearman(eligible.portfolio_hhi_norm,eligible.exposicao_strength_global),"hhi_baixo_exposicao_alta_n":int(((eligible.portfolio_hhi<qh)&(eligible.exposicao_strength_global>=qe)).sum()),"hhi_baixo_exposicao_alta_pct":float(((eligible.portfolio_hhi<qh)&(eligible.exposicao_strength_global>=qe)).mean()*100),"portfolio_hhi_maior_count_hhi_pct":float((eligible.portfolio_hhi>eligible.count_hhi).mean()*100),"lag_negativo_n":int((acc.lag_publicacao_dias<0).sum()),"simulacao":{"ranking_principal":"strength_global","degree":"complementar","random_draws":DRAWS,"seed":SEED,"strength_limiar_50pct":sims[(sims.estrategia=="strength")&(sims.limiar_perda==.5)].to_dict(orient="records")},"sensibilidade_elegibilidade":sens,"estabilidade_mensal":stab}
    (OUT/"resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
