#!/usr/bin/env python3
"""MATH-06P canonical certificate generator (exact integer arithmetic only).

Mathematical content
--------------------
G_l(q)  = [l+8 choose 8]_q = prod_{i=1..8} (1 - q^(l+i)) / (1 - q^i)
F_l(q)  = G_l(q) - q^(4l-18) * B(q),      B(q) = [12 choose 6]_q
a_l(n)  = [q^n] G_l(q),   b_j = [q^j] B(q)   (both zero outside their support)

Reduction (proved in proof/coefficient-reduction.md): for l >= 6, F_l is unimodal iff
    D_a_l(4l-18+j) >= Db_j   for j = -1, 0, ..., 17,
where D_a_l(d) = a_l(d+1) - a_l(d) and Db_j = b_{j+1} - b_j (b-indices relative to the
shifted window). Db is DERIVED here from the definition of B; it is never read from a table.

Infinite step (proof/quasipolynomial-certificate.md): with
    p8(n) = [q^n] prod_{i=1..8} (1 - q^i)^{-1},  p8(n) = 0 for n < 0,
p8 is a quasipolynomial in n of degree <= 7 and period dividing 840 = lcm(1..8), valid for
EVERY n >= 0, and inclusion-exclusion over the numerator gives
    a_l(n) = sum_{S subseteq {1..8}} (-1)^|S| p8(n - |S| l - sigma(S)).
For l >= 840 and c = -18+j with j <= 17 every subset of size >= 4 contributes 0, so for each
residue class r (mod 840) the margin
    Q_{j,r}(t) = D_a_l(4l-18+j) - Db_j,   l = r + 840(t+1),
is a polynomial in t of degree <= 7 (in fact <= 5, which the certificate also tests).

Certificate: Newton's expansion at t = 0,
    Q(t) = sum_{i=0..7} binom(t,i) * Delta^i Q(0),      binom(t,i) >= 0 for integer t >= 0,
so nonnegativity of the eight forward differences Delta^i Q(0) proves Q(t) >= 0 for all t >= 0.
Combined with an exact finite check for 6 <= l <= 839 this covers every l >= 6 with no gap.

Usage:  python3 generate_certificate.py [--out certificate.json]
Exit 0 on success. Standard library only.
"""
import argparse
import json
import platform
import sys
from math import comb

PERIOD = 840
OFFSETS = list(range(-1, 18))          # j = -1..17  (19 obligations per residue class)
T_POINTS = 9                           # t = 0..8: 8 determine the polynomial, 1 degree self-test
TAIL_START = PERIOD                    # certificate applies for l >= 840
FINITE_LO, FINITE_HI = 6, PERIOD - 1   # exact finite range


# ---------------------------------------------------------------- definitions
def qbinom_coeffs(n, k):
    """[q^*] [n choose k]_q from the product definition, exact ints, dense list."""
    num = {0: 1}
    for i in range(1, k + 1):                      # numerator prod (1 - q^(n-k+i))
        d = n - k + i
        new = {}
        for e, c in num.items():
            new[e] = new.get(e, 0) + c
            new[e + d] = new.get(e + d, 0) - c
        num = new
    pol = {e: c for e, c in num.items() if c}
    for i in range(1, k + 1):                      # multiply by 1/(1-q^i): step-i prefix sums
        mx = max(pol)
        out = {}
        for e in range(mx + i + 1):
            v = pol.get(e, 0) + (out.get(e - i, 0) if e - i >= 0 else 0)
            if v:
                out[e] = v
        pol = out
    deg = max(pol)
    return [pol.get(e, 0) for e in range(deg + 1)]


def subset_terms(k=8):
    """Inclusion-exclusion terms: (|S|, sigma(S)) -> signed multiplicity, by enumeration."""
    terms = {}
    subsets = [()]
    for i in range(1, k + 1):
        subsets += [s + (i,) for s in subsets]
    for s in subsets:
        key = (len(s), sum(s))
        terms[key] = terms.get(key, 0) + (-1) ** len(s)
    return sorted(terms.items())


# ---------------------------------------------------------------- p8 and margins
def build_p8(nmax):
    """p8(n) = [q^n] prod_{i=1..8}(1-q^i)^{-1} by DP over part sizes; exact ints."""
    p = [0] * (nmax + 2)
    p[0] = 1
    for part in range(1, 9):
        for n in range(part, nmax + 1):
            p[n] += p[n - part]
    return p


def newton_coeffs(vals):
    """Delta^i Q(0) for i = 0..len(vals)-1 from values at t = 0..len-1."""
    v = list(vals)
    out = [v[0]]
    for _ in range(len(vals) - 1):
        v = [v[i + 1] - v[i] for i in range(len(v) - 1)]
        out.append(v[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="certificate.json")
    args = ap.parse_args()

    B = qbinom_coeffs(12, 6)                       # b_j for j = 0..36, else 0
    bget = lambda j: B[j] if 0 <= j < len(B) else 0
    Db = {j: bget(j + 1) - bget(j) for j in OFFSETS}   # derived, not copied

    lmax = (FINITE_HI) + PERIOD * T_POINTS
    nmax = 4 * lmax + 40
    p8 = build_p8(nmax)
    Dp = [p8[n + 1] - p8[n] for n in range(nmax + 1)]
    terms = subset_terms()

    def delta_a(l, c):
        """a_l(4l+c+1) - a_l(4l+c) exactly, via inclusion-exclusion."""
        tot = 0
        for (k, sig), ch in terms:
            m = 4 - k
            x = m * l + c - sig
            if x >= 0:
                tot += ch * Dp[x]
            else:
                # p8(x)=0 for x<0, so D(x) = p8(x+1)-p8(x) = 1 only at x = -1
                if x == -1:
                    tot += ch
        return tot

    obligations = 19 * PERIOD
    records = []
    neg = 0
    deg_top_nonzero = 0
    min_tail = None
    for j in OFFSETS:
        c = -18 + j
        for r in range(PERIOD):
            vals = [delta_a(r + PERIOD * (t + 1), c) - Db[j] for t in range(T_POINTS)]
            nc = newton_coeffs(vals[:8])          # certificate uses 8 points (degree <= 7)
            # 9th point (t = 8) predicts from the 8-point Newton interpolant: degree test
            assert vals[8] == sum(
                nc[i] * comb(8, i) for i in range(8)
            ), f"Newton expansion failed at j={j} r={r}"
            if any(x < 0 for x in nc):
                neg += 1
            if nc[6] != 0 or nc[7] != 0:
                deg_top_nonzero += 1
            if min_tail is None or nc[0] < min_tail:
                min_tail = nc[0]
            records.append({"j": j, "r": r, "newton": nc})

    # exact finite base, same exact machinery, direct margins
    fin_min = None
    fin_at = None
    for l in range(FINITE_LO, FINITE_HI + 1):
        for j in OFFSETS:
            m = delta_a(l, -18 + j) - Db[j]
            if fin_min is None or m < fin_min:
                fin_min, fin_at = m, (l, j)

    out = {
        "schema": "m06p.certificate.v1",
        "polynomial": "F_l(q) = [l+8 choose 8]_q - q^(4l-18) [12 choose 6]_q",
        "period": PERIOD,
        "offsets": [OFFSETS[0], OFFSETS[-1]],
        "Db_derived": [Db[j] for j in OFFSETS],
        "degree_bound": 7,
        "points_per_class": 8,
        "tail_start": TAIL_START,
        "finite_range": [FINITE_LO, FINITE_HI],
        "obligations": obligations,
        "negative_newton_classes": neg,
        "classes_with_degree_7_or_6": deg_top_nonzero,
        "min_tail_margin_Q0": min_tail,
        "finite_min_margin": fin_min,
        "finite_min_at": list(fin_at),
        "runtime": {"python": platform.python_version(), "stdlib_only": True},
        "records": records,
    }
    with open(args.out, "w") as fh:
        json.dump(out, fh, separators=(",", ":"))
    print(f"certificate written: {args.out}")
    print(f"obligations={obligations} negative_newton_classes={neg} "
          f"classes_with_degree>5={deg_top_nonzero}")
    print(f"min_tail_Q0={min_tail} finite_min_margin={fin_min} at (l,j)={fin_at}")
    print(f"Db_derived={out['Db_derived']}")
    return 0 if neg == 0 and fin_min >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
