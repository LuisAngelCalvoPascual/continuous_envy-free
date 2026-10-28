"""Exact (rational) geometry for the three-agent reciprocal-threshold model.

Barycentric points are tuples (a, b, c) of Fractions with a + b + c = 1.
An agent is given by a priority vector w = (wA, wB, wC) of positive Fractions.
"""
from fractions import Fraction as F
from itertools import permutations
import math

ALT = "ABC"
PERMS = list(permutations(range(3)))  # pi[r] = alternative index assigned to agent r


def lam(w):
    """Return (lambda_AB, lambda_AC, lambda_BC)."""
    return (w[0] / w[1], w[0] / w[2], w[1] / w[2])


def center(w):
    s = sum(w)
    return tuple(x / s for x in w)


def scores(w, p):
    return tuple(p[k] / w[k] for k in range(3))


def preferred(w, p, model):
    """Set of (weakly) preferred alternatives of agent w at p."""
    s = scores(w, p)
    best = max(s) if model == "inc" else min(s)
    return {k for k in range(3) if s[k] == best}


def Phi(W, pi):
    return W[0][pi[0]] * W[1][pi[1]] * W[2][pi[2]]


def optimal_assignments(W, model):
    vals = {pi: Phi(W, pi) for pi in PERMS}
    best = min(vals.values()) if model == "inc" else max(vals.values())
    return [pi for pi in PERMS if vals[pi] == best], vals


# ---------- exact polygon clipping in barycentric coordinates ----------

def clip(poly, f):
    """Keep the part of convex polygon `poly` where linear form f(p) >= 0."""
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        fp, fq = f(P), f(Q)
        if fp >= 0:
            out.append(P)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq)
            out.append(tuple(P[k] + t * (Q[k] - P[k]) for k in range(3)))
    # remove duplicates while keeping order
    res = []
    for p in out:
        if not res or p != res[-1]:
            res.append(p)
    if len(res) > 1 and res[0] == res[-1]:
        res.pop()
    return res


TRI = [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))]


def pref_forms(w, X, model):
    """Linear forms f >= 0 meaning agent w weakly prefers alternative X."""
    forms = []
    for Y in range(3):
        if Y == X:
            continue
        if model == "inc":   # p_X/w_X - p_Y/w_Y >= 0
            forms.append(lambda p, X=X, Y=Y: p[X] / w[X] - p[Y] / w[Y])
        else:                # p_Y/w_Y - p_X/w_X >= 0
            forms.append(lambda p, X=X, Y=Y: p[Y] / w[Y] - p[X] / w[X])
    return forms


def E_pi(W, pi, model, poly=None):
    poly = list(TRI if poly is None else poly)
    for r in range(3):
        for f in pref_forms(W[r], pi[r], model):
            poly = clip(poly, f)
            if not poly:
                return []
    return dedup(poly)


def dedup(poly):
    res = []
    for p in poly:
        if p not in res:
            res.append(p)
    return res


def cart(p):
    a, b, c = (float(x) for x in p)
    return (b + 0.5 * c, (math.sqrt(3) / 2) * c)


def area(poly):
    if len(poly) < 3:
        return 0.0
    pts = [cart(p) for p in poly]
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def extended_set(W, model):
    """Return list of (pi, polygon) for all nonempty E_pi."""
    res = []
    for pi in PERMS:
        P = E_pi(W, pi, model)
        if P:
            res.append((pi, P))
    return res


def boundary_segments(w, model):
    """Segments (in barycentric coords) forming the preference partition of agent w."""
    P = center(w)
    if model == "inc":
        ends = [(w[0], w[1], F(0)), (w[0], F(0), w[2]), (F(0), w[1], w[2])]
        ends = [tuple(x / sum(e) for x in e) for e in ends]
    else:
        ends = [(F(0), F(0), F(1)), (F(0), F(1), F(0)), (F(1), F(0), F(0))]
    return [(P, e) for e in ends]


# ---------- Sperner discretisation ----------

def mesh(m):
    V = {}
    for i in range(m + 1):
        for j in range(m + 1 - i):
            V[(i, j)] = (F(m - i - j, m), F(i, m), F(j, m))
    tris = []
    for i in range(m):
        for j in range(m - i):
            tris.append(((i, j), (i + 1, j), (i, j + 1)))
            if i + j + 1 < m:
                tris.append(((i + 1, j), (i, j + 1), (i + 1, j + 1)))
    return V, tris


def owner(ij):
    i, j = ij
    return (i + 2 * j) % 3


def sperner_labels(W, m, model, tau=(1, 2, 0)):
    """Label each vertex by an alternative preferred by its owner.
    Disincentive corners use the derangement tau (A->B, B->C, C->A by default)."""
    V, tris = mesh(m)
    lab = {}
    for ij, p in V.items():
        if model == "dis" and p.count(F(0)) == 2:
            corner = p.index(F(1))
            lab[ij] = tau[corner]
            assert tau[corner] in preferred(W[owner(ij)], p, model)
        else:
            lab[ij] = min(preferred(W[owner(ij)], p, model))
    return V, tris, lab


def fully_labelled(tris, lab):
    return [t for t in tris if {lab[v] for v in t} == {0, 1, 2}]
