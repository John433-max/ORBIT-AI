# Improvement Cycle 578

## Problem
Classic number-theoretic and transform algorithms were still stubs or mis-routed:
- NTT / modular FFT / number-theoretic transform → NotImplementedError draft
- FFT polynomial multiplication → draft
- Miller–Rabin primality → stolen by `rabin_karp`
- Pollard's Rho factorization → draft
- Baby-step giant-step discrete log → draft
- Matrix exponentiation → not matched (power template did not claim it)

## Research
- NTT: standard modular FFT over prime field 998244353 with primitive root 3 (common in competitive programming / educational NTT).
- FFT: Cooley–Tukey radix-2 (1965) with complex twiddles, rounded to integers for exact small-integer poly mul.
- Miller–Rabin: probabilistic primality (Miller 1976, Rabin 1980); fixed small bases suffice for educational deterministic-ish checks.
- Pollard's Rho: 1975 cycle-finding factorization; Brent-style educational form.
- Discrete log: Shanks baby-step giant-step.
- Matrix exponentiation: binary exponentiation on matrices (CLRS-style).

## Sources
- Cooley, J. W., & Tukey, J. W. (1965). An algorithm for the machine calculation of complex Fourier series.
- Miller, G. L. (1976). Riemann's hypothesis and tests for primality.
- Rabin, M. O. (1980). Probabilistic algorithm for testing primality.
- Pollard, J. M. (1975). A Monte Carlo method for factorization.
- Shanks, D. baby-step giant-step (classic discrete log).
- Standard NTT parameters (mod 998244353, root 3) used in educational/CP references.

## Finding
Phrase-specific matchers plus self-checking examples close the six gaps without stealing existing Rabin–Karp, power, or prime-factor templates. Pack-order (newest first) plus name-token scoring keeps Miller–Rabin preferred over Rabin–Karp when "miller" is present.

## Implementation
- New pack `code_synth_p276.py` with six templates, narrow regex matchers, and deterministic examples.
- Loader prepends `code_synth_p276`.
- Unit test `test_p276_ntt_fft_miller_pollard_bsgs_matpow`.
- Six smoke rows in `evals/datasets/smoke.jsonl`.

## Files Changed
- `code_synth_p276.py` (new)
- `code_synth.py` (loader list)
- `tests/unit/test_code_synth.py`
- `evals/datasets/smoke.jsonl`
- `research/baseline.md`, `findings.md`, `implemented.md`

## Tests
- `test_p276_ntt_fft_miller_pollard_bsgs_matpow`: PASSED
- Direct example execution of all six templates: all OK
- Neighbor probes: rabin_karp, power, prime_factors, is_prime unchanged
- OrbitAI.ask on all six prompts: Verified, no NotImplementedError

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| Templates loaded | 1732 | 1738 | +6 |
| Smoke rows | 1850 | 1856 | +6 |
| New asks verified | 0/6 (stubs/wrong) | 6/6 | +6 |
| Unit test p276 | n/a | PASS | — |

## Result
Six previously unmatched or mis-routed classic algorithms now synthesize verified educational implementations. No regressions on neighboring matchers.

## Problems
None observed. Pollard Rho example factors are stable for the chosen small composites under the educational implementation.

## Next Research Target
Continue unmatched textbook algorithms, or shift to GitHub pack/agents parity / TinyLM fused INT4 if coding coverage is no longer the highest-value gap.
