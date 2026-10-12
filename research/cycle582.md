# Improvement Cycle 582

## Problem
Smoke dataset had 6 new coding rows (strassen, gaussian elimination, newton-raphson, hyperloglog, simhash, johnson's algorithm) that did not return real code:
- `code_synth_p278.py` existed but was invisible to directory listing, so Python could not import it (HyperLogLog / Cartesian / CMS missing).
- strassen was stolen by `matrix_multiply`.
- newton-raphson was classified as calc because science_math key `newton` matched via word boundary.
- gaussian / simhash / johnson had no template and fell through to NotImplemented drafts.

## Research
Bare algorithm titles must hit a verified template (same pattern as Berlekamp-Massey in Cycle 581). Word-boundary science keys must not steal algorithm names. Pack files must be importable (listdir-visible).

## Sources
- Local smoke.jsonl expect_contains for the six rows
- science_math.py looks_like_science_math (mass vs massey precedent)
- code_synth loader (Cycle 244 packs)

## Finding
Highest-value coding-path gap was the six new smoke rows plus an unimportable p278 pack.

## Implementation
- Rewrote `code_synth_p278.py` so it is listable and importable (cartesian_tree, count_min_sketch, hyperloglog).
- Added `code_synth_p279.py` with verified templates: strassen_mul, gaussian_elimination, newton_raphson, simhash, johnson_apsp.
- Registered p279 first in the code_synth loader.
- Excluded "strassen" from matrix_multiply matcher.
- Excluded newton-raphson / newton's method from looks_like_science_math.
- Narrowed critical_connections wrap so generic bridge phrases stay on find_bridges.

## Files Changed
- code_synth.py
- code_synth_p182.py
- code_synth_p278.py
- code_synth_p279.py
- science_math.py

## Tests
- synthesize_and_verify on the six prompts: all verified
- Thinker.classify: all six -> code
- targeted smoke score: 7/7 (including berlekamp)
- tests/unit/test_thinking.py: 11 passed
- tests/unit/test_code_synth.py::test_p248_aho_corasick_and_bridges: passed (after stale pyc clear)

## Benchmark
See eval after this cycle.

## Result
Coding path returns real verified functions for the six previously failing algorithm titles.

## Next Research Target
GitHub parity for p278/p279 + matcher fixes; optional further unmatched textbook algorithms.
