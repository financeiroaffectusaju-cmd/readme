import json
from ortools.sat.python import cp_model
seats={"Psi":2,"TO":2,"Fono":2,"Psped":2,"Psmot":2,"Music":1,"Alim":2}
PK={1:(["Psi","TO","Psped","Psmot"],12),2:(["Psi","Fono","Psped","Alim"],12),3:(["TO","Fono","Psped","Music"],9),
    4:(["Psi","TO","Psmot","Alim"],9),5:(["Psi","Fono","Psmot","Music"],9),6:(["TO","Fono","Psmot","Alim"],9)}
visits=[]
for k,(rooms,n) in PK.items():
    for i in range(n): visits.append((k,rooms))
m=cp_model.CpModel(); iv={r:[] for r in seats}; T={}
for v,(k,rooms) in enumerate(visits):
    S=m.NewIntVarFromDomain(cp_model.Domain.FromIntervals([[0,6],[10,18]]),f"S{v}")
    ts=[]
    for r in rooms:
        t=m.NewIntVar(0,21,f"t{v}{r}"); m.Add(t>=S); m.Add(t<=S+3)
        T[v,r]=t; ts.append(m.NewFixedSizeIntervalVar(t,1,"")); iv[r].append(m.NewFixedSizeIntervalVar(t,1,""))
    m.AddNoOverlap(ts)
for r,l in iv.items(): m.AddCumulative(l,[1]*len(l),seats[r])
# symmetry breaking: visits of same package ordered by start
# (S is not stored; use first-room order is free) -> skip
s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=240; s.parameters.num_workers=8
st=s.Solve(m); print(s.StatusName(st))
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    out=[]
    for v,(k,rooms) in enumerate(visits):
        seq=sorted([(s.Value(T[v,r]),r) for r in rooms])
        out.append({"pkg":k,"seq":seq})
    out.sort(key=lambda x:(x["seq"][0][0],x["pkg"]))
    json.dump(out,open("blocks.json","w"))
    print(len(out), "starts:", sorted({o['seq'][0][0] for o in out}))
