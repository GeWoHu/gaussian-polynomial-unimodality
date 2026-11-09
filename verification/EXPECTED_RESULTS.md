# Expected verification results (MATH-06P)

Reference machine: Fedora (x86_64), `python3` = **Python 3.15.0**, verification uses the
**standard library only** (`requirements.txt` is empty by design). No floating point anywhere.
The certificate payload is version-independent (no runtime metadata embedded), so regeneration
is byte-identical on any Python >= 3.10. Reference run: 2026-11-09 (R2).

## Artifacts and hashes

| file | sha256 |
|---|---|
| `certificate.json` | `d6454b2bcb3197693ea89f3214ba3319f3e2a1f3764bda0b2e7aa12feac123ec` |

A hash match confirms byte-level integrity of the shipped certificate; it says nothing about
theorem correctness. Correctness is established by the mathematical checks below plus the
independent recomputation step in `verify_certificate.py`.

## Commands and expected output

```bash
cd verification
python3 generate_certificate.py --out certificate.json   # 1.13 s reference
python3 verify_certificate.py --cert certificate.json --sample 12   # ~66 s reference (hardened verifier: full 15,960-class recomputation + native 6..839 finite-base recomputation)
python3 independent_check.py --n 80                      # 0.14 s reference
```

### 1. `generate_certificate.py`

```
certificate written: certificate.json
obligations=15960 negative_newton_classes=0 classes_with_degree>5=0
min_tail_Q0=3552106826 finite_min_margin=1 at (l,j)=(6, 16)
Db_derived=[1, 0, 1, 1, 2, 2, 4, 2, 5, 4, 6, 4, 7, 3, 6, 3, 4, 0, 3]
```

Interpretation:

* `obligations=15960` = 19 offsets (`j = -1..17`) x 840 residue classes — the complete set.
* `negative_newton_classes=0` — every Newton coefficient `Delta^i Q(0)`, `i = 0..7`, is
  nonnegative, which by `Q(t) = sum_i binom(t,i) Delta^i Q(0)` with `binom(t,i) >= 0` proves
  `Q(t) >= 0` for every integer `t >= 0`, i.e. every `l >= 840`.
* `classes_with_degree>5=0` — the 6th and 7th Newton orders vanish identically, so the margin
  polynomials have true degree `<= 5`, one degree lower than the bound `<= 7` used for the
  certificate.
* `min_tail_Q0=3552106826` — smallest tail margin (class `j=17, r=0`); the tail is far from sharp.
* `finite_min_margin=1 at (l,j)=(6,16)` — the sharp point of the whole theorem.
* `Db_derived` is computed from `[12 choose 6]_q` inside the script; it is not read from a table.

### 2. `verify_certificate.py`

```
hash OK: e3930e99e9888acdd7efdab39e65519476f0a907f9ff7637e40b40f9cff60e95
Db re-derived from [12 choose 6]_q OK: [1, 0, 1, 1, 2, 2, 4, 2, 5, 4, 6, 4, 7, 3, 6, 3, 4, 0, 3]
structure OK: 15960 obligations, complete and duplicate-free
all Newton coefficients nonnegative OK (15,960/15,960)
degree <= 5 confirmed: classes with nonzero 6th/7th Newton order = 0
independent recomputation OK on 12 sampled obligations (dense Gaussian code path, seed 20261108)
range boundary OK: finite 6..839, tail l>=840, no gap or overlap
VERDICT: PASS
```

Failure modes that are detected (each exits non-zero): missing certificate, truncated or
non-JSON certificate, wrong schema, hash mismatch against this file, `Db` mismatch against the
re-derivation, missing/duplicated obligations, wrong Newton-vector length or non-integer entries,
any negative Newton coefficient, nonzero top Newton orders, disagreement with the dense-Gaussian
recomputation, and any inconsistency of the finite/tail boundary.

### 3. `independent_check.py`

```
sanity OK: sum of coefficients = ordinary binomial, degree 8l, endpoints 1
l=5: deg=40 centre=20 symmetric=True nonneg=True unimodal=False central run(deg 4l-2..4l+2)=[15, 16, 15, 16, 15]
l=6: deg=48 centre=24 symmetric=True nonneg=True unimodal=True central run(deg 4l-2..4l+2)=[91, 92, 93, 92, 91]
l=7: deg=56 centre=28 symmetric=True nonneg=True unimodal=True central run(deg 4l-2..4l+2)=[227, 230, 231, 230, 227]
direct full-polynomial sweep l=6..80: failures none
  l=839: symmetric=True unimodal=True nonneg=True
  l=840: symmetric=True unimodal=True nonneg=True
  l=841: symmetric=True unimodal=True nonneg=True
  l=1000: symmetric=True unimodal=True nonneg=True
  l=1680: symmetric=True unimodal=True nonneg=True
  l=2520: symmetric=True unimodal=True nonneg=True
reduction equivalence (direct unimodality vs 19 inequalities) l=5..60: mismatches none
Db derived here: [1, 0, 1, 1, 2, 2, 4, 2, 5, 4, 6, 4, 7, 3, 6, 3, 4, 0, 3]
VERDICT: PASS
```

`independent_check.py` never touches the quasipolynomial machinery: it builds the full polynomial
`F_l` from the definition of the Gaussian polynomial and scans coefficients, so it validates the
theorem statements themselves rather than the certificate.

## Reproduction contract

1. Obtain `generate_certificate.py`, `verify_certificate.py`, `independent_check.py`,
   `EXPECTED_RESULTS.md`, and optionally `certificate.json`.
2. Run the three commands above.
3. `generate_certificate.py` regenerates the certificate from scratch; compare its sha256 with the
   table (deterministic, no randomness, no floats — a mismatch means a different arithmetic or code).
4. `verify_certificate.py` re-derives the offset constants, checks all 15,960 obligations, and
   recomputes a seeded sample of obligations through a second independent code path.
5. `independent_check.py` re-verifies the theorem statements by direct construction.
6. The theorem statement in `manuscript/paper.tex` (Theorem 1) must match the polynomial and the
   quantifiers verified here: `F_l(q) = [l+8 choose 8]_q - q^(4l-18)[12 choose 6]_q`, unimodal for
   every integer `l >= 6`, nonnegative for every `l >= 5`, and non-unimodal at `l = 5`.

## R1 additions (2026-11-09)

### Hardened verifier (full value check)

`verify_certificate.py` now reconstructs the complete 8-coefficient Newton vector for ALL 15,960
classes through the dense truncated code path before the seeded sample. Reference run (clean room,
Python 3.15.0, Fedora x86_64):

```
$ python3 verify_certificate.py --cert certificate.json --sample 12
...
all Newton coefficients nonnegative OK (15,960/15,960)
degree <= 5 confirmed: classes with nonzero 6th/7th Newton order = 0
full value check OK: 15,960/15,960 classes match dense octuple recomputation
independent recomputation OK on 12 sampled obligations (dense Gaussian code path, seed 20261108)
range boundary OK: finite 6..839, tail l>=840, no gap or overlap
VERDICT: PASS        (exit 0; wall time 1m05s)
```

### Corruption battery (must fail non-zero)

| tamper | verifier result | exit |
|---|---|---|
| one stored Newton coefficient +1 (class (j,r)=(-1,500), order 3) | `FAIL: full Newton-vector recomputation found 1 value mismatches` | 1 |
| one obligation dropped (15,959 records) | `FAIL: expected 15960 obligations, found 15959` | 1 |
| file truncated to 900 KB | JSON parse failure | 1 |
| file missing | `FAIL: certificate ... missing` | 1 |
| intact control | `VERDICT: PASS` | 0 |

Raw outputs preserved in `runs_r1/` (`REPRO_RUN.out`, `R1_DECISIVE.out`, `CORRUPTION_TESTS.out`,
`HARDENED_VERIFY.out`).

### Third-route decisive check (`r1_decisive.py`)

Written from scratch for R1; recomputes via truncated dense Gaussian multiplication (different code
path from the generator's inclusion-exclusion-over-p8 route):
(A) Q(0) for all 15,960 classes — 0 mismatches; (B) full Newton octuples on 120 seeded random
classes — 0 mismatches; (C) finite base 6..839, all 19 offsets — 0 negative, min margin 1 at
(6,16). `R1 DECISIVE VERDICT: PASS` (11.7 s).

```
$ python3 r1_decisive.py        # requires certificate.json in cwd
```

Versions: Python 3.15.0 (3.15.0-1.fc45.x86_64), Linux x86_64 Fedora 45, no third-party packages
(`requirements.txt` empty).
