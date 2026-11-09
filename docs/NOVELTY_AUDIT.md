# Novelty & significance audit — MATH-06-MR

Method: primary-source extraction (arXiv abs records + full-text theorem statements retrieved
2026-11-08/09; raw search receipts are archived in the research record, not shipped with this
repository), fresh searches for
2024–2026 resolutions, and hypothesis-level comparison. Search-absence is never used alone to
infer novelty. Classification per mission scale: KNOWN / ELEMENTARY-CONSEQUENCE /
APPARENTLY-NEW-PRIORITY-UNRESOLVED / GENUINELY-NEW-CANDIDATE.

## Claim-by-claim classification

### C1. Main theorem — unimodality of F_ℓ = [ℓ+8 choose 8]_q − q^(4ℓ−18)[12 choose 6]_q for all ℓ ≥ 6

Stanley–Zanello (arXiv:1711.10033; J. Combin. 11(1) (2020) 111–126, journal-ref verified from the
arXiv record 2026-11-09): define f(k,m,b) = [m choose k]_q − q^(k(m−b)/2 + b − 2k + 2)
[b choose k−2]_q, admissible b ≤ (km−4k+4)/(k−2), kb ≡ km (mod 2), exception
b = (km−4k+2)/(k−2). Our slice: (k,b) = (8,12) — admissible since 12 ≤ (8m−28)/6 for m ≥ 13 —
with m = ℓ+8; our F_ℓ is exactly f(8, ℓ+8, 12). Proved range in SZ: complete characterization
for k ≤ 5 (their Theorems 2.2–2.5). Conjecture 1.1 predicts unimodality for all admissible
(k,b), m ≫_k 0 — our theorem is the (8,12) instance of the conjecture, not a theorem of SZ.
Koutschan–Uncu–Wong (arXiv:2302.04067; ISSAC 2023 434–442, doi:10.1145/3597066.3597113): d-strict
monotonicity with explicit L(m,d), U(m,d) bounds via closed forms + cylindrical algebraic
decomposition; Section 4 closes SZ at k=6 and k=7 (their m = our k) with exception tables;
computation stops at m=7, m ≥ 8 stated feasible "in principle" only. Not covered; their k=7
CAD budget already required weeks of CPU — our slice is beyond their proved cases.
Post-2023 searches ("Stanley Zanello unimodality", "Gaussian polynomial difference unimodality",
papers citing 1711.10033 / 2302.04067, "k=8 Gaussian difference certificate"): no source states
this slice theorem or a stronger theorem implying it.
**Classification: GENUINELY-NEW-CANDIDATE requiring external confirmation** (proof not found in
literature; statement priority to SZ 2017/2020; proof priority unresolved until specialist/
MathReviews check — that is exactly what "external confirmation" means here).

### C2. Sharpness instance ℓ = 5 (nonnegative, non-unimodal, central pattern (15,16,15,16,15))

The existence of low-m exceptions is anticipated by SZ's exception structure (their conjecture's
bound b ≤ (km−4k+4)/(k−2): at m = 13 this gives b ≤ 76/6 ≈ 12.67, so b = 12 sits at the edge of
admissibility exactly where ℓ = 5 breaks, and isolated low-m counterexamples are documented
already at k = 3). The explicit instance is a five-minute
exact hand computation given the definitions.
**Classification: KNOWN/ELEMENTARY-CONSEQUENCE** (as an example; no priority claimed).

### C3. Generalized even-k Ferrers injection (Theorem 4, window-margin propagation)

The mechanism is in the Stanley–Zanello KOH/Ferrers-diagram lineage (SZ §3 uses Ferrers
arguments for k ≤ 5; window monotonicity propagation is standard practice in this literature).
We supply a complete proof because the paper uses it, but no method-level priority is claimed;
an expert will likely regard the statement as known-to-experts.
**Classification: KNOWN or ELEMENTARY-CONSEQUENCE** (proof included for completeness; not a
claimed contribution).

### C4. Method: quasipolynomial partial fractions + Newton forward positivity + exact finite certificate

Sylvester-wave/quasipolynomial machinery and Newton-basis positivity are classical; KUW use the
same philosophy with different technology (CAD). No method novelty claimed anywhere in the paper.
**Classification: KNOWN.**

### C5. The 15,960-class machine certificate artifact for this slice

New artifact (not a new theorem): an independently regenerable, tamper-detectable exact
certificate with hash e3930e99…0e95. Value is reproducibility engineering.
**Classification: apparently new artifact; no mathematical priority claimed.**

## Hypothesis-coverage check (no accidental subsumption)

| source | proved parameter region | covers (k,b,m) = (8,12,≥13)? |
|---|---|---|
| SZ 2020 Thms 2.2–2.5 | k ≤ 5 complete | no |
| KUW 2023 §4 | k=6, k=7 (their m=6,7), explicit exceptions | no |
| Pak–Panova 2013; Zanello 2015 | strict unimodality of single Gaussian polynomials [n choose k]: interior first differences ≥ 1 | gives only ≥1; our required bounds reach 7; no implication |
| Reiner–Stanton 1998 | predecessor conjecture (Gaussian differences, different shape) | no; SZ exhibit a k=3 counterexample to RS itself |
| Makowsky–Rakita 2021 | graph-polynomial unimodality, different domain | independent |
| O'Hara 1990; Zeilberger 1994 | unimodality of single Gaussian polynomials | background only |

## Significance (assessed separately from correctness)

- Resolves one infinite family instance ((k,b)=(8,12)) of a named published conjecture, including
  the exact sharpness boundary — a legitimate short note / experimental-math paper contribution.
- Does NOT resolve SZ at k=8 in general (other admissible b remain), does not improve KUW bounds,
  and claims no new technique. Expected audience: q-series/additive combinatorics specialists.
- Honest significance grade: moderate-but-real; the certificate methodology may be the more
  reusable part.

## Residual unverified items (recorded, none load-bearing)

- Paywalled venue confirmation of page ranges for SZ/KUW beyond arXiv journal-ref fields
  (referee axis viii marks UNVERIFIED).
- Castillo–Li–Zhang (Ann. Comb. 23 (2019) 589–611), Dousse–Kim (arXiv:1806.04964), Keith (2021):
  exact statements not audited (no access); none is cited by any claim in the paper and none
  concerns Gaussian-polynomial differences of SZ shape in the audited parameter region.
- A complete MathReviews-level sweep 2020–2026 was not possible; this is precisely why C1 is
  graded "genuinely new CANDIDATE requiring external confirmation", not "genuinely new".
