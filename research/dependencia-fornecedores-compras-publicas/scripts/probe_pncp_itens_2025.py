#!/usr/bin/env python3
"""Probe compacto de campos de classificação em itens de contratações de 2025."""
import json
from pathlib import Path
import pandas as pd
import requests

BASE="https://pncp.gov.br/api/pncp"
PROCS=[
 ("88659313000105-1-000238/2025","88659313000105",2025,238),
 ("14675553000159-1-000011/2025","14675553000159",2025,11),
 ("06102908000192-1-000004/2025","06102908000192",2025,4),
]
OUT=Path(__file__).resolve().parents[1]/"results"/"pncp_itens_2025_probe"
OUT.mkdir(parents=True,exist_ok=True)

def items(payload):
    if isinstance(payload,list): return payload
    for k in ("itens","data","content","items"):
        if isinstance(payload,dict) and isinstance(payload.get(k),list): return payload[k]
    return []

def results(payload):
    if isinstance(payload,list): return payload
    for k in ("listaResultados","resultados","data","content","items"):
        if isinstance(payload,dict) and isinstance(payload.get(k),list): return payload[k]
    return []

def present(s):
    return s.notna() & s.astype('string').str.strip().ne('')

s=requests.Session(); s.headers.update({'User-Agent':'Pesquisa-PNCP-Itens-2025/1.0','Accept':'application/json'})
all_items=[]; all_res=[]; status=[]
for pid,cnpj,ano,seq in PROCS:
    base=f"{BASE}/v1/orgaos/{cnpj}/compras/{ano}/{seq}"
    r=s.get(base+'/itens',params={'pagina':1,'tamanhoPagina':100},timeout=60); r.raise_for_status()
    its=items(r.json()); status.append({'id_compra':pid,'endpoint':'itens','status':'ok','n':len(its)})
    for x in its:
        y=dict(x); y['id_compra_probe']=pid; all_items.append(y)
    eligible=[x for x in its if bool(x.get('temResultado'))][:5]
    for x in eligible:
        n=x.get('numeroItem')
        try:
            rr=s.get(base+f'/itens/{n}/resultados',timeout=60); rr.raise_for_status()
            rs=results(rr.json()); status.append({'id_compra':pid,'endpoint':f'resultado_{n}','status':'ok','n':len(rs)})
            for z in rs:
                q=dict(z); q['id_compra_probe']=pid; q['numeroItem_probe']=n
                if str(q.get('tipoPessoa','')).upper()!='PJ':
                    q['niFornecedor']=None; q['nomeRazaoSocialFornecedor']=None
                all_res.append(q)
        except Exception as e:
            status.append({'id_compra':pid,'endpoint':f'resultado_{n}','status':'erro','n':0,'erro':repr(e)})

di=pd.json_normalize(all_items,sep='.') if all_items else pd.DataFrame()
dr=pd.json_normalize(all_res,sep='.') if all_res else pd.DataFrame()
pd.DataFrame(status).to_csv(OUT/'status.csv',index=False)
di.to_csv(OUT/'itens.csv',index=False)
dr.to_csv(OUT/'resultados_minimizados.csv',index=False)
rows=[]
for pid,g in di.groupby('id_compra_probe'):
    def pc(c): return round(float(present(g[c]).mean()*100),2) if c in g else None
    rows.append({
      'id_compra':pid,'n_itens_pagina1':len(g),
      'tem_resultado_pct':round(float(g['temResultado'].fillna(False).astype(bool).mean()*100),2) if 'temResultado' in g else None,
      'material_servico_pct':pc('materialOuServico'),'categoria_item_pct':pc('itemCategoriaNome'),
      'categoria_item_nao_se_aplica_pct':round(float(g['itemCategoriaNome'].astype('string').str.lower().eq('não se aplica').mean()*100),2) if 'itemCategoriaNome' in g else None,
      'ncm_nbs_pct':pc('ncmNbsCodigo'),'catalogo_codigo_pct':pc('catalogoCodigoItem'),
      'categoria_catalogo_pct':pc('categoriaItemCatalogo.nome')
    })
res=pd.DataFrame(rows); res.to_csv(OUT/'resumo_cobertura.csv',index=False)
report={'contratacoes':len(PROCS),'itens':len(di),'resultados':len(dr),'erros':sum(1 for x in status if x['status']=='erro')}
(OUT/'resumo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(res.to_string(index=False)); print(json.dumps(report,ensure_ascii=False,indent=2))
