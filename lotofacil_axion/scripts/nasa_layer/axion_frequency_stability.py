#!/usr/bin/env python3
"""AXION frequency-dispersion stability analysis.

Tests whether the Phase-1 excess cross-number frequency dispersion is stable
across non-overlapping windows and expanding prefixes. The null distribution of
count vectors is simulated from the exact first/second moments of a 15-of-25
uniform draw using a multivariate-normal approximation. This approximation was
checked against the exact Phase-1 Monte Carlo at N=3435 and closely reproduces
its mean/SD/quantiles for dispersion metrics.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
import numpy as np


def load_binary(path):
    rows=[]; contests=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f)
        for z in r:
            contests.append(int(z['contest'])); rows.append([int(z[f'd{i:02d}']) for i in range(1,26)])
    return np.asarray(contests),np.asarray(rows,dtype=np.int8)

def bh_adjust(p):
    p=np.asarray(p,float); m=len(p); o=np.argsort(p); q=np.empty(m); run=1.0
    for rev in range(m-1,-1,-1):
        i=o[rev]; rank=rev+1; run=min(run,p[i]*m/rank); q[i]=min(1.0,run)
    return q

def metrics(M):
    f=M.sum(0).astype(float); n=len(M); e=.6*n
    return {'freq_sd':float(f.std(ddof=1)),'freq_range':float(f.max()-f.min()),'freq_chi2':float(np.sum((f-e)**2/e))}

def null_metrics(n,B,seed):
    cov=np.full((25,25),-0.01*n,float); np.fill_diagonal(cov,.24*n)
    rng=np.random.default_rng(seed); X=rng.multivariate_normal(np.full(25,.6*n),cov,size=B)
    sd=X.std(1,ddof=1); rg=X.max(1)-X.min(1); chi=np.sum((X-.6*n)**2/(.6*n),axis=1)
    return {'freq_sd':sd,'freq_range':rg,'freq_chi2':chi}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binary',required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--null-b',type=int,default=100000); ap.add_argument('--seed',type=int,default=20260910)
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    contests,B=load_binary(a.binary); N=len(B); cache={}
    def getnull(n):
        if n not in cache: cache[n]=null_metrics(n,a.null_b,a.seed+n)
        return cache[n]
    rows=[]
    for w in [250,500,1000]:
        k=0
        for start in range(0,N-w+1,w):
            k+=1; M=B[start:start+w]; obs=metrics(M); null=getnull(w)
            for met,val in obs.items():
                p=(1+np.sum(null[met]>=val))/(a.null_b+1)
                rows.append({'design':'window','size':w,'segment':k,'start_contest':int(contests[start]),
                             'end_contest':int(contests[start+w-1]),'metric':met,'actual':val,
                             'null_mean':float(null[met].mean()),'null_sd':float(null[met].std(ddof=1)),
                             'p_upper_excess':float(p)})
    for n in [500,1000,1500,2000,2500,3000,N]:
        obs=metrics(B[:n]); null=getnull(n)
        for met,val in obs.items():
            p=(1+np.sum(null[met]>=val))/(a.null_b+1)
            rows.append({'design':'expanding','size':n,'segment':1,'start_contest':int(contests[0]),
                         'end_contest':int(contests[n-1]),'metric':met,'actual':val,
                         'null_mean':float(null[met].mean()),'null_sd':float(null[met].std(ddof=1)),
                         'p_upper_excess':float(p)})
    for met in ['freq_sd','freq_range','freq_chi2']:
        idx=[i for i,r in enumerate(rows) if r['metric']==met]; q=bh_adjust([rows[i]['p_upper_excess'] for i in idx])
        for i,v in zip(idx,q): rows[i]['q_bh_within_metric']=float(v); rows[i]['triage_q_lt_0_05']=bool(v<.05)
    with open(out/'frequency_stability.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    primary=[r for r in rows if r['metric']=='freq_chi2']
    summary={'module':'frequency_stability','n_contests':N,'null_B':a.null_b,'seed':a.seed,
             'primary_metric':'freq_chi2','significant_primary_cuts':[r for r in primary if r['triage_q_lt_0_05']],
             'full_history':[r for r in rows if r['design']=='expanding' and r['size']==N]}
    (out/'frequency_stability_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
