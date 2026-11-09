# Unimodality of a Stanley–Zanello slice: F_ℓ = [ℓ+8 choose 8]_q − q^(4ℓ−18)[12 choose 6]_q

A self-contained proof package for the following theorem, proved for the fixed
parameter slice `(k, b) = (8, 12)` of the difference family of Stanley and Zanello:

> For every integer ℓ ≥ 6, the polynomial
> F_ℓ(q) = [ℓ+8 choose 8]_q − q^(4ℓ−18) [12 choose 6]_q
> is unimodal, and the bound is best possible: F_5 is coefficientwise
> nonnegative but not unimodal (central coefficients 15, 16, 15, 16, 15).

Structure: a hand proof reduces the infinite family to 19 explicit inequalities
per ℓ ≥ 840, encoded as 15,960 degree-≤7 Newton-basis certificates on residue
classes modulo 840, plus an exact finite check for 6 ≤ ℓ ≤ 839. All computations
use exact integer arithmetic (no floating point) and run on the Python standard
library alone.

## Status of claims

- **Internally verified** — regenerated certificate, multiple cross-checking
  verification routes (inclusion–exclusion vs dense truncated multiplication;
  distinct algorithms, not independently authored clean-room implementations),
  full corruption/tamper battery, and an adversarial AI review pass with zero
  blocking findings (see `docs/` and `verification/`).
- **Ready for independent human review.** This is *not* a peer-reviewed or
  published result.
- **Novelty is provisional and priority remains unresolved.** The statement is
  an instance of Conjecture 1.1 of Stanley–Zanello (arXiv:1711.10033); the
  proved literature reaches k ≤ 7 (Koutschan–Uncu–Wong, arXiv:2302.04067). No
  prior proof of this (k, b) = (8, 12) slice was located, but no established
  originality claim is made. See `docs/NOVELTY_AUDIT.md`.
- Scope: the fixed (k, b) = (8, 12) slice only, not the general
  Stanley–Zanello conjecture.

## Reproduce in three commands

Requires Python 3.10+ (tested on 3.15.0), standard library only, ~70 seconds total.
The certificate payload embeds no runtime metadata, so regeneration is byte-identical
across Python versions.

```bash
cd verification
python3 generate_certificate.py --out certificate.json      # ~1 s
python3 verify_certificate.py --cert certificate.json --sample 12   # ~65 s
python3 independent_check.py --n 80                          # <1 s
```

Expected: all three exit 0 with `VERDICT: PASS`, and the regenerated
certificate reproduces byte-for-byte:

```
d6454b2bcb3197693ea89f3214ba3319f3e2a1f3764bda0b2e7aa12feac123ec  certificate.json
```

The verifier recomputes the entire finite base (all 19 inequalities for every
6 ≤ ℓ ≤ 839) natively, so a tampered finite-range claim cannot pass. An
cross-check route (`r1_decisive.py`, ~12 s) re-derives stored certificate
values through yet another code path. `docs/CHANGES.md` records the
manuscript-revision history, including the Section 6.2 asymptotic-degree
correction (residual degree is exactly 5, not 3).

## Layout

| path | contents |
|---|---|
| `paper/revised.pdf` | the manuscript (9 pages) |
| `paper/revised.tex`, `references.bib`, `revised.bbl` | LaTeX source (compiles with tectonic or pdflatex+bibtex) |
| `verification/` | standalone exact-integer scripts + the certificate + expected results + quickstart |
| `verification/runs/` | captured reproduction logs |
| `docs/` | proof audit, Section 6.2 analysis, novelty audit, change log |

The verifier's sampled route and the finite-base recomputation use the dense
code path; the generator uses inclusion–exclusion over restricted partition
functions. These are different algorithms sharing some helper code, and are
described as cross-checking routes rather than independent implementations.

## License

MIT (see `LICENSE`). Contents of `verification/` are additionally dedicated to
the public domain under CC0 1.0 (see `LICENSE-CC0`) to the extent possible
under law. Author attribution: the manuscript carries an author placeholder
pending owner completion; no AI system is presented as an author, and no AI
review is presented as peer review.
