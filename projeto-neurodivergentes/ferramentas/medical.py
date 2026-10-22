from datetime import date, timedelta
from collections import defaultdict, Counter
from ortools.sat.python import cp_model
DOCS=["Neuropediatra","Psiquiatra infantil","Pediatra"]
def hm(m): return f"{m//60:02d}:{m%60:02d}"
def slots(dur):
    out=[]
    for a,b in ((8*60,12*60),(13*60,17*60)):
        t=a
        while t+dur<=b: out.append(t); t+=dur
    return out
def kid_table(ids,blocks):
    """ids[(bloco_idx,dia)] -> código; devolve {código:(dia,ini,fim)} em minutos"""
    out={}
    for (i,d),k in ids.items():
        s=blocks[i]["start"]; h,m=map(int,s.split(":")); ini=h*60+m
        out[k]=(d,ini,ini+120)
    return out
def run_day(kids,seen,cnt,doc,dur):
    """escolhe até len(slots) crianças do dia; devolve [(slot_ini,código)]"""
    S=slots(dur); m=cp_model.CpModel(); x={}; obj=[]
    for k,(d,ini,fim) in kids.items():
        for si,t in enumerate(S):
            if t+dur<=ini or t>=fim:
                gap=ini-(t+dur) if t+dur<=ini else t-fim
                v=m.NewBoolVar(""); x[k,si]=v
                rw=100000-30000*cnt[k]-(60000 if doc in seen[k] else 0)-gap
                obj.append(rw*v)
    for k in kids: m.Add(sum(x[k,si] for si in range(len(S)) if (k,si) in x)<=1)
    for si in range(len(S)): m.Add(sum(x[k,si] for k in kids if (k,si) in x)<=1)
    m.Maximize(sum(obj))
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=20; s.parameters.num_workers=8
    s.Solve(m)
    return sorted((S[si],k) for (k,si),v in x.items() if s.Value(v))
def doctor_dates(holidays):
    res=[]
    months=[(2026,7),(2026,8),(2026,9),(2026,10),(2026,11),(2026,12),(2027,1),(2027,2),(2027,3),(2027,4),(2027,5),(2027,6)]
    for mi,(y,mo) in enumerate(months):
        for di in range(3):
            w=(mi+2*di)%5; c=0; d=date(y,mo,1); occ=[]
            while d.month==mo:
                if d.weekday()==w: occ.append(d)
                d+=timedelta(1)
            pick=occ[1]
            idx=1
            while pick in holidays or pick.weekday()>4:
                idx=(idx+1)%len(occ); pick=occ[idx]
            res.append((pick,w,di))
    res.sort()
    return res
def plan(ids,blocks,holidays,dur=30,extra_months=0):
    kt=kid_table(ids,blocks); byw=defaultdict(dict)
    for k,(d,ini,fim) in kt.items(): byw[d][k]=(d,ini,fim)
    seen={k:set() for k in kt}; cnt=Counter({k:0 for k in kt})
    rows=[]
    for dt,w,di in doctor_dates(holidays):
        res=run_day(byw[w],seen,cnt,DOCS[di],dur)
        for t,k in res:
            seen[k].add(DOCS[di]); cnt[k]+=1; rows.append((dt,DOCS[di],t,k,kt[k]))
    return rows,seen,cnt,kt,byw
def months_to_complete(ids,blocks,dur,maxm=40):
    kt=kid_table(ids,blocks); byw=defaultdict(dict)
    for k,(d,ini,fim) in kt.items(): byw[d][k]=(d,ini,fim)
    seen={k:set() for k in kt}; cnt=Counter({k:0 for k in kt})
    for mi in range(maxm):
        for di in range(3):
            w=(mi+2*di)%5
            for t,k in run_day(byw[w],seen,cnt,DOCS[di],dur):
                seen[k].add(DOCS[di]); cnt[k]+=1
        if all(len(v)==3 for v in seen.values()): return mi+1
    return None
