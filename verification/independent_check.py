#!/usr/bin/env python3
"""MATH-06P independent check: verifies the theorem statements directly from the
definition of the Gaussian polynomial, WITHOUT the quasipolynomial/certificate machinery.
Exact integer arithmetic only. Exit != 0 on any failure.

Checks
  1. sanity of the Gaussian routine: sum of coefficients = ordinary binomial, degree, endpoints
  2. F_5, F_6, F_7 computed completely: nonnegativity, symmetry centre, unimodality status
  3. direct full-polynomial unimodality for every l in 6..N (default 80)
  4. direct test for a large-l sample (default 839,840,841,1000,1680,2520)
  5. equivalence between direct unimodality and the 19 fixed-offset inequalities, l=5..60,
     with the offset constants derived here (not copied)

Usage: python3 independent_check.py [--n 80]
"""
import argparse
import sys
from math import comb


def qbinom_coeffs(n, k):
    num = {0: 1}
    for i in range(1, k + 1):
        d = n - k + i
        new = {}
        for e, c in num.items():
            new[e] = new.get(e, 0) + c
            new[e + d] = new.get(e + d, 0) - c
        num = new
    pol = {e: c for e, c in num.items() if c}
    for i in range(1, k + 1):
        mx = max(pol)
        out = {}
        for e in range(mx + i + 1):
            v = pol.get(e, 0) + (out.get(e - i, 0) if e - i >= 0 else 0)
            if v:
                out[e] = v
        pol = out
    deg = max(pol)
    return [pol.get(e, 0) for e in range(deg + 1)]


OFFSETS = list(range(-1, 18))
B = qbinom_coeffs(12, 6)
bget = lambda j: B[j] if 0 <= j < len(B) else 0
Db = {j: bget(j + 1) - bget(j) for j in OFFSETS}


def F_coeffs(l):
    """Coefficients of F_l = [l+8 choose 8]_q - q^(4l-18) [12 choose 6]_q, from the definition."""
    g = qbinom_coeffs(l + 8, 8)
    sh = 4 * l - 18
    d = max(len(g) - 1, 36 + sh)
    out = []
    for e in range(d + 1):
        gi = g[e] if e < len(g) else 0
        out.append(gi - bget(e - sh))
    return out, sh


def status(l):
    c, sh = F_coeffs(l)
    n = len(c)
    sym = all(c[i] == c[n - 1 - i] for i in range(n))
    ctr = (n - 1) // 2
    uni = all(c[i] <= c[i + 1] for i in range(ctr)) and all(c[i] >= c[i + 1] for i in range(ctr, n - 1))
    return sym, uni, all(v >= 0 for v in c), ctr, c


def reduced_ok(l):
    g, sh = qbinom_coeffs(l + 8, 8), 4 * l - 18
    for j in OFFSETS:
        d = 4 * l - 18 + j
        a1 = g[d + 1] if d + 1 < len(g) else 0
        a0 = g[d] if d < len(g) else 0
        if a1 - a0 < Db[j]:
            return False, j
    return True, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=80)
    ap.add_argument("--big", default="839,840,841,1000,1680,2520")
    args = ap.parse_args()

    # 1. sanity
    for l in (5, 6, 7, 20):
        g = qbinom_coeffs(l + 8, 8)
        assert sum(g) == comb(l + 8, 8), f"coefficient sum wrong at l={l}"
        assert len(g) == 8 * l + 1, f"degree wrong at l={l}"
        assert g[0] == g[-1] == 1, f"endpoint wrong at l={l}"
    print("sanity OK: sum of coefficients = ordinary binomial, degree 8l, endpoints 1")

    # 2. low cases, complete
    for l in (5, 6, 7):
        sym, uni, nn, ctr, c = status(l)
        run = c[4 * l - 2: 4 * l + 3]
        print(f"l={l}: deg={len(c)-1} centre={ctr} symmetric={sym} nonneg={nn} unimodal={uni} "
              f"central run(deg 4l-2..4l+2)={run}")
        if not nn:
            print("FAIL: nonnegativity"); return 1
        if l == 5 and uni:
            print("FAIL: l=5 expected non-unimodal"); return 1
        if l > 5 and not uni:
            print("FAIL: l>=6 expected unimodal"); return 1

    # 3. direct sweep
    bad = [l for l in range(6, args.n + 1) if not status(l)[1] or not status(l)[2]]
    print(f"direct full-polynomial sweep l=6..{args.n}: failures {bad if bad else 'none'}")
    if bad:
        return 1

    # 4. large sample
    for l in [int(x) for x in args.big.split(",")]:
        sym, uni, nn, ctr, c = status(l)
        print(f"  l={l}: symmetric={sym} unimodal={uni} nonneg={nn}")
        if not (sym and uni and nn):
            return 1

    # 5. equivalence of the reduction
    mism = [l for l in range(5, 61) if status(l)[1] != reduced_ok(l)[0]]
    print(f"reduction equivalence (direct unimodality vs 19 inequalities) l=5..60: "
          f"mismatches {mism if mism else 'none'}")
    print(f"Db derived here: {[Db[j] for j in OFFSETS]}")
    if mism:
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
