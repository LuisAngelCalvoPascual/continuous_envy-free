from geom import *
from search import third_on_edge, meets_S
import search
def mk(ab,bc): return (ab*bc, bc, F(1))
EX={"inc":[mk(F(5,2),F(1,3)),mk(F(5,2),F(2)),mk(F(2),F(1))],
    "dis":[mk(F(3,2),F(5,2)),mk(F(1,3),F(4,3)),mk(F(1),F(5,2))]}
def fr(x): return f"{x.numerator}/{x.denominator}" if x.denominator!=1 else str(x.numerator)
for model,W in EX.items():
    search.MODEL=model
    print("=====",model)
    for r,w in enumerate(W):
        l=lam(w); P=center(w)
        print(f"agent{r+1} w={[fr(x) for x in w]} lamAB={fr(l[0])} lamAC={fr(l[1])} lamBC={fr(l[2])} P={[fr(x) for x in P]} ~ {[round(float(x),3) for x in P]}")
    opt,vals=optimal_assignments(W,model)
    for pi in PERMS: print(" pi",''.join(ALT[k] for k in pi),fr(vals[pi]),float(vals[pi]))
    pi=opt[0]; print("opt",[''.join(ALT[k] for k in p) for p in opt])
    S=E_pi(W,pi,model); print("S vertices",[[round(float(x),4) for x in p] for p in S], "area",area(S), "rel", area(S)/(3**0.5/4))
    print("S vertices frac",[[fr(x) for x in p] for p in S])
    V,tris,lab=sperner_labels(W,10,model); FL=fully_labelled(tris,lab)
    print("#FL",len(FL))
    for t in FL:
        print(" FL",[ (v, [fr(x) for x in V[v]], 'agent%d'%(owner(v)+1), ALT[lab[v]]) for v in t], "meets closure?", bool(E_pi(W,pi,model,poly=[V[v] for v in t])))
        e=third_on_edge(W,V,t,lab); print("  third:",e[0],e[1],[fr(x) for x in e[2]],'agent%d'%(e[3]+1),'prefers',ALT[e[4]])
    ms=[t for t in tris if meets_S(W,pi,model,[V[v] for v in t])]
    print("#tri meeting S",len(ms),"of which FL",sum(t in FL for t in ms))
    print(" queries", (11*12)//2, "corners fixed ->", 66-3)
