import json
from ortools.sat.python import cp_model
B=json.load(open("blocks.json"))
def mins(s): return 7*60+30*s if s<10 else 13*60+30*(s-10)
HRS=[7,8,9,10,11,13,14,15,16,17,18]
def run(nvis,cap_x=6,cap_c=10):
    vs=B[:]  # use all blocks; for 54 drop 6 (free) evenly
    if nvis<60:
        step=60/(60-nvis); drop={int(i*step) for i in range(60-nvis)}; vs=[b for i,b in enumerate(B) if i not in drop]
    m=cp_model.CpModel(); X={}; C={}; cost=[]
    for i,b in enumerate(vs):
        st=mins(b["seq"][0][0]); en=st+120; morning=b["seq"][0][0]<10
        opts=[]
        for typ in ("X","C"):
            for H in HRS:
                if (H<12)!=morning: continue
                if H*60>=en or (H+1)*60<=st:
                    v=m.NewBoolVar(f"{i}{typ}{H}"); X[(i,typ,H)]=v; opts.append(v)
                    gap=(H*60-en) if H*60>=en else (st-(H+1)*60)
                    cost.append(gap*v)
        m.AddExactlyOne(opts)
    for H in HRS:
        m.Add(sum(v for (i,t,h),v in X.items() if t=="X" and h==H)<=cap_x)
        m.Add(sum(v for (i,t,h),v in X.items() if t=="C" and h==H)<=cap_c)
    nx=sum(v for (i,t,h),v in X.items() if t=="X"); nc=sum(v for (i,t,h),v in X.items() if t=="C")
    m.Add(nx-nc<=4); m.Add(nc-nx<=4)
    m.Minimize(sum(cost))
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=60; s.parameters.num_workers=8
    st=s.Solve(m); print(nvis,s.StatusName(st))
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        gaps=[]; asg={}
        for (i,t,h),v in X.items():
            if s.Value(v):
                b=vs[i]; stt=mins(b["seq"][0][0]); en=stt+120
                gaps.append((h*60-en) if h*60>=en else (stt-(h+1)*60)); asg[i]=(t,h)
        print("  espera media %.0f min, max %d min; X=%d C=%d"%(sum(gaps)/len(gaps),max(gaps),sum(1 for t,h in asg.values() if t=='X'),sum(1 for t,h in asg.values() if t=='C')))
        return vs,asg
if __name__=="__main__":
    run(54); run(60)
