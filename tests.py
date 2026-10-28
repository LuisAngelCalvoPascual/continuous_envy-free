from geom import *
import random
random.seed(1)
def rw(): return tuple(F(random.randint(1,12),random.randint(1,12)) for _ in range(3))
bad=0; nties=0
for trial in range(1500):
    if trial%3==0:  # force ties sometimes
        base=rw(); W=[base, base, rw()] if trial%2 else [rw(),rw(),rw()]
        W=[tuple(x*random.choice([1,2]) for x in w) for w in W]
    else: W=[rw(),rw(),rw()]
    for model in ("inc","dis"):
        opt,vals=optimal_assignments(W,model)
        for pi in PERMS:
            P=E_pi(W,pi,model)
            strict = area(P)>1e-15
            if strict != (opt==[pi]): bad+=1; print("strict mismatch",W,model,pi)
            if bool(P) != (pi in opt): bad+=1; print("weak mismatch",W,model,pi)
        if len(opt)>1: nties+=1
print("mismatches",bad,"tie cases",nties)
# Sperner odd count check
W=[rw(),rw(),rw()]
for model in ("inc","dis"):
    V,tris,lab=sperner_labels(W,10,model); print(model,"FL count",len(fully_labelled(tris,lab)))
# A1 counterexample
w=(F(1),F(1),F(1)); p=(F(1,5),F(1,5),F(3,5))
print("A1 inc",preferred(w,p,"inc"),"dis",preferred(w,p,"dis"))
# A2 counterexample: lamAB=1 all, lamBC=(2,2,1): w=(1,1,1/lamBC)
W=[(F(1),F(1),F(1,2)),(F(1),F(1),F(1,2)),(F(1),F(1),F(1))]
for pi,P in extended_set(W,"inc"): print("A2",pi,P)
