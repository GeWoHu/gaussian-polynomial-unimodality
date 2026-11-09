# Section 6.2 exact-symbolic analysis (MATH-06-MR)

Script: `verification/s62_analysis.py` (exact integers + `fractions.Fraction`; no floats).
Raw output: `verification/runs/S62.out`. Python 3.15.0, 2.2 s.

## The passage under review

The R1 manuscript §6.2 ("The obstruction to an injection-only proof") displayed the identity

  a_ℓ(n+1) − a_ℓ(n) = #{μ ⊢ n+1 in the 8×ℓ box : μ₁ = μ₂} − #{λ ⊢ n in the box : λ₁ = ℓ}

and then asserted: "Both terms are, at fixed offset, degree-6 quasi-polynomials in ℓ whose terms
of degree 4, 5, 6 cancel exactly, leaving a residual of order ℓ³."

The certificate reports nonzero FIFTH-order Newton coefficients in all 15,960 classes and margin
polynomials of degree 5. The asymptotic sentence is therefore wrong; the identity is not.

## 1. Exact degree of each quantity (per residue class ℓ ≡ r mod 840, offset n = 4ℓ + c)

Exact Newton interpolation (rational arithmetic, 8 nodes per class, ℓ = r + 840(t+1)):

| quantity | degree | evidence |
|---|---|---|
| a_ℓ(4ℓ+c) =: A_c(ℓ) | **7** | interpolated degree 7 at r ∈ {0,1,500,839}; leading coeff 438,541,689,600,000 (identical for all sampled r and c) |
| T₁ = #{μ : μ₁=μ₂} at (ℓ, 4ℓ+c+1) | **6** | interpolated degree 6 at all sampled classes |
| T₂ = #{λ : λ₁=ℓ} at (ℓ, 4ℓ+c) | **6** | interpolated degree 6 at all sampled classes |
| D = T₁ − T₂ = A_{c+1} − A_c | **exactly 5** | interpolated degree 5; certificate: 5th Newton coefficient ≠ 0 in **15,960/15,960** classes, 6th/7th vanish in all |

Distinction required by the mission: **individual counting terms have degree 6; their difference
has degree 5.** The margin Q_{j,r} (D minus the constant Db_j) has the same degree 5.

## 2. Which leading coefficients cancel, which survive

- deg-7: A_c and A_{c+1} have the SAME degree-7 coefficient (438541689600000 sampled; the leading
  term is the continuous slice-volume density, insensitive to an O(1) shift of n) → cancels.
- deg-6: lc₆(T₁) = lc₆(T₂) exactly in every sampled class → cancels; equivalently
  lc₆(A_{c+1} − A_c) = 0.
- deg-5: lc₅(T₁) − lc₅(T₂) ≠ 0 in every sampled class. Exact values (parameter t):
  c = −19 → 21,320,880,000; c = −10 → 10,948,560,000; c = −1 → 576,240,000.
  All equal **−(2c+1)·576,240,000**, independent of the residue class r, and nonzero for every
  integer c (the factor 2c+1 is odd). **The degree-5 term survives.**

So the old sentence's "degree 4, 5, 6 cancel" is wrong in exactly two places: degree 6 cancels
(holds), degree 5 does not cancel (fails), degree 4 is not the residue — the residual is degree 5.

## 3. Is the displayed partition-counting identity correct?

YES. Independent direct enumeration (m-sum over μ₁=μ₂=m with Gaussian [m+6 choose 6], and
[ℓ+7 choose 7] for λ₁=ℓ) matched a_ℓ(n+1) − a_ℓ(n) at 6 fixed and 24 seeded pairs: 0 mismatches.
The bijective proof (subtract 1 from the largest part: {μ₁ ≥ μ₂+1} ↔ partitions of n−1 in the
8×(ℓ−1) box) is exact and gives the fast closed forms T₁ = a_ℓ(N) − a_{ℓ−1}(N−1),
T₂ = a_ℓ(n) − a_{ℓ−1}(n), also verified. **The identity stands; only the asymptotic gloss was
repaired.**

## 4. Does degree 5 follow analytically, or only from computation?

Two layers, kept separate:

- **Proof-grade (exhaustive, exact):** the drop 7 → 5 and the nonzero degree-5 coefficient are
  established for ALL classes by the certificate's exact integer arithmetic (15,960 classes;
  6th/7th Newton coefficients identically zero; 5th never zero). This is a finite proof, not
  sampling.
- **Structural explanation (why it had to happen):** the window sits at the CENTRE of the
  coefficient array: palindromic symmetry a_ℓ(m) = a_ℓ(8ℓ − m) (verified exactly at ℓ ∈ {6,17,840,
  841}) makes the continuous slice-volume V symmetric about n/ℓ = 4. Its Taylor expansion in 1/ℓ
  therefore contains only EVEN powers, so the first difference
  ℓ⁷[V(4+(c+1)/ℓ) − V(4+c/ℓ)] contains only ODD degrees ℓ⁵, ℓ³, ℓ¹ — the degree-7 and degree-6
  contributions vanish identically, and the leading surviving term is
  V″(4)·((c+1)² − c²)·ℓ⁵ ∝ (2c+1)·ℓ⁵. The exact interpolation reproduces precisely this
  (2c+1)-proportionality with class-independent constant. V″(4) ≠ 0 is witnessed by the
  certificate (nonzero lc₅), not assumed.
- We do NOT claim a closed-form analytic proof of the drop that bypasses the finite certificate;
  the main theorem does not need one (the certificate's degree bound is verified, not assumed).

## 5. Dependent statements audit

grep over `paper.tex`: the phrase "order $\ell^3$" and any asymptotic-degree claim occur ONLY in
§6.2 (one line). The proof chain (reduction → Lemma quasi → Lemma IE → Corollary → Newton
positivity → certificate → finite base) contains no asymptotic inputs; §6.2 is expository
motivation for why the injection mechanism is quantitatively insufficient. Its qualitative
conclusion (a surplus must be beat against absolute constants 3 and 7; near-tightness 4 vs 3 at
ℓ=6) is unaffected by the degree correction. Corollary 5's "degree at most 7" bound and the
remark "the true degree is at most 5" are both correct as stated. No other statement depends on
the incorrect asymptotic analysis.

## Repair applied

§6.2 now states: degree-6 leading terms cancel exactly, degree-5 survives (exactly degree 5 per
class, certificate-confirmed), cites the palindromic-symmetry mechanism, and distinguishes term
degrees (6) from the difference degree (5). See CHANGES.md item 1.
