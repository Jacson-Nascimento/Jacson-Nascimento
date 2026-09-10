#!/usr/bin/env python3
"""AXION-BB: regime-change screening with Bernoulli block fitness.

Two complementary outputs are produced:
1) an observed-only exact dynamic-programming segmentation using the Bernoulli
   block likelihood and Scargle's ncp_prior as the complexity penalty;
2) an empirical null calibration of the strongest one-change split using
   uniform Bernoulli(0.6) sequences of identical length.

The null-calibrated max-split statistic is the inferential gate. The exact
segmentation is descriptive until the split evidence survives multiple tests.
"""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path
import numpy as np


def bh_adjust(p):
    p=np.asarray(p,float); m=len(p); order=np.argsort(p); q=np.empty(m); running=1.0
    for rev in range(m-1,-1,-1):
        idx=order[rev]; rank=rev+1; running=min(running,p[idx]*m/rank); q[idx]=min(1.0,running)
    return q


def load_binary(path):
    contests=[]; dates=[]; rows=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f)
        for z in r:
            contests.append(int(z['contest'])); dates.append(z['date'])
            rows.append([int(z[f'd{i:02d}']) for i in range(1,26)])
    return np.asarray(contests), dates, np.asarray(rows,dtype=np.int8)


def ll_bernoulli(k,n):
    k=np.asarray(k,float); n=np.asarray(n,float); p=k/n
    out=np.zeros(np.broadcast(k,n).shape,dtype=float)
    m1=k>0; m0=k<n
    with np.errstate(divide='ignore',invalid='ignore'):
        out=np.where(m1,k*np.log(p),0.0)+np.where(m0,(n-k)*np.log1p(-p),0.0)
    return out


def exact_blocks(x, penalty):
    x=np.asarray(x,dtype=np.int64); n=len(x); cs=np.concatenate(([0],np.cumsum(x)))
    best=np.empty(n,float); last=np.empty(n,np.int32)
    for R in range(n):
        starts=np.arange(R+1); nn=R-starts+1; k=cs[R+1]-cs[starts]
        fit=ll_bernoulli(k,nn)-penalty
        if R>0: fit[1:]+=best[:R]
        i=int(np.argmax(fit)); best[R]=fit[i]; last[R]=i
    edges=[]; ind=n
    while ind>0:
        i=int(last[ind-1]); edges.append(i); ind=i
    edges=sorted(set(edges+[n]));
    if not edges or edges[0]!=0: edges=[0]+edges
    rates=[float(x[a:b].mean()) for a,b in zip(edges[:-1],edges[1:])]
    return edges,rates


def max_split_gain_1d(x,min_block):
    x=np.asarray(x,dtype=np.int64); n=len(x); cs=np.cumsum(x)
    t=np.arange(min_block,n-min_block+1)
    k1=cs[t-1]; k2=cs[-1]-k1
    gain=ll_bernoulli(k1,t)+ll_bernoulli(k2,n-t)-ll_bernoulli(cs[-1],n)
    i=int(np.argmax(gain)); return float(gain[i]),int(t[i]),float(k1[i]/t[i]),float(k2[i]/(n-t[i]))


def null_max_gains(n,B,seed,min_block,batch=250):
    rng=np.random.default_rng(seed); out=np.empty(B,float); pos=0
    t=np.arange(min_block,n-min_block+1)
    nt=(n-t).astype(float); tf=t.astype(float)
    while pos<B:
        b=min(batch,B-pos)
        X=rng.binomial(1,0.6,size=(b,n)).astype(np.int8)
        cs=np.cumsum(X,axis=1,dtype=np.int32); total=cs[:,-1]
        k1=cs[:,t-1]; k2=total[:,None]-k1
        base=ll_bernoulli(total,n)[:,None]
        gains=ll_bernoulli(k1,tf[None,:])+ll_bernoulli(k2,nt[None,:])-base
        out[pos:pos+b]=np.max(gains,axis=1); pos+=b
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binary',required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--p0',type=float,default=0.05); ap.add_argument('--null-b',type=int,default=20000)
    ap.add_argument('--seed',type=int,default=20260910); ap.add_argument('--min-block',type=int,default=30)
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    contests,dates,B=load_binary(a.binary); n=len(B)
    penalty=4-math.log(73.53*a.p0*(n**-0.478))
    null=null_max_gains(n,a.null_b,a.seed,a.min_block)

    rows=[]; segments=[]
    for j in range(25):
        x=B[:,j]; gain,split,r1,r2=max_split_gain_1d(x,a.min_block)
        p=(1+np.sum(null>=gain))/(a.null_b+1)
        edges,rates=exact_blocks(x,penalty)
        rows.append({'number':j+1,'global_rate':float(x.mean()),'max_split_gain':gain,
                     'best_split_index':split,'best_split_after_contest':int(contests[split-1]),
                     'best_split_before_contest':int(contests[split]),'rate_before':r1,'rate_after':r2,
                     'rate_difference_after_minus_before':r2-r1,'p_empirical_max_split':p,
                     'exact_scargle_n_blocks':len(edges)-1})
        for s,(u,v,rate) in enumerate(zip(edges[:-1],edges[1:],rates),1):
            segments.append({'number':j+1,'segment':s,'start_contest':int(contests[u]),'end_contest':int(contests[v-1]),
                             'start_date':dates[u],'end_date':dates[v-1],'length':v-u,'rate':rate})
    q=bh_adjust([r['p_empirical_max_split'] for r in rows])
    for i,r in enumerate(rows):
        r['q_bh_25_numbers']=float(q[i]); r['triage_q_lt_0_05']=bool(q[i]<0.05)

    with open(out/'bb_number_summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(out/'bb_segments_exact_observed.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(segments[0])); w.writeheader(); w.writerows(segments)
    with open(out/'bb_null_max_split_gain.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['simulation','max_split_gain']);
        for i,v in enumerate(null,1): w.writerow([i,v])
    meta={'module':'AXION-BB','method':'Bernoulli block fitness + observed exact DP + null-calibrated max one-change split',
          'n_contests':n,'contest_min':int(contests.min()),'contest_max':int(contests.max()),'p0':a.p0,
          'scargle_penalty':penalty,'null_B':a.null_b,'seed':a.seed,'min_block_length':a.min_block,
          'null_quantiles':{str(qv):float(np.quantile(null,qv)) for qv in [0.5,0.9,0.95,0.99,0.999]}}
    (out/'bb_metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'candidates':[r for r in rows if r['triage_q_lt_0_05']],
                      'top5':sorted(rows,key=lambda z:z['p_empirical_max_split'])[:5]},indent=2,ensure_ascii=False))

if __name__=='__main__': main()
