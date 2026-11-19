import json, random, statistics as st, numpy as np, sys
D=7293.06
ref=json.load(open('score-raw/reference/human_edit.timeline.json',encoding='utf-8-sig'))['clips']
def uni(iv):
    iv=sorted([list(x) for x in iv]); o=[]
    for a,b in iv:
        if o and a<=o[-1][1]: o[-1][1]=max(o[-1][1],b)
        else: o.append([a,b])
    return o
def tot(u): return sum(b-a for a,b in u)
def ov(x,y):
    i=j=0;s=0
    while i<len(x) and j<len(y):
        s+=max(0,min(x[i][1],y[j][1])-max(x[i][0],y[j][0]))
        if x[i][1]<y[j][1]: i+=1
        else: j+=1
    return s
def dil(u,t): return uni([[max(0,a-t),min(D,b+t)] for a,b in u])
R=uni([(c['in'],c['out']) for c in ref])
def f1(P,R,t=0):
    p=ov(P,dil(R,t))/tot(P) if t else ov(P,R)/tot(P)
    r=ov(R,dil(P,t))/tot(R) if t else ov(P,R)/tot(R)
    return 2*p*r/(p+r) if p+r else 0
# key moments: human clips >=15s (long performances/scenes)
key=[(c['in'],c['out']) for c in ref if c['out']-c['in']>=15]
def keyrec(P):
    hit=0
    for a,b in key:
        o=ov(P,[[a,b]])
        if o>=min(3,0.3*(b-a)) and o/(b-a)>=0.3: hit+=1
    return hit,len(key)
# loudness baseline
x=np.fromfile('audio8k.raw',dtype=np.int16).astype(np.float32)
sec=len(x)//8000; rms=np.sqrt((x[:sec*8000].reshape(sec,8000)**2).mean(1)+1e-9)
def loud_baseline(total,win=20):
    w=np.convolve(rms,np.ones(win)/win,mode='valid'); order=np.argsort(-w); taken=np.zeros(sec,bool); sel=[];acc=0
    for s in order:
        if taken[s:s+win].any(): continue
        taken[s:s+win]=True; sel.append([s,s+win]); acc+=win
        if acc>=total: break
    return uni(sel)
def rand_f1(lens,t=0,n=500):
    out=[]
    for _ in range(n):
        P=uni([[s:=random.random()*(D-L),s+L] for L in lens]); out.append(f1(P,R,t))
    out.sort(); return st.mean(out), out[int(.95*n)]
res={}
for cond,runs in [('raw',['raw','raw2','raw3']),('stylegen',['stylegen','stylegen2','stylegen3']),('style(leaky)',['style']),('hybrid',['hybrid1','hybrid2','hybrid3']),('tool',['tool1','tool2','tool3'])]:
    rows=[]
    for r in runs:
        c=json.load(open(f'{r}/timeline.json',encoding='utf-8-sig'))['clips']
        P=uni([(x['in'],x['out']) for x in c]); lens=[x['out']-x['in'] for x in c]
        k=keyrec(P)
        rows.append(dict(run=r,dur=round(tot(P)),clips=len(c),f1=f1(P,R),f1_t2=f1(P,R,2),f1_t3=f1(P,R,3),key_hit=k[0],key_n=k[1],rand_mean=rand_f1(lens)[0],rand_p95=rand_f1(lens)[1],loud_f1=f1(loud_baseline(tot(P)),R)))
    res[cond]=rows
for cond,rows in res.items():
    print('==',cond)
    for r in rows: print({k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()})
    for m in ['f1','f1_t2','f1_t3','key_hit']:
        v=[r[m] for r in rows]; print(f'  {m}: mean {st.mean(v):.3f}'+(f' sd {st.stdev(v):.3f}' if len(v)>1 else ''))
# key moments random baseline
lens=[x['out']-x['in'] for x in json.load(open('stylegen/timeline.json',encoding='utf-8-sig'))['clips']]
kr=[keyrec(uni([[s:=random.random()*(D-L),s+L] for L in lens]))[0] for _ in range(500)]
print('key moments total',len(key),'random hits mean',st.mean(kr),'p95',sorted(kr)[475])
lb=loud_baseline(1430); print('loudness baseline f1',round(f1(lb,R),3),'t3',round(f1(lb,R,3),3),'key',keyrec(lb))
json.dump(res,open('eval_results.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
