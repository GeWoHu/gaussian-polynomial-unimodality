# CHANGES — revised.tex vs original manuscript (paper-1 / R1 paper.tex)

Baseline: `math06-publication-r1/manuscript/paper.tex` (the 8-page R1 revision of paper-1,
which is `math06-publication/manuscript/paper.tex` plus the R1 repairs). The theorem statement,
all proof environments, tables, and bibliography entries are UNCHANGED from the R1 baseline;
this mission changes four expository passages. Full diff: 33 lines across 4 blocks
(`diff` of the two .tex files). No mathematical result was weakened, strengthened, or altered.

## 1. §6.2 — asymptotic degree claim repaired (the mission's mandatory correction)

- **Before:** "Both terms are, at fixed offset, degree-6 quasi-polynomials in ℓ whose terms of
  degree 4, 5, 6 cancel exactly, leaving a residual of order ℓ³ that must be compared against
  absolute constants (3 and 7)."
- **After:** degree-6 leading terms cancel exactly while the degree-5 term survives; the
  difference is of degree exactly 5 on each residue class (certificate: 5th Newton coefficient
  nonzero in all 15,960 classes, 6th/7th vanish identically); mechanism stated (palindromic
  symmetry a_ℓ(m)=a_ℓ(8ℓ−m) kills the smooth degree-7/6 contributions; leading smooth term
  ∝ (c+1)²−c² = 2c+1 at degree ℓ⁵; lower periodic terms cannot raise the degree above 5);
  exact rational interpolation evidence cited; "residual of order ℓ³" replaced by "residual of
  degree 5".
- **Justification:** exact symbolic derivation in `proofs/section62-analysis.md` — individual
  counting terms degree 6, difference exactly degree 5; deg-7/6 leading coefficients verified
  equal across offsets and sampled residue classes; surviving deg-5 coefficient
  = −(2c+1)·576,240,000 ≠ 0 for every integer offset.
- The displayed partition-counting identity itself is CORRECT (direct enumeration: 30/30 exact
  matches) and is left intact. The paragraph's qualitative conclusion (surplus must beat absolute
  constants; near-tightness 4 vs 3) is unchanged and does not depend on the corrected degree.

## 2. §6 ("Why this is a certificate") — recomputation claim synchronized to the hardened verifier

- **Before:** "…the same values are recomputed through a second independent code path (dense
  Gaussian polynomials) on a seeded sample."
- **After:** the verification package recomputes the COMPLETE Newton vectors of EVERY obligation
  through a second independent code path (dense truncated Gaussian multiplication), so a
  value-tampered certificate cannot pass.
- **Justification:** matches verify_certificate.py step 6 as hardened in R1 and re-run here
  (`verification/runs/REPRO.out` #2).

## 3. §7 — verifier description synchronized

- **Before:** "…recomputes a seeded sample of obligations through an independent
  dense-polynomial code path, failing non-zero on a missing, truncated, or corrupted
  certificate;"
- **After:** recomputes the full eight-coefficient Newton vector of EVERY one of the 15,960
  obligations through an independent dense code path (plus a seeded sample through a third
  route), failing non-zero on a missing, truncated, or VALUE-TAMPERED certificate.

## 4. §7 — runtime expectations synchronized

- **Before:** "Reference timings … total under ten seconds."
- **After:** generation about one second, full verification about sixty-five seconds (dominated
  by the 15,960-class dense recomputation), independent checks under two seconds.
- **Justification:** measured 1.15 s / 65.0 s / 0.15 s + 11.5 s in this mission's clean-room run.

## Reconciliation sweep (mission item 4.3, no edits required)

- Certificate counts: 15,960 = 19 × 840 everywhere (abstract, §6, §7, EXPECTED_RESULTS.md,
  quickstart). ✓
- Parameter ranges: finite base 6 ≤ ℓ ≤ 839, tail ℓ ≥ 840, no gap/overlap; ℓ = 5 handled
  separately; verified by verifier range check. ✓
- Theorem numbering/cross-references: recompiles with zero undefined or multiply-defined
  references (tectonic, 8 pages). ✓
- Scope statement (fixed (k,b)=(8,12) slice, not the general Stanley–Zanello conjecture):
  present in §1 and §10 as in R1, unchanged. ✓
- Sharpness example ℓ=5 and the coefficientwise-nonnegativity-for-ℓ≥5 claim: preserved verbatim. ✓
- Author placeholder line: preserved (owner approval still pending). ✓
