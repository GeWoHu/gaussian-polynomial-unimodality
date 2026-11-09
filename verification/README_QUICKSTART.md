# math06-verification — runnable proof package

Theorem: F_l(q) = [l+8 choose 8]_q - q^(4l-18)[12 choose 6]_q is unimodal for every integer
l >= 6, nonnegative for every l >= 5, and non-unimodal at l = 5.

Requirements: Python 3 (tested on 3.15.0), standard library only, exact integer arithmetic.

    python3 generate_certificate.py --out certificate.json   # rebuild from definitions (~1 s)
    python3 verify_certificate.py --cert certificate.json --sample 12   # full value check + native finite base (~66 s)
    python3 independent_check.py --n 80                       # direct theorem check, no certificate (~0.2 s)
    python3 r1_decisive.py                                    # cross-check route, dense third path (~12 s)

Expected outputs and the reference certificate hash: EXPECTED_RESULTS.md.
Expected reference hash: d6454b2bcb3197693ea89f3214ba3319f3e2a1f3764bda0b2e7aa12feac123ec
The certificate payload carries no runtime metadata, so regeneration is byte-identical across
Python versions (>= 3.10).
The verifier exits non-zero on missing, truncated, structurally incomplete, or value-tampered
certificates (including a tampered finite-base claim, which the verifier now catches by
recomputing 6..839 natively). Hash integrity is not theorem correctness: the mathematical chain
is paper/revised.tex Sections 5-8 (hand proofs) + this package (finite exact certificate).
The code paths cross-check each other (inclusion-exclusion vs dense truncated multiplication);
they are distinct algorithms, not independently authored clean-room implementations.
