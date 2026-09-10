#!/usr/bin/env python3
"""AXION-SE/MSE: Sample Entropy and Multiscale Sample Entropy for 25 binary series.

Primary design:
- m = 2;
- scales = 1,2,3,5,10,20;
- tolerance r = ratio * SD(original series), ratios 0.15 and 0.20;
- coarse-graining by non-overlapping block means;
- null calibration from Bernoulli(0.6) sequences of identical length;
- empirical two-sided p-values and BH correction.

For discrete coarse scales where r < 1/scale, matching is exact and is counted
by integer pattern codes. For larger scales a Chebyshev-radius KD-tree is used.
"""
from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree


def bh_adjust(p):
    p=np.asarray(p,float); m=len(p); order=np.argsort(p); q=np.empty(m); running=1.0
    for rev in range(m-1,-1,-1):
        idx=order[rev]; rank=rev+1; running=min(running,p[idx]*m/rank); q[idx]=min(1.0,running)
    return q


def load_binary(path):
    rows=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f)
        for z in r: rows.append([int(z[f'd{i:02d}']) for i in range(1,26)])
    return np.asarray(rows,dtype=np.int8)


def exact_pair_count(c,L,base):
    n=len(c)-L+1
    if n<2: return 0
    code=np.zeros(n,dtype=np.int64)
    for j in range(L): code=code*base+c[j:j+n]
    _,cnt=np.unique(code,return_counts=True)
    return int(np.sum(cnt*(cnt-1)//2))


def kd_pair_count(y,L,r):
    if len(y)-L+1<2: return 0
    E=np.lib.stride_tricks.sliding_window_view(y,L)
    tree=cKDTree(E)
    return int(len(tree.query_pairs(r,p=np.inf,output_type='ndarray')))


def sampen_scale(x,scale,ratio,m=2):
    x=np.asarray(x,dtype=np.int8); n=(len(x)//scale)*scale
    c=x[:n].reshape(-1,scale).sum(1).astype(np.int16)
    sd=float(np.std(x,ddof=1)); r=ratio*sd
    exact=(r < (1.0/scale)-1e-12)
    if exact:
        base=scale+1; B=exact_pair_count(c,m,base); A=exact_pair_count(c,m+1,base)
    else:
        y=c.astype(float)/scale; B=kd_pair_count(y,m,r); A=kd_pair_count(y,m+1,r)
    if B<=0 or A<=0: return float('inf')
    return float(-math.log(A/B))


def two_sided_empirical(null,obs):
    n=len(null); lo=(1+np.sum(null<=obs))/(n+1); hi=(1+np.sum(null>=obs))/(n+1)
    return float(min(1.0,2*min(lo,hi)))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binary',required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--null-b',type=int,default=5000); ap.add_argument('--seed',type=int,default=20260910)
    ap.add_argument('--scales',default='1,2,3,5,10,20'); ap.add_argument('--ratios',default='0.15,0.20')
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    B=load_binary(a.binary); n=len(B); scales=[int(v) for v in a.scales.split(',')]; ratios=[float(v) for v in a.ratios.split(',')]

    obs=np.empty((len(ratios),25,len(scales)),float)
    for ir,ratio in enumerate(ratios):
        for j in range(25):
            for iscale,s in enumerate(scales): obs[ir,j,iscale]=sampen_scale(B[:,j],s,ratio)

    null=np.empty((len(ratios),a.null_b,len(scales)),float); rng=np.random.default_rng(a.seed)
    for b in range(a.null_b):
        x=rng.binomial(1,0.6,size=n).astype(np.int8)
        for ir,ratio in enumerate(ratios):
            for iscale,s in enumerate(scales): null[ir,b,iscale]=sampen_scale(x,s,ratio)

    cell_rows=[]; overall_rows=[]
    for ir,ratio in enumerate(ratios):
        pcell=[]; positions=[]
        means=null[ir].mean(0); sds=null[ir].std(0,ddof=1); sds[sds==0]=1
        znull=(null[ir]-means)/sds; Tnull=np.sum(znull*znull,axis=1)
        pover=[]
        for j in range(25):
            z=(obs[ir,j]-means)/sds; T=float(np.sum(z*z)); pT=float((1+np.sum(Tnull>=T))/(a.null_b+1)); pover.append(pT)
            overall_rows.append({'r_ratio':ratio,'number':j+1,'multiscale_T':T,'p_empirical_T':pT})
            for k,s in enumerate(scales):
                p=two_sided_empirical(null[ir,:,k],obs[ir,j,k]); pcell.append(p); positions.append(len(cell_rows))
                cell_rows.append({'r_ratio':ratio,'number':j+1,'scale':s,'sampen':float(obs[ir,j,k]),
                                  'null_mean':float(means[k]),'null_sd':float(sds[k]),'z':float(z[k]),'p_empirical_two_sided':p})
        qcell=bh_adjust(pcell)
        for q,idx in zip(qcell,positions): cell_rows[idx]['q_bh_25xscales_within_ratio']=float(q); cell_rows[idx]['triage_q_lt_0_05']=bool(q<0.05)
        qover=bh_adjust(pover)
        start=len(overall_rows)-25
        for j,q in enumerate(qover):
            overall_rows[start+j]['q_bh_25_numbers']=float(q); overall_rows[start+j]['triage_q_lt_0_05']=bool(q<0.05)

    with open(out/'entropy_scale_summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(cell_rows[0])); w.writeheader(); w.writerows(cell_rows)
    with open(out/'entropy_multiscale_number_summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(overall_rows[0])); w.writeheader(); w.writerows(overall_rows)
    ns=[]
    for ir,ratio in enumerate(ratios):
        for k,s in enumerate(scales):
            v=null[ir,:,k]; ns.append({'r_ratio':ratio,'scale':s,'mean':float(v.mean()),'sd':float(v.std(ddof=1)),
                'q025':float(np.quantile(v,.025)),'q50':float(np.quantile(v,.5)),'q975':float(np.quantile(v,.975))})
    with open(out/'entropy_null_summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(ns[0])); w.writeheader(); w.writerows(ns)
    meta={'module':'AXION-SE/MSE','n_contests':n,'m':2,'scales':scales,'r_ratios':ratios,'null_B':a.null_b,'seed':a.seed,
          'null_model':'Bernoulli(0.6) marginal presence sequence; appropriate for per-number temporal entropy.',
          'note':'No predictive interpretation without out-of-sample incremental validation.'}
    (out/'entropy_metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    cand=[r for r in overall_rows if r['triage_q_lt_0_05']]
    top=sorted(overall_rows,key=lambda z:z['p_empirical_T'])[:10]
    print(json.dumps({'candidates':cand,'top10':top},indent=2,ensure_ascii=False))

if __name__=='__main__': main()
