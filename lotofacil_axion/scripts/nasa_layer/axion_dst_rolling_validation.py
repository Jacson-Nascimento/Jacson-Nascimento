#!/usr/bin/env python3
"""Rolling chronological replication for AXION-DST."""
from __future__ import annotations
import argparse,csv,json,math,sys
from pathlib import Path
import numpy as np
from scipy.stats import ks_2samp
sys.path.insert(0,str(Path(__file__).resolve().parent))
from axion_dst import load_features, random_draws, vector_features


def bh_adjust(p):
    p=np.asarray(p,float); m=len(p); o=np.argsort(p); q=np.empty(m); run=1.0
    for rev in range(m-1,-1,-1):
        i=o[rev]; rank=rev+1; run=min(run,p[i]*m/rank); q[i]=min(1.,run)
    return q

def fit_transform(train):
    mu=np.nanmean(train,axis=0); sd=np.nanstd(train,axis=0,ddof=1); sd[sd==0]=1.0
    Z=(np.where(np.isnan(train),mu,train)-mu)/sd; C=np.cov(Z,rowvar=False)
    ev,P=np.linalg.eigh(C); o=np.argsort(ev)[::-1]; ev=ev[o]; P=P[:,o]
    keep=ev>max(ev[0]*1e-10,1e-12); lam=ev[keep]; P=P[:,keep]
    def score(Y):
        Y=np.where(np.isnan(Y),mu,Y); W=((Y-mu)/sd@P)/np.sqrt(lam); return np.sum(W*W,axis=1)
    return score,int(keep.sum())

def bootstrap_mean_p(rng,null,actual,n,B):
    vals=np.empty(B)
    for i in range(B): vals[i]=rng.choice(null,size=n,replace=True).mean()
    return float((1+np.sum(np.abs(vals-null.mean())>=abs(actual-null.mean())))/(B+1))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--features',required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--null-rows',type=int,default=30000); ap.add_argument('--bootstrap-b',type=int,default=3000); ap.add_argument('--seed',type=int,default=20260910)
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    contests,dates,names,X=load_features(a.features); N=len(X); block=N//10
    train_ends=[5*block,6*block,7*block,8*block,9*block]
    rows=[]
    for s,te in enumerate(train_ends,1):
        ts=te; ee=N if s==5 else min(N,te+block)
        train=X[:te]; test=X[ts:ee]; score,k=fit_transform(train); dtest=score(test)
        rng=np.random.default_rng(a.seed+s); parts=[]; rem=a.null_rows; prev=None
        while rem>0:
            b=min(5000,rem); draws=random_draws(rng,b); F,prev=vector_features(draws,prev); parts.append(score(F)); rem-=b
        dn=np.concatenate(parts); ks=ks_2samp(dtest,dn)
        pmean=bootstrap_mean_p(np.random.default_rng(a.seed+100+s),dn,float(dtest.mean()),len(dtest),a.bootstrap_b)
        rows.append({'split':s,'train_start_contest':int(contests[0]),'train_end_contest':int(contests[te-1]),
                     'test_start_contest':int(contests[ts]),'test_end_contest':int(contests[ee-1]),
                     'train_n':te,'test_n':ee-ts,'retained_components':k,
                     'actual_mean_distance2':float(dtest.mean()),'null_mean_distance2':float(dn.mean()),
                     'p_mean':pmean,'ks_statistic':float(ks.statistic),'p_ks':float(ks.pvalue)})
    qmean=bh_adjust([r['p_mean'] for r in rows]); qks=bh_adjust([r['p_ks'] for r in rows])
    for i,r in enumerate(rows):
        r['q_bh_mean_5_splits']=float(qmean[i]); r['q_bh_ks_5_splits']=float(qks[i]);
        r['mean_pass_q_lt_0_05']=bool(qmean[i]<.05); r['ks_pass_q_lt_0_05']=bool(qks[i]<.05)
    with open(out/'dst_rolling_validation.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={'module':'AXION-DST rolling validation','n_contests':N,'null_rows_per_split':a.null_rows,'bootstrap_B':a.bootstrap_b,
             'splits':rows,'replicated_mean_significant_splits':sum(r['mean_pass_q_lt_0_05'] for r in rows),
             'replicated_ks_significant_splits':sum(r['ks_pass_q_lt_0_05'] for r in rows)}
    (out/'dst_rolling_validation_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
