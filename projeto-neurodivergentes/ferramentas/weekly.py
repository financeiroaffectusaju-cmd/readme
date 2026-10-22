import itertools, sys, numpy as np
sys.path.insert(0,'.')
from scipy.optimize import milp, LinearConstraint, Bounds
from lp import S, big, seats, H
from ortools.sat.python import cp_model
DAYS=246
def pk(onlybig):
    P=[]
    for sub in itertools.combinations(S,4):
        if len(big&set(sub))<2: continue
        for hh in itertools.combinations(sub,2):
            if onlybig and any(x not in big for x in hh): continue
            P.append((sub,hh))
    return P
def lp(onlybig,occ=1.0):
    P=pk(onlybig); A=np.zeros((len(S),len(P)))
    for j,(sub,hh) in enumerate(P):
        for i,s in enumerate(S):
            if s in sub: A[i,j]=(1.0 if s in hh else 0.5)*48
    cap=np.array([seats[s]*H*DAYS*occ for s in S])
    r=milp(c=-np.ones(len(P)),constraints=LinearConstraint(A,-np.inf,cap),integrality=np.ones(len(P)),bounds=Bounds(0,np.inf))
    x=np.round(r.x).astype(int); return x.sum(),[(P[j],x[j]) for j in range(len(P)) if x[j]>0]
def feasible(visits,tl=90):
    m=cp_model.CpModel(); iv={r:[] for r in seats}
    for v,rooms in enumerate(visits):
        L=sum(d for _,d in rooms)
        Sv=m.NewIntVarFromDomain(cp_model.Domain.FromIntervals([[0,10-L],[10,22-L]]),f"S{v}")
        ts=[]
        for k,(r,d) in enumerate(rooms):
            t=m.NewIntVar(0,21,""); m.Add(t>=Sv); m.Add(t+d<=Sv+L)
            ts.append(m.NewFixedSizeIntervalVar(t,d,"")); iv[r].append(m.NewFixedSizeIntervalVar(t,d,""))
        m.AddNoOverlap(ts)
    for r,l in iv.items(): m.AddCumulative(l,[1]*len(l),seats[r])
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=8
    return s.StatusName(s.Solve(m))
for onlybig in (False,True):
    tot,mix=lp(onlybig)
    print("1h livre" if not onlybig else "1h so em Psi/TO/Fono","teto criancas",tot,"visitas/dia(teto)=%.1f"%(tot*48/DAYS))
    for (sub,hh),n in mix: print("   ",sub,"1h:",hh,n)
    if not onlybig:
        for f in (0.80,0.85,0.90):
            vis=[]
            for (sub,hh),n in mix:
                k=round(f*n*48/DAYS)
                vis+= [tuple((s,2 if s in hh else 1) for s in sub)]*k
            print("  fator",f,"visitas/dia",len(vis),"->",feasible(vis))
