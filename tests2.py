from geom import *
import random
random.seed(7)
def kind(W,model):
    pts=[]; ar=0
    for pi,P in extended_set(W,model):
        ar+=area(P); pts+=P
    pts=dedup(pts)
    if ar>1e-15: return "region"
    return "point" if len(pts)==1 else "segment"
bad=0
for t in range(3000):
    X,Y=random.choice([(0,1),(0,2),(1,2)]); Z=3-X-Y
    lamXY=F(random.randint(1,6),random.randint(1,6))
    W=[]
    for r in range(3):
        w=[None]*3; w[Y]=F(1); w[X]=lamXY; w[Z]=F(random.randint(1,5),random.randint(1,5)); W.append(tuple(w))
    # exactly one chain: other ratios not all equal
    rat=[w[Z]/w[Y] for w in W]
    if len(set(rat))==1: continue
    for model in ("inc","dis"):
        ext=min(rat) if model=="inc" else max(rat)
        unique = rat.count(ext)==1
        k=kind(W,model)
        exp="segment" if unique else "point"
        if k!=exp: bad+=1; print(W,model,k,exp)
print("chain test mismatches",bad)
# cycle equality configurations: always a point
bad=0;cnt=0
for t in range(4000):
    lam=[F(random.randint(1,9),random.randint(1,9)) for _ in range(6)]
    # agents r,s,t = 0,1,2 ; w=(lamAB*lamBC? ) build w from lamAB, lamBC: w=(lamAB*lamBC, lamBC, 1)
    def mk(ab,bc): return (ab*bc, bc, F(1))
    W=[mk(lam[0],lam[1]),mk(lam[2],lam[3]),mk(lam[4],lam[5])]
    L=[ (w[0]/w[1], w[0]/w[2], w[1]/w[2]) for w in W]
    r,s,tt=0,1,2
    inc = L[r][1]==L[s][0]*L[tt][2] and L[tt][0]>L[s][0]>L[r][0] and L[s][1]<min(L[r][1],L[tt][1])
    dis = L[r][1]==L[s][0]*L[tt][2] and L[tt][0]<L[s][0]<L[r][0] and L[s][1]>max(L[r][1],L[tt][1])
    for model,ok in (("inc",inc),("dis",dis)):
        if ok:
            cnt+=1
            k=kind(W,model)
            pts=dedup(sum([P for _,P in extended_set(W,model)],[]))
            target=(F(1),1/L[s][0],1/L[r][1]); sm=sum(target); target=tuple(x/sm for x in target)
            if k!="point" or pts!=[target]: bad+=1; print("cycle",model,W,k,pts,target)
print("cycle cases",cnt,"mismatches",bad)
