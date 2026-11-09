# Full proof audit — MATH-06-MR (items A–E)

Auditor: orchestrator (exact integer arithmetic throughout; reruns in
`verification/runs/REPRO.out`, `verification/runs/S62.out`). The hostile referee (META-01,
different provider) independently repeats the computational parts in its own clean directory;
its report is `referee/REPORT.md`.

Theorem under audit (unchanged): `F_ℓ(q) = [ℓ+8 choose 8]_q − q^(4ℓ−18)[12 choose 6]_q`
coefficientwise nonnegative for every integer ℓ ≥ 5; unimodal for every ℓ ≥ 6; non-unimodal at
ℓ = 5.

## A. Ferrers-diagram injection (paper §4, Theorem 4)

- **Partition preservation:** Φ(λ) = (λ₁+1,…,λ_{k/2}+1, λ_{k/2+1},…,λ_k). The only adjacent pair
  at risk is (k/2, k/2+1): λ_{k/2}+1 ≥ λ_{k/2+1} holds since λ_{k/2} ≥ λ_{k/2+1} (integers).
  Other adjacencies unaffected. ✓
- **Injectivity:** subtract 1 from the first k/2 parts recovers λ. ✓
- **Degree shift:** |Φλ| = |λ| + k/2, matching s(m+1)−s(m) = k/2 for even k with the SZ shift
  convention. ✓
- **Box bound:** λ₁ ≤ m−k ⟹ λ₁+1 ≤ (m+1)−k. ✓
- **Admissibility:** for even k, 3 ≤ k ≤ m, b ≤ (km−4k+4)/(k−2), kb ≡ km (mod 2): parity for
  (m+1,b) follows since k even ⟹ k(m+1) ≡ km (mod 2); the upper bound for b is nondecreasing in
  m. ✓
- **Exact base-case margins (k=8):** window-margin minimum 1 at ℓ=5 (degree 2), 10 at ℓ=6
  (degree 6); finite-base margin minimum 1 at (ℓ,j) = (6,16); central surplus exactly 4 vs
  required 3 at ℓ=6,7. All reproduced by exact computation. ✓
- **General even k vs k=8:** the k=8 slice does NOT establish the general statement; the paper
  proves the general even-k theorem as a standalone environment and uses only its k=8 instance
  for the main theorem. Each step above is checked for general even k; no step silently assumes
  k=8. Honest status: general theorem verified line-by-line here and by the referee; only the
  k=8 instance is load-bearing for the main result. ✓

## B. Reduction to 19 inequalities (paper §5, Theorem 2)

- Symmetry: F_ℓ palindromic of degree 8ℓ (both terms: [ℓ+8 choose 8] palindromic deg 8ℓ;
  q^(4ℓ−18)[12 choose 6] palindromic about 4ℓ−18+18 = 4ℓ). ✓ verified exactly at ℓ ∈
  {6,17,840,841}.
- Unimodality ⟺ c_{d+1} ≥ c_d for 0 ≤ d ≤ 4ℓ−1. With d = 4ℓ−18+j:
  c_{d+1}−c_d = (a_ℓ(d+1)−a_ℓ(d)) − (b_{j+1}−b_j), b_j = [q^j][12 choose 6]_q.
  **Sign convention verified:** the margin is written as a(d+1)−a(d) ≥ Db_j = b_{j+1}−b_j
  (forward differences of coefficients against forward differences of b). Direct polynomial at
  ℓ=20 matches the convention; equivalence of Theorem 2 against direct unimodality confirmed for
  5 ≤ ℓ ≤ 60 (0 mismatches).
- j ≤ −2: both b-indices < 0 ⟹ b_{j+1}−b_j = 0 and a_ℓ(d+1)−a_ℓ(d) ≥ 0 by unimodality of the
  Gaussian polynomial with d+1 < 4ℓ (classical; O'Hara/Zeilberger lineage). No condition.
- j ≥ 18: d ≥ 4ℓ, covered by palindromic symmetry of the condition set. No condition.
- j = −1 carries a condition: b₀−b₋₁ = 1−0 = 1 (paper states this explicitly). ✓
- Count: j ∈ {−1,0,…,17} = 19 inequalities. Db vector re-derived from [12 choose 6]_q inside the
  code (never tabulated): [1,0,1,1,2,2,4,2,5,4,6,4,7,3,6,3,4,0,3], matching Table 1. ✓

## C. Quasipolynomial argument (paper §6, Lemma 5 + Lemma 6)

- p(n) = [q^n] ∏_{i≤8}(1−q^i)^{-1}, p(n)=0 for n<0: P(q)=1/D(q) is PROPER (deg D = 36 > 0), so
  the partial-fraction decomposition over the 840-th roots of unity has NO polynomial part;
  coefficient extraction is an identity of formal power series for EVERY n ≥ 0 — no eventual-only
  assumption, no finitely-supported correction terms. Multiplicities m(ζ) ≤ 8 ⟹ per-class degree
  ≤ 7; period divides 840 = lcm(1..8). ✓
- Inclusion–exclusion (Lemma 6): expansion of ∏(1−q^{ℓ+i}) — exact finite identity of
  polynomials, no convergence issue. ✓
- **Truncation audit:** argument of p for subset S is 4ℓ−18+j −|S|ℓ −σ(S). For |S|=4:
  j−18−σ ≤ 17−18−10 = −11 < 0. For |S|≥5: −ℓ+(j−18)−σ ≤ −ℓ−1−15 = −ℓ−16 < 0. So all |S| ≥ 4
  terms vanish for ℓ ≥ 840 — and in fact for every ℓ ≥ 1 — matching p(n)=0 for n<0. Boundary
  terms |S| ≤ 3: arguments are linear in ℓ with residue fixed on each class ℓ ≡ r (mod 840), so
  each contributes a polynomial in t of degree ≤ 7 valid for all integer t ≥ 0. ✓
- Corollary (Q_{j,r} polynomial in t, degree ≤ 7, all t ≥ 0): follows; the parameterization
  ℓ = r + 840(t+1) is a bijection {0..839} × {t ≥ 0} → {ℓ ≥ 840} with no gaps (r = ℓ mod 840,
  t = ⌊ℓ/840⌋ − 1; ℓ=840 ↔ (r,t)=(0,0)). ✓

## D. Infinite certificate (paper §6, Theorem 3 + certificate files)

- Newton positivity lemma: Q real polynomial degree ≤ 7 with Δ^i Q(0) ≥ 0, i = 0..7 ⟹
  Q(t) = Σ binom(t,i) Δ^i Q(0) ≥ 0 for every integer t ≥ 0 (Newton forward expansion;
  binom(t,i) ≥ 0 for integer t ≥ 0). No analytic positivity beyond integers is claimed or needed. ✓
- Degree bound: certificate stores 8 Newton coefficients per class; the 6th/7th vanish in all
  15,960 classes (exact recomputation), so degree ≤ 5 ≤ 7 — the bound used to size the
  certificate is never violated. **Degree drop 7→5 documented** in section62-analysis.md:
  exhaustive-exact (all classes) plus structural explanation (palindromic central symmetry kills
  the smooth degree-7/6 contributions; surviving leading term ∝ (2c+1)·ℓ⁵ ≠ 0). Not required
  for the main theorem; the certificate verifies the bound it uses.
- Parameter mapping: each record (j,r) stores the Newton octuple of Q_{j,r} at t=0; obligations
  = 19 × 840 = 15,960, completeness + duplicate detection enforced by the verifier. ✓
- All 15,960 obligations: nonnegativity checked; full 8-vector reconstruction through the dense
  truncated route inside verify_certificate.py; third-route r1_decisive.py re-derives Q(0) for
  all classes and full octuples on 120 seeded classes. Hash of regenerated certificate:
  e3930e99e9888acdd7efdab39e65519476f0a907f9ff7637e40b40f9cff60e95 (byte-stable across runs). ✓

## E. Finite range (paper §3 Theorem 1 base + §8)

- All 19 inequalities for 6 ≤ ℓ ≤ 839 recomputed by dense route: 0 negative margins; minimum
  margin 1 at (ℓ,j) = (6,16). Boundary: finite range covers 6..839, tail starts at 840 — no gap,
  no overlap (verifier range check). ✓
- ℓ = 5 counterexample confirmed exactly: F_5 central coefficients (15,16,15,16,15) at degrees
  18..22 — rises, falls, rises, falls ⟹ not unimodal; nonnegativity holds (window minimum 1). ✓
- Direct full-polynomial construction: F_5, F_6, F_7 built from the definition of the Gaussian
  polynomial and scanned; sweep 6..80 clean; large-parameter spot checks ℓ ∈ {839, 840, 841,
  1000, 1680, 2520} unimodal. ✓

## Stored data vs reduction sufficiency (mission §3 requirement)

Hash equality verifies ONLY that the stored certificate bytes match. The mathematical reduction
that makes the data sufficient is verified separately and every run: Lemma 5 + Lemma 6 +
Corollary + Newton lemma (hand proofs, paper §6) establish that the 15,960 octuples ⟹ 19
inequalities for all ℓ ≥ 840; the reduction theorem (hand proof + machine-checked equivalence
for 5 ≤ ℓ ≤ 60) establishes 19 inequalities ⟺ unimodality; the finite base closes 6..839. The
verifier additionally re-derives Db from [12 choose 6]_q and recomputes every stored value
through a second code path, so stored-data trust is reduced to arithmetic, not to the generator.

## Residual honest caveats

- The general even-k Theorem 4 is verified line-by-line but its generality is not exercised;
  only k=8 is needed. A human reader should still check the general statement only if they care
  about it.
- Bibliography journal metadata is taken from arXiv journal-ref fields (2026-11-09); paywalled
  venue confirmation is UNVERIFIED (referee classification).
- Novelty: statement priority belongs to Stanley–Zanello; see literature/NOVELTY_AUDIT.md.
