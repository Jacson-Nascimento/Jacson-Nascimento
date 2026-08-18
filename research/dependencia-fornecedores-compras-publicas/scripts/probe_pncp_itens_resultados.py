#!/usr/bin/env python3
"""Probe de itens e resultados de contratações PNCP.

Objetivo: medir se os itens permitem refinar a definição de mercado e se os
resultados de item ligam fornecedores vencedores às classificações de item.

Não produz resultados econômicos do artigo.
"""
from __future__ import annotations

import json
from pathlib import Path
import requests
import pandas as pd

BASE = "https://pncp.gov.br/api/pncp"
# Contratações reais já observadas no piloto/microamostra.
PROCUREMENTS = [
    {"id":"00402552000126-1-000316/2022","cnpj":"00402552000126","ano":2022,"seq":316},
    {"id":"00396895000125-1-000495/2022","cnpj":"00396895000125","ano":2022,"seq":495},
    {"id":"12075748000132-1-000133/2024","cnpj":"12075748000132","ano":2024,"seq":133},
]
MAX_ITEMS_RESULTS = 50
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "pncp_itens_probe"
OUT.mkdir(parents=True, exist_ok=True)


def get_json(session, url, params=None):
    r = session.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def extract_items(payload):
    if isinstance(payload, list):
        return payload
    for key in ("itens", "data", "content", "items"):
        val = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(val, list):
            return val
    return []


def extract_results(payload):
    if isinstance(payload, list):
        return payload
    for key in ("listaResultados", "resultados", "data", "content", "items"):
        val = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(val, list):
            return val
    return []


def nonempty(series):
    return series.notna() & series.astype("string").str.strip().ne("")


def main():
    s = requests.Session()
    s.headers.update({"User-Agent":"Pesquisa-Academica-PNCP-Itens/1.0","Accept":"application/json"})
    item_rows=[]
    result_rows=[]
    status=[]

    for p in PROCUREMENTS:
        base = f"{BASE}/v1/orgaos/{p['cnpj']}/compras/{p['ano']}/{p['seq']}"
        try:
            payload = get_json(s, base + "/itens", {"pagina":1,"tamanhoPagina":500})
            items = extract_items(payload)
            status.append({"id_compra":p["id"],"endpoint":"itens","status":"ok","n":len(items)})
        except Exception as e:
            status.append({"id_compra":p["id"],"endpoint":"itens","status":"erro","n":0,"erro":repr(e)})
            continue

        for it in items:
            row = dict(it)
            row["id_compra_probe"] = p["id"]
            item_rows.append(row)

        # Resultado por item, limitado para tornar o probe controlado.
        for it in items[:MAX_ITEMS_RESULTS]:
            numero = it.get("numeroItem")
            if numero is None:
                continue
            try:
                rp = get_json(s, base + f"/itens/{numero}/resultados")
                results = extract_results(rp)
                status.append({"id_compra":p["id"],"endpoint":f"resultado_item_{numero}","status":"ok","n":len(results)})
                for res in results:
                    rr = dict(res)
                    rr["id_compra_probe"] = p["id"]
                    rr["numeroItem_probe"] = numero
                    # não persistir nome de PF no arquivo público
                    if str(rr.get("tipoPessoa", "")).upper() != "PJ":
                        rr["niFornecedor"] = None
                        rr["nomeRazaoSocialFornecedor"] = None
                    result_rows.append(rr)
            except Exception as e:
                status.append({"id_compra":p["id"],"endpoint":f"resultado_item_{numero}","status":"erro","n":0,"erro":repr(e)})

    items_df = pd.json_normalize(item_rows, sep=".") if item_rows else pd.DataFrame()
    res_df = pd.json_normalize(result_rows, sep=".") if result_rows else pd.DataFrame()
    st = pd.DataFrame(status)

    items_df.to_csv(OUT/"itens_probe.csv", index=False, encoding="utf-8-sig")
    res_df.to_csv(OUT/"resultados_probe_minimizado.csv", index=False, encoding="utf-8-sig")
    st.to_csv(OUT/"status.csv", index=False, encoding="utf-8-sig")

    summary=[]
    if len(items_df):
        for compra, g in items_df.groupby("id_compra_probe"):
            def pct(col):
                return round(float(nonempty(g[col]).mean()*100),2) if col in g else None
            summary.append({
                "id_compra":compra,
                "n_itens_pagina1":len(g),
                "tem_resultado_pct":round(float(pd.to_numeric(g.get("temResultado"), errors="coerce").fillna(False).astype(bool).mean()*100),2) if "temResultado" in g else None,
                "material_servico_pct":pct("materialOuServico"),
                "item_categoria_pct":pct("itemCategoriaNome"),
                "ncm_nbs_pct":pct("ncmNbsCodigo"),
                "catalogo_codigo_pct":pct("catalogoCodigoItem"),
                "categoria_catalogo_pct":pct("categoriaItemCatalogo.nome"),
            })
    summary_df=pd.DataFrame(summary)
    summary_df.to_csv(OUT/"resumo_cobertura_itens.csv", index=False, encoding="utf-8-sig")

    # Correspondência fornecedor-item nos resultados públicos PJ.
    result_summary=[]
    if len(res_df):
        for compra,g in res_df.groupby("id_compra_probe"):
            pj = g[g.get("tipoPessoa", pd.Series(index=g.index,dtype="string")).astype("string").str.upper().eq("PJ")]
            homolog = pd.to_numeric(g.get("quantidadeHomologada"),errors="coerce") * pd.to_numeric(g.get("valorUnitarioHomologado"),errors="coerce")
            result_summary.append({
                "id_compra":compra,
                "n_resultados_consultados":len(g),
                "fornecedores_pj_distintos":int(pj["niFornecedor"].nunique()) if "niFornecedor" in pj else 0,
                "valor_homologado_resultados_consultados":float(homolog.sum(skipna=True)),
            })
    pd.DataFrame(result_summary).to_csv(OUT/"resumo_resultados.csv", index=False, encoding="utf-8-sig")

    report={
        "contratacoes_testadas":len(PROCUREMENTS),
        "itens_coletados":int(len(items_df)),
        "resultados_coletados":int(len(res_df)),
        "consultas_com_erro":int(st["status"].eq("erro").sum()) if len(st) else 0,
        "observacao":"Probe técnico. Nenhuma métrica representa resultado econômico do artigo. Identificadores de PF não são persistidos.",
    }
    (OUT/"resumo.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(summary_df.to_string(index=False))
    print(pd.DataFrame(result_summary).to_string(index=False))
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
