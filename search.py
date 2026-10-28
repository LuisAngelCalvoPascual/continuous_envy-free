from geom import *
import random, itertools
NICE=[F(1,3),F(1,2),F(2,3),F(3,4),F(1),F(4,3),F(3,2),F(2),F(5,2),F(3)]
def mk(ab,bc): return (ab*bc, bc, F(1))
def tri_pts(V,t): return [V[v] for v in t]
def disjoint_from(W,pi,model,tri):
    return E_pi(W,pi,model,poly=tri)==[]
def meets_S(W,pi,model,tri):
    return area(E_pi(W,pi,model,poly=tri))>1e-15
def third_on_edge(W,V,t,lab):
    # edge between labels X,Y: exists point & agent strictly preferring Z
    for a_,b_ in ((0,1),(1,2),(0,2)):
        u,v=t[a_],t[b_]; Z=({0,1,2}-{lab[u],lab[v]}).pop()
        for k in range(1,40):
            s=F(k,40); p=tuple(V[u][q]*(1-s)+V[v][q]*s for q in range(3))
            for r in range(3):
                if preferred(W[r],p,MODEL)=={Z}: return (u,v,p,r,Z)
    return None
random.seed(11)
res=[]
for MODEL in ("inc","dis"):
    found=[]
    for trial in range(20000):
        W=[mk(random.choice(NICE),random.choice(NICE)) for _ in range(3)]
        opt,_=optimal_assignments(W,MODEL)
        if len(opt)!=1: continue
        pi=opt[0]; S=E_pi(W,pi,MODEL); A=area(S)
        if A<0.004: continue
        V,tris,lab=sperner_labels(W,10,MODEL)
        FL=fully_labelled(tris,lab)
        if MODEL=="dis" and len(FL)!=1: continue
        if MODEL=="inc" and len(FL)>3: continue
        dis_fl=[t for t in FL if disjoint_from(W,pi,MODEL,tri_pts(V,t))]
        if not dis_fl: continue
        if MODEL=="dis" and len(dis_fl)!=1: continue
        edge=None
        for t in dis_fl:
            edge=third_on_edge(W,V,t,lab)
            if edge: break
        if not edge: continue
        notfl=[t for t in tris if meets_S(W,pi,MODEL,tri_pts(V,t)) and t not in FL]
        if not notfl: continue
        found.append((A,len(FL),W,pi,t,edge))
        if len(found)>=15: break
    found.sort(key=lambda z:(z[1],-z[0]))
    print(MODEL,len(found))
    for f in found[:6]:
        A,n,W,pi,t,edge=f
        print(" area %.4f FL %d"%(A,n),[ (str(lam(w)[0]),str(lam(w)[2])) for w in W],pi,t)
