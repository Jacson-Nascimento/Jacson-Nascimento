#!/usr/bin/env python3
"""Consolida um mês do PNCP e recalcula o acumulado de 2025.

Uso:
    python scripts/consolidar_analisar_acumulado_2025.py --month 3

Premissas:
- partições mensais previamente coletadas com coletar_pncp_periodo.py;
- base pública identificada restrita a fornecedores PJ;
- métricas econômicas: instrumentos assinados em 2025 e valorInicial > 0;
- comprador principal: CNPJ institucional do órgão.

O acumulado de meses de publicação é diagnóstico até que o ano de 2025 esteja
completo e seja aplicada uma janela posterior para capturar publicações tardias.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from calendar import monthrange
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pncp_mensal"
RES = ROOT / "results"
SEED = 20260818
RANDOM_DRAWS = 1000


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_mixed(s: pd.Series) -> pd.Series:
    try:
        return pd.to_datetime(s, errors="coerce", format="mixed")
    except TypeError:
        return pd.to_datetime(s, errors="coerce")


def entropy_norm(shares: pd.Series) -> float:
    x = pd.to_numeric(shares, errors="coerce").dropna()
    x = x[x > 0]
    if len(x) <= 1:
        return 0.0 if len(x) == 1 else float("nan")
    return float(-(x * np.log(x)).sum() / math.log(len(x)))


def load_public(path: Path) -> pd.DataFrame:
    d = pd.read_csv(
        path,
        dtype={
            "id_contrato": "string",
            "id_compra": "string",
            "orgao_cnpj": "string",
            "orgao_compra_cnpj": "string",
            "municipio_ibge": "string",
            "fornecedor_id_limpo": "string",
        },
        low_memory=False,
    )
    d["data_publicacao"] = parse_mixed(d["data_publicacao"])
    d["data_assinatura"] = parse_mixed(d["data_assinatura"])
    d["valorInicial"] = pd.to_numeric(d["valorInicial"], errors="coerce")
    d["ano_assinatura"] = pd.to_numeric(d["ano_assinatura"], errors="coerce").astype("Int64")
    d["lag_publicacao_dias"] = pd.to_numeric(d["lag_publicacao_dias"], errors="coerce")
    return d


def consolidate_month(month: int):
    ym = f"2025-{month:02d}"
    out_month = RES / f"carteira_2025_{month:02d}_diagnostico"
    out_month.mkdir(parents=True, exist_ok=True)
    part_paths = sorted(DATA.glob(f"pncp_{ym}-d*_municipal_pj.csv.gz"))
    if not part_paths:
        raise FileNotFoundError(f"Nenhuma partição encontrada para {ym}")

    frames, manifests, summaries = [], [], []
    for p in part_paths:
        label = p.name.removeprefix("pncp_").removesuffix("_municipal_pj.csv.gz")
        d = load_public(p)
        d["particao"] = label
        frames.append(d)
        manifests.append({"particao": label, "linhas_pj": int(len(d)), "sha256": sha256(p)})
        sp = RES / "pncp_mensal" / f"{label}_resumo.json"
        if sp.exists():
            summaries.append(json.loads(sp.read_text(encoding="utf-8")))

    x = pd.concat(frames, ignore_index=True)
    dup = x.duplicated("id_contrato", keep=False)
    if dup.any():
        x.loc[dup, ["id_contrato", "particao"]].to_csv(out_month/"duplicidades_particoes.csv", index=False, encoding="utf-8-sig")
        raise RuntimeError(f"Duplicidades no mês {ym}: {x.loc[dup,'id_contrato'].nunique()}")
    if x["data_publicacao"].isna().any():
        raise RuntimeError(f"Datas de publicação não parseáveis em {ym}: {int(x['data_publicacao'].isna().sum())}")

    start = pd.Timestamp(2025, month, 1)
    end = pd.Timestamp(2026, 1, 1) if month == 12 else pd.Timestamp(2025, month + 1, 1)
    outside = ~((x["data_publicacao"] >= start) & (x["data_publicacao"] < end))
    if outside.any():
        x.loc[outside, ["id_contrato", "data_publicacao", "particao"]].to_csv(out_month/"publicacoes_fora_mes.csv", index=False, encoding="utf-8-sig")
        raise RuntimeError(f"Publicações fora de {ym}: {int(outside.sum())}")

    out_path = DATA / f"pncp_{ym}_publicacoes_municipal_pj.csv.gz"
    x.drop(columns=["particao"]).to_csv(out_path, index=False, compression="gzip", encoding="utf-8")
    pd.DataFrame(manifests).to_csv(out_month/"manifesto_particoes.csv", index=False, encoding="utf-8-sig")

    summary = {
        "mes": ym,
        "particoes_n": len(part_paths),
        "registros_pj": int(len(x)),
        "instrumentos_unicos": int(x["id_contrato"].nunique()),
        "duplicidades": int(x.duplicated("id_contrato").sum()),
        "compradores_unicos": int(x["orgao_cnpj"].nunique()),
        "fornecedores_pj_unicos": int(x["fornecedor_id_limpo"].nunique()),
        "municipios_unicos": int(x["municipio_ibge"].nunique()),
        "assinados_2025": int(x["ano_assinatura"].eq(2025).sum()),
        "assinados_antes_2025": int(x["ano_assinatura"].lt(2025).sum()),
        "lag_mediana": float(x["lag_publicacao_dias"].median()),
        "lag_p90": float(x["lag_publicacao_dias"].quantile(.90)),
        "lag_p95": float(x["lag_publicacao_dias"].quantile(.95)),
        "lag_negativo_n": int((x["lag_publicacao_dias"] < 0).sum()),
        "janela_publicacao": {"min": x["data_publicacao"].min().isoformat(), "max": x["data_publicacao"].max().isoformat()},
        "sha256_base_pj": sha256(out_path),
    }
    if summaries:
        summary.update({
            "registros_brutos_particoes_soma": int(sum(s.get("registros_brutos",0) for s in summaries)),
            "registros_municipais_validos_todos_tipos_soma": int(sum(s.get("registros_municipais_validos",0) for s in summaries)),
            "registros_pf_soma": int(sum(s.get("registros_pf",0) for s in summaries)),
            "registros_pe_soma": int(sum(s.get("registros_pe",0) for s in summaries)),
        })
    (out_month/"resumo_mes.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return x.drop(columns=["particao"]), out_path, summary


def calculate_metrics(df: pd.DataFrame):
    x = df[df["ano_assinatura"].eq(2025) & df["valorInicial"].gt(0)].copy()
    rel = x.groupby(["orgao_cnpj", "fornecedor_id_limpo"], dropna=False).agg(
        valor_relacao=("valorInicial","sum"), n_instrumentos=("id_contrato","nunique")
    ).reset_index()
    rel["share_valor"] = rel["valor_relacao"] / rel.groupby("orgao_cnpj")["valor_relacao"].transform("sum")
    rel["share_contagem"] = rel["n_instrumentos"] / rel.groupby("orgao_cnpj")["n_instrumentos"].transform("sum")

    rows=[]
    for buyer,g in rel.groupby("orgao_cnpj", sort=False):
        sv=g["share_valor"].sort_values(ascending=False); sc=g["share_contagem"].sort_values(ascending=False)
        hv=float((sv**2).sum()); hc=float((sc**2).sum())
        rows.append({
            "orgao_cnpj":buyer,"valor_total":float(g["valor_relacao"].sum()),
            "n_instrumentos":int(g["n_instrumentos"].sum()),"n_fornecedores":int(g["fornecedor_id_limpo"].nunique()),
            "portfolio_hhi":hv,"portfolio_cr1":float(sv.iloc[0]),"portfolio_cr4":float(sv.iloc[:4].sum()),
            "portfolio_neff":1/hv if hv>0 else np.nan,"portfolio_entropy_norm":entropy_norm(sv),
            "count_hhi":hc,"count_neff":1/hc if hc>0 else np.nan,"hhi_gap_value_minus_count":hv-hc,
        })
    buyers=pd.DataFrame(rows)

    suppliers=rel.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"),strength=("valor_relacao","sum")).reset_index()
    nb=max(int(rel["orgao_cnpj"].nunique()),1)
    suppliers["reach"]=suppliers["degree"]/nb
    suppliers["system_share"]=suppliers["strength"]/suppliers["strength"].sum()
    suppliers["pct_degree"]=suppliers["degree"].rank(pct=True,method="average")
    suppliers["pct_strength"]=suppliers["strength"].rank(pct=True,method="average")
    z=rel.merge(suppliers[["fornecedor_id_limpo","pct_degree","pct_strength"]],on="fornecedor_id_limpo",how="left")
    z["ed"]=z["share_valor"]*z["pct_degree"]; z["es"]=z["share_valor"]*z["pct_strength"]
    exp=z.groupby("orgao_cnpj").agg(exposicao_degree=("ed","sum"),exposicao_strength=("es","sum")).reset_index()
    buyers=buyers.merge(exp,on="orgao_cnpj",how="left")
    return x,rel,buyers,suppliers


def corr(a,b):
    rho,p=spearmanr(a,b,nan_policy="omit")
    return {"rho":None if pd.isna(rho) else float(rho),"p":None if pd.isna(p) else float(p)}


def simulate(rel: pd.DataFrame, eligible_buyers: pd.Series):
    eligible_set=set(eligible_buyers.astype(str)); r=rel[rel["orgao_cnpj"].astype(str).isin(eligible_set)].copy()
    r["orgao_cnpj"]=r["orgao_cnpj"].astype(str); r["fornecedor_id_limpo"]=r["fornecedor_id_limpo"].astype(str)
    blist=sorted(r["orgao_cnpj"].unique()); slist=sorted(r["fornecedor_id_limpo"].unique())
    bi={v:i for i,v in enumerate(blist)}; si={v:i for i,v in enumerate(slist)}
    A=np.zeros((len(blist),len(slist)),dtype=np.float32)
    for row in r.itertuples(index=False): A[bi[row.orgao_cnpj],si[row.fornecedor_id_limpo]] += float(row.share_valor)
    sup=r.groupby("fornecedor_id_limpo").agg(degree=("orgao_cnpj","nunique"),strength=("valor_relacao","sum")).reset_index()
    sup["idx"]=sup["fornecedor_id_limpo"].map(si)
    rng=np.random.default_rng(SEED); rows=[]; thresholds=[.25,.5,.75]
    for pct in [.01,.05,.10]:
        k=max(1,int(math.ceil(len(slist)*pct))); rnd_sev={t:[] for t in thresholds}; rnd_loss=[]
        for _ in range(RANDOM_DRAWS):
            idx=rng.choice(len(slist),size=k,replace=False); loss=A[:,idx].sum(axis=1)
            rnd_loss.append(float(loss.mean()))
            for t in thresholds: rnd_sev[t].append(float((loss>=t).mean()))
        for strategy in ["degree","strength"]:
            target=sup.nlargest(k,strategy)["idx"].astype(int).to_numpy(); loss=A[:,target].sum(axis=1)
            for t in thresholds:
                rr=np.asarray(rnd_sev[t]); rl=np.asarray(rnd_loss)
                rows.append({"estrategia":strategy,"pct_fornecedores_removidos":pct,"k":k,"limiar_perda":t,
                    "share_severos_direcionado":float((loss>=t).mean()),"share_severos_aleatorio_media":float(rr.mean()),
                    "share_severos_aleatorio_p025":float(np.quantile(rr,.025)),"share_severos_aleatorio_p975":float(np.quantile(rr,.975)),
                    "perda_media_direcionada":float(loss.mean()),"perda_media_aleatoria_media":float(rl.mean()),
                    "perda_media_aleatoria_p025":float(np.quantile(rl,.025)),"perda_media_aleatoria_p975":float(np.quantile(rl,.975))})
    return pd.DataFrame(rows)


def load_accumulated(month: int):
    frames=[]; manifests=[]
    for m in range(1,month+1):
        p=DATA/f"pncp_2025-{m:02d}_publicacoes_municipal_pj.csv.gz"
        if not p.exists(): raise FileNotFoundError(p)
        d=load_public(p); d["mes_publicacao"]=m; frames.append(d)
        manifests.append({"mes":m,"linhas":len(d),"sha256":sha256(p)})
    x=pd.concat(frames,ignore_index=True)
    dup=x.duplicated("id_contrato",keep=False)
    if dup.any(): raise RuntimeError(f"IDs repetidos entre meses: {x.loc[dup,'id_contrato'].nunique()}")
    return x,pd.DataFrame(manifests)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--month",type=int,required=True,choices=range(1,13)); args=ap.parse_args(); month=args.month
    _, month_path, month_summary=consolidate_month(month)
    acc, manifest=load_accumulated(month)
    out=RES/f"carteira_acumulada_2025_{month:02d}_diagnostico"; out.mkdir(parents=True,exist_ok=True)
    manifest.to_csv(out/"manifesto_meses.csv",index=False,encoding="utf-8-sig")
    cohort,rel,buyers,suppliers=calculate_metrics(acc)
    eligible=buyers[(buyers["n_fornecedores"]>=3)&(buyers["n_instrumentos"]>=5)].copy()
    sims=simulate(rel,eligible["orgao_cnpj"])
    rel.to_csv(out/"relacoes_acumuladas_assinados_2025.csv.gz",index=False,compression="gzip")
    buyers.to_csv(out/"metricas_compradores.csv",index=False,encoding="utf-8-sig")
    suppliers.to_csv(out/"metricas_fornecedores.csv",index=False,encoding="utf-8-sig")
    eligible.to_csv(out/"compradores_elegiveis.csv",index=False,encoding="utf-8-sig")
    sims.to_csv(out/"simulacoes_remocao.csv",index=False,encoding="utf-8-sig")

    # Estabilidade cumulativa por mês.
    stab=[]
    for m in range(1,month+1):
        sub=acc[acc["mes_publicacao"]<=m].copy(); _,_,bb,_=calculate_metrics(sub)
        ee=bb[(bb["n_fornecedores"]>=3)&(bb["n_instrumentos"]>=5)]
        stab.append({"mes_final":m,"n_elegiveis":len(ee),"hhi_mediana":ee["portfolio_hhi"].median(),
            "count_hhi_mediana":ee["count_hhi"].median(),"neff_mediana":ee["portfolio_neff"].median(),
            "cr1_mediana":ee["portfolio_cr1"].median(),"cr4_mediana":ee["portfolio_cr4"].median()})
    pd.DataFrame(stab).to_csv(out/"estabilidade_cumulativa.csv",index=False,encoding="utf-8-sig")

    qh=float(eligible["portfolio_hhi"].quantile(.75)); qe=float(eligible["exposicao_strength"].quantile(.75))
    summary={
        "mes_final_publicacao":f"2025-{month:02d}","advertencia":"Coorte parcial de publicação; não interpretar como resultado anual.",
        "registros_pj_acumulados":int(len(acc)),"instrumentos_unicos":int(acc["id_contrato"].nunique()),"duplicidades":0,
        "assinados_2025":int(acc["ano_assinatura"].eq(2025).sum()),"compradores_metricas":int(len(buyers)),
        "compradores_elegiveis":int(len(eligible)),"fornecedores_rede_total":int(suppliers["fornecedor_id_limpo"].nunique()),
        "portfolio_hhi_mediana":float(eligible["portfolio_hhi"].median()),"count_hhi_mediana":float(eligible["count_hhi"].median()),
        "portfolio_neff_mediana":float(eligible["portfolio_neff"].median()),"portfolio_cr1_mediana":float(eligible["portfolio_cr1"].median()),
        "portfolio_cr4_mediana":float(eligible["portfolio_cr4"].median()),"spearman_portfolio_count":corr(eligible["portfolio_hhi"],eligible["count_hhi"]),
        "spearman_portfolio_exposicao_strength":corr(eligible["portfolio_hhi"],eligible["exposicao_strength"]),
        "q75_portfolio_hhi":qh,"q75_exposicao_strength":qe,
        "hhi_baixo_exposicao_alta_n":int(((eligible["portfolio_hhi"]<qh)&(eligible["exposicao_strength"]>=qe)).sum()),
        "hhi_alto_exposicao_alta_n":int(((eligible["portfolio_hhi"]>=qh)&(eligible["exposicao_strength"]>=qe)).sum()),
        "portfolio_hhi_maior_count_hhi_n":int((eligible["portfolio_hhi"]>eligible["count_hhi"]).sum()),
        "portfolio_hhi_maior_count_hhi_pct":float((eligible["portfolio_hhi"]>eligible["count_hhi"]).mean()*100),
        "lag_negativo_n_acumulado":int((acc["lag_publicacao_dias"]<0).sum()),"random_draws_por_cenario":RANDOM_DRAWS,"seed":SEED,
        "mes_consolidado":month_summary,"sha256_mes_consolidado":sha256(month_path),
    }
    (out/"resumo_acumulado.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2)); print("\nSimulações limiar 50%:\n",sims[sims["limiar_perda"].eq(.5)].to_string(index=False))

if __name__=="__main__": main()
