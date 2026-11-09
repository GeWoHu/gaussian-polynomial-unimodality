#!/usr/bin/env python3
"""R1 decisive independent check -- genuinely different implementation.

The certificate generator computes margins via inclusion-exclusion over the
parts-<=8 partition function p8 (Lemma 3 route). THIS script, written from
scratch for R1, recomputes the same quantities through a dense truncated
Gaussian-polynomial route and:

  (A) recomputes Q(0) for ALL 15,960 certificate classes and compares to the
      stored 0th Newton coefficient (Q(0));
  (B) for 120 random classes recomputes Q(0)..Q(7) densely and recovers ALL
      Newton coefficients by forward differences, comparing to the stored
      octuples;
  (C) verifies the finite base 6..839 margins directly from dense
      coefficient differences for all 19 offsets.

Exact integers only. No floats.
"""
import json, random, sys

PER = 840
JS = list(range(-1, 18))

def a_l_dense(l, N):
    """a_l(n) for 0<=n<=N: partitions in the 8 x l box.
    Dense route: 1/prod_{i=1..8}(1-q^i) by coin-change DP, then multiply the
    numerator factors (1-q^{l+i}) one at a time (descending in-place).
    Independent of the generator's p8 inclusion-exclusion code path."""
    out = [0] * (N + 1)
    out[0] = 1
    for i in range(1, 9):
        for e in range(i, N + 1):
            out[e] += out[e - i]
    for i in range(1, 9):
        s = l + i
        for n in range(N, s - 1, -1):
            out[n] -= out[n - s]
    return out

def db_vector():
    """[12 choose 6]_q by the same dense route (k=6, box 6x6), Db derived."""
    N = 36
    arr = [0] * (N + 1)
    arr[0] = 1
    for i in range(1, 7):
        for e in range(i, N + 1):
            arr[e] += arr[e - i]
    for i in range(1, 7):
        s = 6 + i
        for n in range(N, s - 1, -1):
            arr[n] -= arr[n - s]
    b = arr
    return [b[j + 1] - (b[j] if j >= 0 else 0) for j in JS], b

def newton_from_values(vals):
    v = list(vals)
    out = []
    while v:
        out.append(v[0])
        v = [v[i + 1] - v[i] for i in range(len(v) - 1)]
    return out

def main():
    cert = json.load(open("certificate.json"))
    db, b = db_vector()
    assert db == cert["Db_derived"], "Db mismatch"
    obl = cert["records"]
    assert len(obl) == 15960 and cert["obligations"] == 15960

    # sanity: b palindromic, b[0]=b[36]=1, sum = binom(12,6)=924
    assert b[0] == 1 and b[36] == 1 and sum(b) == 924 and b == b[::-1]

    # (A) Q(0) for all classes via dense route, one array per l = r+840
    print("(A) recomputing Q(0) for all 15,960 classes (dense route)...")
    by_r = {}
    for o in obl:
        by_r.setdefault(o["r"], {})[o["j"]] = o
    badA = 0
    for r in range(PER):
        l = r + PER
        a = a_l_dense(l, 4 * l - 18 + 17 + 1)
        for jj, j in enumerate(JS):
            c = -18 + j
            q0 = a[4 * l + c + 1] - a[4 * l + c] - db[jj]
            if q0 != by_r[r][j]["newton"][0]:
                badA += 1
                if badA < 5:
                    print("  MISMATCH", j, r, q0, by_r[r][j]["newton"][0])
        if r % 168 == 0:
            print(f"  r={r} done ({r+1}/840)")
    print(f"(A) RESULT: Q(0) mismatches = {badA} / 15,960")

    # (B) full Newton octuples, 120 random classes, dense values
    print("(B) dense octuple reconstruction on 120 random classes...")
    rng = random.Random(20261109)
    sample = rng.sample(obl, 120)
    cache = {}
    badB = 0
    for o in sample:
        j, r = o["j"], o["r"]
        jj = JS.index(j)
        vals = []
        for t in range(8):
            l = r + PER * (t + 1)
            key = l
            if key not in cache:
                cache[key] = a_l_dense(l, 4 * l)
            a = cache[key]
            c = -18 + j
            vals.append(a[4 * l + c + 1] - a[4 * l + c] - db[jj])
        nc = newton_from_values(vals)
        if nc != o["newton"]:
            badB += 1
            print("  MISMATCH", j, r, nc, o["newton"])
    print(f"(B) RESULT: sampled classes with octuple mismatch = {badB} / 120")

    # (C) finite base 6..839 margins, all 19 offsets
    print("(C) finite base 6..839 margins (dense route)...")
    minm, argmin, badC = None, None, 0
    for l in range(6, 840):
        a = a_l_dense(l, 4 * l)
        for jj, j in enumerate(JS):
            d = 4 * l - 18 + j
            m = a[d + 1] - a[d] - db[jj]
            if m < 0:
                badC += 1
            if minm is None or m < minm:
                minm, argmin = m, (l, j)
    print(f"(C) RESULT: negative margins = {badC}; min margin = {minm} at {argmin}")

    ok = badA == 0 and badB == 0 and badC == 0 and minm == 1 and argmin == (6, 16)
    print("R1 DECISIVE VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
