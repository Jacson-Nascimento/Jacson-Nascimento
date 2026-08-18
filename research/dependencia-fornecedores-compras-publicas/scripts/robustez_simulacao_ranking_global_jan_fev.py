#!/usr/bin/env python3
"""Robustez da simulação: ranking de fornecedores global vs rede elegível.

Cenário 'eligible': reproduz a lógica diagnóstica anterior — universo e ranking
são definidos apenas nas relações dos compradores elegíveis.

Cenário 'global': degree/strength e universo aleatório são definidos em toda a
rede observada de contratos assinados em 2025 publicados até fevereiro; o
impacto continua sendo medido nos compradores elegíveis.

Isso testa se a evidência de vulnerabilidade direcionada depende da seleção dos
compradores usada para classificar os fornecedores.
"""
from pathlib import Path
import json, math
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"results"
INP=RES/"carteira_jan_fev_2025_diagnostico"
OUT=RES/"robustez_ranking_global_jan_fev_2025"
OUT.mkdir(parents=True,exist_ok=True)
SEED=20260818
DRAWS=1000


def build_matrix(rel, eligible_ids, universe_suppliers):
    r=rel[rel["orgao_cnpj"].astype(str).isin(eligible_ids)].copy()
    r["orgao_cnpj"]=r["orgao_cnpj"].astype(str)
    r["fornecedor_id_limpo"]=r["fornecedor_id_limpo"].astype(str)
    blist=sorted(eligible_ids)
    slist=sorted(universe_suppliers)
    bi={v:i for i,v in enumerate(blist)}; si={v:i for i,v in enumerate(slist)}
    A=np.zeros((len(blist),len(slist)),dtype=np.float32)
    for row in r.itertuples(index=False):
        sid=str(row.fornecedor_id_limpo)
        if sid in si:
            A[bi[str(row.orgao_cnpj)],si[sid]] += float(row.share_valor)
    return A, blist, slist, si


def run_scope(rel, eligible, scope):
    eligible_ids=set(eligible["orgao_cnpj"].astype(str))
    full=rel.copy(); full["orgao_cnpj"]=full["orgao_cnpj"].astype(str); full["fornecedor_id_limpo"]=full["fornecedor_id_limpo"].astype(str)
    er=full[full["orgao_cnpj"].isin(eligible_ids)].copy()
    ranking_rel = er if scope=="eligible" else full
    supplier_stats=(ranking_rel.groupby("fornecedor_id_limpo")
        .agg(degree=("orgao_cnpj","nunique"),strength=("valor_relacao","sum"))
        .reset_index())
    universe=set(supplier_stats["fornecedor_id_limpo"].astype(str))
    A,blist,slist,si=build_matrix(full,eligible_ids,universe)
    supplier_stats["idx"]=supplier_stats["fornecedor_id_limpo"].map(si)
    rng=np.random.default_rng(SEED)
    rows=[]
    for pct in [.01,.05,.10]:
        k=max(1,int(math.ceil(len(slist)*pct)))
        rnd={.25:[],.5:[],.75:[]}; rnd_loss=[]
        for _ in range(DRAWS):
            idx=rng.choice(len(slist),size=k,replace=False)
            loss=A[:,idx].sum(axis=1); rnd_loss.append(float(loss.mean()))
            for t in rnd: rnd[t].append(float((loss>=t).mean()))
        for strategy in ["degree","strength"]:
            target=supplier_stats.nlargest(k,strategy)["idx"].astype(int).to_numpy()
            loss=A[:,target].sum(axis=1)
            for t in [.25,.5,.75]:
                rr=np.asarray(rnd[t]); rl=np.asarray(rnd_loss)
                rows.append({
                    "ranking_scope":scope,"strategy":strategy,"pct_removed":pct,"k":k,"threshold":t,
                    "candidate_suppliers":len(slist),"eligible_buyers":len(blist),
                    "target_severe_share":float((loss>=t).mean()),
                    "random_severe_mean":float(rr.mean()),"random_severe_p025":float(np.quantile(rr,.025)),"random_severe_p975":float(np.quantile(rr,.975)),
                    "target_mean_loss":float(loss.mean()),"random_mean_loss":float(rl.mean()),"random_mean_loss_p025":float(np.quantile(rl,.025)),"random_mean_loss_p975":float(np.quantile(rl,.975)),
                })
    return pd.DataFrame(rows), supplier_stats


def main():
    rel=pd.read_csv(INP/"relacoes_jan_fev_assinados_2025.csv.gz",dtype={"orgao_cnpj":"string","fornecedor_id_limpo":"string"},low_memory=False)
    eligible=pd.read_csv(INP/"compradores_elegiveis_jan_fev.csv",dtype={"orgao_cnpj":"string"},low_memory=False)
    results=[]; stats={}
    for scope in ["eligible","global"]:
        r,s=run_scope(rel,eligible,scope); results.append(r); stats[scope]=s
        s.to_csv(OUT/f"ranking_fornecedores_{scope}.csv",index=False,encoding="utf-8-sig")
    out=pd.concat(results,ignore_index=True)
    out.to_csv(OUT/"comparacao_simulacoes.csv",index=False,encoding="utf-8-sig")
    key=out[out["threshold"].eq(.5)].copy()
    key.to_csv(OUT/"comparacao_limiar_50pct.csv",index=False,encoding="utf-8-sig")
    resumo={
        "eligible_buyers":int(len(eligible)),
        "relations_full":int(len(rel)),
        "suppliers_candidate_eligible":int(len(stats["eligible"])),
        "suppliers_candidate_global":int(len(stats["global"])),
        "random_draws":DRAWS,"seed":SEED,
        "limiar_50pct":key.to_dict(orient="records"),
        "interpretacao":"A hipótese de vulnerabilidade é mais robusta se a remoção direcionada permanecer acima do intervalo aleatório também quando o ranking é calculado na rede global observada.",
    }
    (OUT/"resumo_robustez.json").write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(resumo,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
