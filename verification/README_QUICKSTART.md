# math06-verification — runnable proof package

Theorem: F_l(q) = [l+8 choose 8]_q - q^(4l-18)[12 choose 6]_q is unimodal for every integer
l >= 6, nonnegative for every l >= 5, and non-unimodal at l = 5.

Requirements: Python 3 (tested on 3.15.0), standard library only, exact integer arithmetic.

    python3 generate_certificate.py --out certificate.json   # rebuild from definitions (~1 s)
    python3 verify_certificate.py --cert certificate.json --sample 12   # full value check (~65 s)
    python3 independent_check.py --n 80                       # direct theorem check, no certificate (~0.2 s)
    python3 r1_decisive.py                                    # third-route decisive check (~12 s)

Expected outputs and the reference certificate hash: EXPECTED_RESULTS.md.
Expected reference hash: e3930e99e9888acdd7efdab39e65519476f0a907f9ff7637e40b40f9cff60e95
The verifier exits non-zero on missing, truncated, structurally incomplete, or value-tampered
certificates. Hash integrity is not theorem correctness: the mathematical chain is
paper.tex Sections 5-8 (hand proofs) + this package (finite exact certificate).
