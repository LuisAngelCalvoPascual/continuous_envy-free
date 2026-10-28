from draw import *
def mk(ab,bc): return (ab*bc, bc, F(1))
def region_letters(ax,w,model):
    for X in range(3):
        P=TRI
        for f in pref_forms(w,X,model): P=clip(P,f)
        pts=[cart(p) for p in P]; cx=sum(x for x,_ in pts)/len(pts); cy=sum(y for _,y in pts)/len(pts)
        ax.text(cx,cy,ALT[X],fontsize=12,ha="center",va="center",color="#333333",fontweight="bold")
def lab_line(ax,p,q,txt,frac=0.55,off=(0,0)):
    (x1,y1),(x2,y2)=cart(p),cart(q); x=x1+frac*(x2-x1)+off[0]; y=y1+frac*(y2-y1)+off[1]
    ax.text(x,y,txt,fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.5,alpha=0.85))

# ---------- Figure 1 ----------
w=mk(F(3,2),F(4,3)); P=center(w)
fig=plt.figure(figsize=(7.2,5.4))
names=[("a = \\lambda_{AB}\\, b",(w[0],w[1],F(0)),(F(0),F(0),F(1)),(0,1)),
       ("a = \\lambda_{AC}\\, c",(w[0],F(0),w[2]),(F(0),F(1),F(0)),(0,2)),
       ("b = \\lambda_{BC}\\, c",(F(0),w[1],w[2]),(F(1),F(0),F(0)),(1,2))]
for k,(txt,e1,e2,(X,Y)) in enumerate(names):
    ax=fig.add_axes([0.02+0.33*k,0.60,0.30,0.38]); base(ax)
    e1=tuple(x/sum(e1) for x in e1)
    seg(ax,e1,e2,color="black",lw=1.3)
    # side letters for the incentive model: side where X beats Y
    for Z,shift in ((X,-0.18),(Y,0.18)):
        pass
    mid=[(e1[q]+e2[q])/2 for q in range(3)]
    for Z in (X,Y):
        v=[F(0)]*3; v[Z]=F(1)
        q=tuple((mid[t]+v[t]*2)/3 for t in range(3))
        x,y=cart(q); ax.text(x,y,ALT[Z],fontsize=10,ha="center",va="center",fontweight="bold",color="#333")
    lab_line(ax,e1,e2,"$"+txt+"$",frac=0.72)
    ax.set_title("(a%d)"%(k+1),fontsize=8,y=-0.08)
for k,(model,ttl) in enumerate((("inc","(b) incentive model"),("dis","(c) disincentive model"))):
    ax=fig.add_axes([0.08+0.46*k,0.02,0.40,0.52]); base(ax)
    partition(ax,[w],model,agents=(0,),lw=1.6); region_letters(ax,w,model)
    ax.set_title(ttl,fontsize=9,y=-0.07)
fig.savefig("figs/fig1.pdf"); plt.close(fig)

def panel_grid(fname,panels,ncol=2,size=(7.0,6.4)):
    nrow=(len(panels)+ncol-1)//ncol
    fig,axs=plt.subplots(nrow,ncol,figsize=size)
    for ax,(W,model,ttl) in zip(axs.flat,panels):
        base(ax)
        for r,lw in zip(range(3),(3.0,1.8,0.9)):
            for Pp,e in boundary_segments(W[r],model): seg(ax,Pp,e,color=COL[r],lw=lw,zorder=3,solid_capstyle="round")
        for r,ms in zip(range(3),(8,6,4)):
            x,y=cart(center(W[r])); ax.plot(x,y,"o",color=COL[r],ms=ms,mec="black",mew=0.5,zorder=5)
        solution(ax,W,model)
        ax.set_title(ttl,fontsize=9,y=-0.06)
    fig.tight_layout(); fig.savefig(fname); plt.close(fig)

# ---------- Figure 3 ----------
W3=[mk(F(1),F(3)),mk(F(1),F(2)),mk(F(1),F(1))]
Wc=[mk(F(1),F(1))]*3
panel_grid("figs/fig3.pdf",[(W3,"inc","(a) incentive: segment"),(W3,"dis","(b) disincentive: segment"),
                           (Wc,"inc","(c) incentive: common centre"),(Wc,"dis","(d) disincentive: common centre")])
# ---------- Figure 4 ----------
W4si=[mk(F(4,3),F(3,2))]*2+[mk(F(3),F(1,2))]
W4sd=[mk(F(5,2),F(1))]*2+[mk(F(1,2),F(3,4))]
W4pi=[mk(F(1,2),F(1,2))]*2+[mk(F(2,3),F(1,2))]
W4pd=[mk(F(1,2),F(1,2))]*2+[mk(F(1,2),F(2,3))]
panel_grid("figs/fig4.pdf",[(W4si,"inc","(a) incentive: segment"),(W4sd,"dis","(b) disincentive: segment"),
                           (W4pi,"inc","(c) incentive: point"),(W4pd,"dis","(d) disincentive: point")])
# ---------- Figure 5 ----------
E1i=[mk(F(4,3),F(3,4)),mk(F(4,3),F(2,3)),mk(F(1,2),F(5,2))]
E1d=[mk(F(1,2),F(4,3)),mk(F(1,2),F(5,2)),mk(F(4,3),F(1,2))]
E2i=[mk(F(1,2),F(3,2)),mk(F(1,2),F(1,2)),mk(F(5,2),F(3))]
E2d=[mk(F(3),F(1)),mk(F(3),F(3,2)),mk(F(1),F(1))]
panel_grid("figs/fig5.pdf",[(E1i,"inc","(a) E1, incentive"),(E1d,"dis","(b) E1, disincentive"),
                           (E2i,"inc","(c) E2, incentive"),(E2d,"dis","(d) E2, disincentive")])
# ---------- Figure 6 ----------
C6i=[mk(F(1),F(2)),mk(F(2),F(1,4)),mk(F(3),F(1))]
C6d=[mk(F(3),F(2,3)),mk(F(2),F(4)),mk(F(1),F(1))]
panel_grid("figs/fig6.pdf",[(C6i,"inc","(a) incentive model"),(C6d,"dis","(b) disincentive model")],size=(7.0,3.3))

# ---------- Figures 7, 8: worked examples ----------
EX={"inc":[mk(F(5,2),F(1,3)),mk(F(5,2),F(2)),mk(F(2),F(1))],
    "dis":[mk(F(3,2),F(5,2)),mk(F(1,3),F(4,3)),mk(F(1),F(5,2))]}
for model,fname in (("inc","figs/fig7.pdf"),("dis","figs/fig8.pdf")):
    W=EX[model]
    fig=plt.figure(figsize=(7.2,7.0))
    ax1=fig.add_axes([0.0,0.50,0.5,0.48]); ax2=fig.add_axes([0.5,0.50,0.5,0.48]); ax3=fig.add_axes([0.17,0.04,0.66,0.46])
    base(ax1); sperner(ax1,W,10,model,vsize=5.2); ax1.set_title("(a) Sperner discretization, $m=10$",fontsize=9,y=-0.05)
    base(ax2); partition(ax2,W,model); solution(ax2,W,model); legend_agents(ax2); ax2.set_title("(b) exact region",fontsize=9,y=-0.05)
    base(ax3); sperner(ax3,W,10,model,vsize=7.0); partition(ax3,W,model,lw=1.1); solution(ax3,W,model)
    ax3.set_title("(c) overlay",fontsize=9,y=-0.06)
    fig.savefig(fname); plt.close(fig)
print("ok")
