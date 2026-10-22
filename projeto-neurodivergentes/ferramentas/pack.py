import sys, math
from ortools.sat.python import cp_model
sys.path.insert(0,'.')
from lp import solve, seats
DAYS=253; DAYS_MONTH=DAYS/12
def feasible(visits, tl=60, seed=0):
    """visits: list of tuples of (room, dur_slots) ; all consecutive, one period."""
    m=cp_model.CpModel()
    iv={r:[] for r in seats}
    for v,rooms in enumerate(visits):
        L=sum(d for _,d in rooms)
        S=m.NewIntVarFromDomain(cp_model.Domain.FromIntervals([[0,9-L+1],[10,21-L+1]]),f"S{v}")
        starts=[]
        for k,(r,d) in enumerate(rooms):
            t=m.NewIntVar(0,21,f"t{v}_{k}")
            m.Add(t>=S); m.Add(t+d<=S+L)
            iv[r].append((m.NewFixedSizeIntervalVar(t,d,f"i{v}_{k}")))
            starts.append((t,d))
        # sessions of one visit must tile [S,S+L) without overlap -> no-overlap suffices given total length L
        m.AddNoOverlap([m.NewFixedSizeIntervalVar(t,d,"") for t,d in starts])
    for r,ints in iv.items():
        m.AddCumulative(ints,[1]*len(ints),seats[r])
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=8; s.parameters.random_seed=seed
    st=s.Solve(m)
    return s.StatusName(st)
if __name__=="__main__":
    tot,u,mix=solve(["C4"],DAYS,1.0)
    print("children",tot,mix)
    for f in (1.0,0.95,0.90,0.85):
        visits=[]
        for fmt,sub,n in mix:
            k=round(f*n*6/DAYS_MONTH)
            visits += [tuple((s,1) for s in sub)]*k
        # room orders are free: solver decides order via t vars
        print(f"fator {f}: visitas/dia={len(visits)} ->",feasible(visits,tl=90))
