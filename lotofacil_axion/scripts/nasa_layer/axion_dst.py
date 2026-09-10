#!/usr/bin/env python3
"""AXION-DST: decorrelation/whitening layer inspired by JPL Decorrelation Stretch.

The module standardizes the AXION feature matrix on a chronological training
sample, diagonalizes its correlation structure, whitens the retained PCA
subspace, and scores the holdout contests by squared whitened distance.
A large uniform 15/25 synthetic sample is transformed with the *same* training
geometry to calibrate the holdout distance distribution.
"""
from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path
import numpy as np
from scipy.stats import ks_2samp, binomtest

PRIMES=np.array([2,3,5,7,11,13,17,19,23])
BORDER=np.array([n for n in range(1,26) if ((n-1)//5+1 in (1,5) or (n-1)%5+1 in (1,5))])


def load_features(path):
    with open(path,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); names=[x for x in r.fieldnames if x not in ('contest','date')]
        contests=[]; dates=[]; rows=[]
        for z in r:
            contests.append(int(z['contest'])); dates.append(z['date'])
            rows.append([np.nan if z[n]=='' else float(z[n]) for n in names])
    return np.asarray(contests),dates,names,np.asarray(rows,float)


def random_draws(rng,n):
    keys=rng.random((n,25)); idx=np.argpartition(keys,15,axis=1)[:,:15]+1
    return np.sort(idx,axis=1).astype(np.int16)


def vector_features(draws, prev_binary=None):
    X=np.asarray(draws,np.int16); n=len(X); dif=np.diff(X,axis=1)
    binary=np.zeros((n,25),dtype=np.int8); rr=np.arange(n)[:,None]; binary[rr,X-1]=1
    s=X.sum(1); mean=X.mean(1); sd=X.std(1,ddof=1); mn=X[:,0]; mx=X[:,-1]; rg=mx-mn
    even=(X%2==0).sum(1); odd=15-even; prime=np.isin(X,PRIMES).sum(1)
    low=(X<=13).sum(1); high=15-low; border=np.isin(X,BORDER).sum(1); center=15-border
    cp=(dif==1).sum(1)
    cons=(dif==1); cur=np.ones(n,dtype=np.int16); best=np.ones(n,dtype=np.int16)
    for j in range(cons.shape[1]):
        cur=np.where(cons[:,j],cur+1,1); best=np.maximum(best,cur)
    gap_mean=dif.mean(1); gap_sd=dif.std(1,ddof=1); gap_max=dif.max(1)
    ent=np.zeros(n,float)
    for g in range(1,12):
        c=(dif==g).sum(1); p=c/14.0; m=c>0; ent[m]-=p[m]*np.log2(p[m])
    weights=(2*np.arange(15)-14).astype(float)
    mean_pair=(X*weights).sum(1)/105.0
    repeat=np.empty(n,float)
    if prev_binary is None: repeat[0]=np.nan
    else: repeat[0]=(binary[0]*prev_binary).sum()
    if n>1: repeat[1:]=(binary[1:]*binary[:-1]).sum(1)
    jacc=repeat/(30-repeat)
    row_counts=np.column_stack([((X>=1+5*r)&(X<=5*(r+1))).sum(1) for r in range(5)])
    col_counts=np.column_stack([(((X-1)%5)==c).sum(1) for c in range(5)])
    cols=[s,mean,sd,mn,mx,rg,even,odd,prime,low,high,border,center,cp,best,gap_mean,gap_sd,gap_max,ent,mean_pair,repeat,jacc]
    cols.extend([row_counts[:,i] for i in range(5)]); cols.extend([col_counts[:,i] for i in range(5)])
    return np.column_stack(cols),binary[-1]


def bootstrap_stat(rng, null, n, B, stat):
    vals=np.empty(B,float)
    for i in range(B):
        samp=rng.choice(null,size=n,replace=True); vals[i]=stat(samp)
    return vals


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--features',required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--train-frac',type=float,default=0.8); ap.add_argument('--null-rows',type=int,default=100000)
    ap.add_argument('--bootstrap-b',type=int,default=5000); ap.add_argument('--seed',type=int,default=20260910)
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    contests,dates,names,X=load_features(a.features); n=len(X); split=int(math.floor(n*a.train_frac))
    train=X[:split].copy(); hold=X[split:].copy()
    mu=np.nanmean(train,axis=0); sd=np.nanstd(train,axis=0,ddof=1); sd[sd==0]=1.0
    train=np.where(np.isnan(train),mu,train); hold=np.where(np.isnan(hold),mu,hold)
    Z=(train-mu)/sd; C=np.cov(Z,rowvar=False)
    eigval,eigvec=np.linalg.eigh(C); order=np.argsort(eigval)[::-1]; eigval=eigval[order]; eigvec=eigvec[:,order]
    tol=max(eigval[0]*1e-10,1e-12); keep=eigval>tol; lam=eigval[keep]; P=eigvec[:,keep]
    def score(Y):
        Y=np.where(np.isnan(Y),mu,Y); Z=(Y-mu)/sd; W=(Z@P)/np.sqrt(lam); return W, np.sum(W*W,axis=1)
    W_hold,d_hold=score(hold)

    rng=np.random.default_rng(a.seed); d_null_parts=[]; remaining=a.null_rows; prev=None
    while remaining>0:
        b=min(5000,remaining); draws=random_draws(rng,b); F,prev=vector_features(draws,prev)
        _,d=score(F); d_null_parts.append(d); remaining-=b
    d_null=np.concatenate(d_null_parts)
    ks=ks_2samp(d_hold,d_null,alternative='two-sided',method='auto')
    rngb=np.random.default_rng(a.seed+1); m=len(d_hold)
    bm=bootstrap_stat(rngb,d_null,m,a.bootstrap_b,np.mean); bq=bootstrap_stat(rngb,d_null,m,a.bootstrap_b,lambda v:np.quantile(v,.95))
    pmean=(1+np.sum(np.abs(bm-d_null.mean())>=abs(d_hold.mean()-d_null.mean())))/(a.bootstrap_b+1)
    pq95=(1+np.sum(np.abs(bq-np.quantile(d_null,.95))>=abs(np.quantile(d_hold,.95)-np.quantile(d_null,.95))))/(a.bootstrap_b+1)
    q99=float(np.quantile(d_null,.99)); above=int(np.sum(d_hold>q99)); p_above=binomtest(above,m,.01,alternative='two-sided').pvalue

    with open(out/'dst_holdout_scores.csv','w',newline='',encoding='utf-8') as f:
        fields=['contest','date','distance2']+[f'w{i+1}' for i in range(W_hold.shape[1])]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for i in range(m):
            z={'contest':int(contests[split+i]),'date':dates[split+i],'distance2':float(d_hold[i])}
            z.update({f'w{k+1}':float(W_hold[i,k]) for k in range(W_hold.shape[1])}); w.writerow(z)
    with open(out/'dst_components.csv','w',newline='',encoding='utf-8') as f:
        fields=['component','eigenvalue','explained_ratio']+names; w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        total=eigval[eigval>0].sum()
        for k in range(len(lam)):
            z={'component':k+1,'eigenvalue':float(lam[k]),'explained_ratio':float(lam[k]/total)}
            z.update({names[j]:float(P[j,k]) for j in range(len(names))}); w.writerow(z)
    with open(out/'dst_null_distance_sample.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['distance2']); [w.writerow([float(v)]) for v in d_null]
    raw_p=np.array([pmean,pq95,p_above,ks.pvalue],float)
    order=np.argsort(raw_p); qvals=np.empty(4,float); running=1.0
    for rev in range(3,-1,-1):
        idx=order[rev]; rank=rev+1; running=min(running,raw_p[idx]*4/rank); qvals[idx]=min(1.0,running)
    summary={
      'module':'AXION-DST','n_contests':n,'train_n':split,'holdout_n':m,'train_end_contest':int(contests[split-1]),
      'holdout_start_contest':int(contests[split]),'features':len(names),'retained_components':int(keep.sum()),
      'holdout_mean_distance2':float(d_hold.mean()),'null_mean_distance2':float(d_null.mean()),'p_bootstrap_mean':float(pmean),'q_bh_mean':float(qvals[0]),
      'holdout_q95_distance2':float(np.quantile(d_hold,.95)),'null_q95_distance2':float(np.quantile(d_null,.95)),'p_bootstrap_q95':float(pq95),'q_bh_q95':float(qvals[1]),
      'null_q99_distance2':q99,'holdout_above_null_q99':above,'holdout_above_null_q99_rate':above/m,'p_binomial_above_q99':float(p_above),'q_bh_above_q99':float(qvals[2]),
      'ks_statistic':float(ks.statistic),'ks_pvalue':float(ks.pvalue),'q_bh_ks':float(qvals[3]),'null_rows':a.null_rows,'bootstrap_B':a.bootstrap_b,'seed':a.seed,
      'interpretation_gate':'DST is descriptive unless distributional differences survive validation and add out-of-sample information.'}
    (out/'dst_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
