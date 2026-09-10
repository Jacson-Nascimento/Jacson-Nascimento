#!/usr/bin/env python3
"""AXION-COMP: compression-based global structure test for the 25D binary matrix.

Uses packed-bit representations and two independent compressors (zlib, bz2),
under row-major and column-major layouts. Lower compressed/raw ratio means
higher compressibility. Real non-overlapping windows are compared with uniform
15/25 synthetic histories of the same size. The inferential target is whether
real data are *more compressible* than the null model.
"""
from __future__ import annotations
import argparse,bz2,csv,json,zlib
from pathlib import Path
import numpy as np


def load_binary(path):
    rows=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f)
        for z in r: rows.append([int(z[f'd{i:02d}']) for i in range(1,26)])
    return np.asarray(rows,dtype=np.uint8)

def bh_adjust(p):
    p=np.asarray(p,float); m=len(p); o=np.argsort(p); q=np.empty(m); run=1.0
    for rev in range(m-1,-1,-1):
        i=o[rev]; rank=rev+1; run=min(run,p[i]*m/rank); q[i]=min(1.,run)
    return q

def ratio(M,layout,algo):
    flat=M.ravel(order='C' if layout=='row_major' else 'F')
    raw=np.packbits(flat).tobytes(); den=max(1,len(raw))
    if algo=='zlib': c=zlib.compress(raw,9)
    elif algo=='bz2': c=bz2.compress(raw,compresslevel=9)
    else: raise ValueError(algo)
    return len(c)/den

def random_binary(rng,n):
    keys=rng.random((n,25)); idx=np.argpartition(keys,15,axis=1)[:,:15]
    B=np.zeros((n,25),dtype=np.uint8); B[np.arange(n)[:,None],idx]=1
    return B

def null_ratios(n,Bn,seed):
    rng=np.random.default_rng(seed); combos=[('row_major','zlib'),('row_major','bz2'),('column_major','zlib'),('column_major','bz2')]
    out={c:np.empty(Bn,float) for c in combos}
    for b in range(Bn):
        M=random_binary(rng,n)
        for c in combos: out[c][b]=ratio(M,*c)
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binary',required=True); ap.add_argument('--out',required=True); ap.add_argument('--seed',type=int,default=20260910)
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    X=load_binary(a.binary); N=len(X)
    sizes=[250,500,1000,N]; Bmap={250:2000,500:2000,1000:1500,N:1000}; combos=[('row_major','zlib'),('row_major','bz2'),('column_major','zlib'),('column_major','bz2')]
    rows=[]; null_summary=[]
    for n in sizes:
        real=[X[s:s+n] for s in range(0,N-n+1,n)]; k=len(real); nr=null_ratios(n,Bmap[n],a.seed+n)
        rng=np.random.default_rng(a.seed+10*n)
        for layout,algo in combos:
            rv=np.array([ratio(M,layout,algo) for M in real]); nv=nr[(layout,algo)]
            if k==1: boot=nv
            else: boot=np.array([rng.choice(nv,size=k,replace=True).mean() for _ in range(5000)])
            actual=float(rv.mean()); p=float((1+np.sum(boot<=actual))/(len(boot)+1))
            rows.append({'window_size':n,'real_windows':k,'layout':layout,'algorithm':algo,'actual_mean_ratio':actual,
                         'actual_sd_across_windows':float(rv.std(ddof=1)) if k>1 else 0.0,'null_mean_ratio':float(nv.mean()),
                         'null_sd_ratio':float(nv.std(ddof=1)),'p_lower_more_compressible':p,'null_B':Bmap[n]})
            null_summary.append({'window_size':n,'layout':layout,'algorithm':algo,'null_B':Bmap[n],
                                 'mean':float(nv.mean()),'sd':float(nv.std(ddof=1)),'q025':float(np.quantile(nv,.025)),
                                 'q50':float(np.quantile(nv,.5)),'q975':float(np.quantile(nv,.975))})
    q=bh_adjust([r['p_lower_more_compressible'] for r in rows])
    for i,r in enumerate(rows): r['q_bh_16_tests']=float(q[i]); r['triage_q_lt_0_05']=bool(q[i]<.05)
    with open(out/'compression_summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(out/'compression_null_summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(null_summary[0])); w.writeheader(); w.writerows(null_summary)
    summary={'module':'AXION-COMP','n_contests':N,'tests':len(rows),'significant':[r for r in rows if r['triage_q_lt_0_05']],
             'top5':sorted(rows,key=lambda r:r['p_lower_more_compressible'])[:5],
             'decision_rule':'Only lower compression ratios than null after BH indicate candidate extra structure.'}
    (out/'compression_metadata.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
