import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
S = ["Psi","TO","Fono","Psped","Psmot","Music","Alim"]
big = {"Psi","TO","Fono"}
seats = {"Psi":2,"TO":2,"Fono":2,"Psped":2,"Psmot":2,"Music":1,"Alim":2}
H = 11
def pkgs(fmt, only_big_hour=False):
    out=[]
    if fmt in("A","C4"): n=4
    else: n=3
    for sub in itertools.combinations(S,n):
        if len(big & set(sub))<2: continue
        if fmt=="C4": out.append((fmt,sub,{s:0.5 for s in sub},6))
        elif fmt=="C3": out.append((fmt,sub,{s:0.5 for s in sub},8))
        elif fmt=="A":
            for one in sub:
                if only_big_hour and one not in big: continue
                out.append((fmt,sub+("1h:"+one,),{s:(1.0 if s==one else 0.5) for s in sub},6))
        elif fmt=="B":
            for half in sub:
                if only_big_hour and any(s not in big and s!=half for s in sub if False): pass
                out.append((fmt,sub+("30m:"+half,),{s:(0.5 if s==half else 1.0) for s in sub},8))
    return out
def solve(fmts, days, occ=1.0, only_big_hour=False, label=""):
    P=[]
    for f in fmts: P+=pkgs(f, only_big_hour)
    # hours/year per spec per child = visits/month*12*dur
    A=np.zeros((len(S),len(P)))
    for j,(f,sub,dur,vm) in enumerate(P):
        for i,s in enumerate(S):
            A[i,j]=dur.get(s,0)*vm*12
    cap=np.array([seats[s]*H*days*occ for s in S])
    res=milp(c=-np.ones(len(P)),constraints=LinearConstraint(A,-np.inf,cap),integrality=np.ones(len(P)),bounds=Bounds(0,np.inf))
    x=np.round(res.x).astype(int)
    tot=x.sum()
    use=A@x
    return tot,{S[i]:round(use[i]/cap[i]*100) for i in range(len(S))},[(P[j][0],P[j][1],x[j]) for j in range(len(P)) if x[j]>0]
if __name__=="__main__":
    for days in (253,):
        print("DIAS",days)
        for occ in (1.0,0.85):
            print(" ocupacao",occ)
            for name,f,ob in [("A (1h livre)",["A"],False),("A (1h so em Psi/TO/Fono)",["A"],True),("B",["B"],False),("C4 (4x30)",["C4"],False),("C3 (3x30)",["C3"],False),("mix C4+C3",["C4","C3"],False),("mix A+B livre",["A","B"],False),("mix tudo",["A","B","C4","C3"],False)]:
                tot,u,mix=solve(f,days,occ,ob)
                print(f"   {name:28s} criancas={tot:4d}  uso%={u}")
