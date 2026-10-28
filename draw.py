import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from geom import *

COL = ["#d62728", "#2ca02c", "#1f77b4"]  # agents 1,2,3
H = math.sqrt(3) / 2
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 9})


def base(ax, fill="#ececec"):
    ax.add_patch(Polygon([(0, 0), (1, 0), (0.5, H)], closed=True, fc=fill, ec="black", lw=1.1, zorder=0))
    for (x, y), s, dx, dy in (((0, 0), "A", -0.045, -0.04), ((1, 0), "B", 0.02, -0.04), ((0.5, H), "C", -0.012, 0.025)):
        ax.plot(x, y, "ko", ms=3, zorder=6)
        ax.text(x + dx, y + dy, s, fontsize=10)
    ax.set_xlim(-0.07, 1.07)
    ax.set_ylim(-0.08, H + 0.07)
    ax.set_aspect("equal")
    ax.axis("off")


def seg(ax, p, q, **kw):
    (x1, y1), (x2, y2) = cart(p), cart(q)
    ax.plot([x1, x2], [y1, y2], **kw)


def partition(ax, W, model, lw=1.3, centers=True, agents=(0, 1, 2)):
    for r in agents:
        for P, e in boundary_segments(W[r], model):
            seg(ax, P, e, color=COL[r], lw=lw, zorder=3, solid_capstyle="round")
        if centers:
            x, y = cart(center(W[r]))
            ax.plot(x, y, "o", color=COL[r], ms=4.5, mec="black", mew=0.5, zorder=5)


def solution(ax, W, model, fc="#8c8c8c"):
    for pi, P in extended_set(W, model):
        if area(P) > 1e-15:
            ax.add_patch(Polygon([cart(p) for p in P], closed=True, fc=fc, ec="black", lw=0.6, zorder=2, alpha=0.9))
        elif len(P) == 2:
            seg(ax, P[0], P[1], color="black", lw=3.0, zorder=4)
        else:
            x, y = cart(P[0])
            ax.plot(x, y, "o", ms=9, mfc="none", mec="black", mew=1.4, zorder=6)


def sperner(ax, W, m, model, show_labels=True, fl_fc="#f6c75a", vsize=5.5):
    V, tris, lab = sperner_labels(W, m, model)
    FL = fully_labelled(tris, lab)
    for t in tris:
        pts = [cart(V[v]) for v in t]
        ax.add_patch(Polygon(pts, closed=True, fc=fl_fc if t in FL else "none",
                             ec="#555555", lw=0.45, zorder=1, alpha=0.95 if t in FL else 1))
    for ij, p in V.items():
        x, y = cart(p)
        ax.plot(x, y, "o", color=COL[owner(ij)], ms=vsize, mec="white", mew=0.4, zorder=7)
        if show_labels:
            ax.text(x, y, ALT[lab[ij]], fontsize=3.6, color="white", ha="center", va="center",
                    zorder=8, fontweight="bold")
    return V, tris, lab, FL


def legend_agents(ax, loc="upper right"):
    for r in range(3):
        ax.plot([], [], "-", color=COL[r], lw=1.5, label=f"agent {r+1}")
    ax.legend(loc=loc, fontsize=7, frameon=False, handlelength=1.5)
