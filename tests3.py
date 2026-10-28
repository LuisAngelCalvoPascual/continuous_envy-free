from geom import *
import random
from tests2 import kind
random.seed(3)
def mk(ab,bc): return (ab*bc, bc, F(1))
bad=cnt=0
for t in range(600):
    for model in ("inc","dis"):
        a=sorted(F(random.randint(1,30),random.randint(1,10)) for _ in range(3))
        a=list(dict.fromkeys(a))
        if len(a)<3: continue
        if model=="inc": rAB,sAB,tAB=a
        else: tAB,sAB,rAB=a
        tBC=F(random.randint(1,20),random.randint(1,10))
        rAC=sAB*tBC; rBC=rAC/rAB; tAC=tAB*tBC
        if model=="inc":
            bound=min(rAC,tAC); sAC=bound*F(random.randint(1,9),10)
        else:
            bound=max(rAC,tAC); sAC=bound*F(random.randint(11,40),10)
        sBC=sAC/sAB
        W=[mk(rAB,rBC),mk(sAB,sBC),mk(tAB,tBC)]
        cnt+=1
        pts=dedup(sum([P for _,P in extended_set(W,model)],[]))
        target=(F(1),1/sAB,1/rAC); sm=sum(target); target=tuple(x/sm for x in target)
        if kind(W,model)!="point" or pts!=[target]: bad+=1; print(model,W,pts)
print(cnt,"cycle configs, mismatches",bad)
