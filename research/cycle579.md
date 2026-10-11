# Improvement Cycle 579

## Problem
Coding agent still fell back (or weakly matched) on several textbook algorithms: Karatsuba integer multiplication, linear-sieve Möbius function, Berlekamp–Massey minimal linear recurrence, tree diameter, Lagrange polynomial interpolation, and virtual/compressed tree construction.

## Research
- Karatsuba (Anatoly Karatsuba, 1962): divide-and-conquer integer multiplication reducing the three multiplies of schoolbook to two recursive + one cross term, O(n^{log₂3}) ≈ O(n^1.58).
- Linear sieve for Möbius: Euler sieve variant that also fills μ(n) in O(n) by tracking least prime factor (standard CP technique; e.g. implementations on CP-Algorithms / Project Euler solvers).
- Berlekamp–Massey (1968/1969): finds the shortest LFSR / connection polynomial for a sequence over a field in O(n²).
- Tree diameter: two BFS (or DFS) farthest-node method on undirected trees.
- Lagrange interpolation: unique degree < k polynomial through k points; evaluated with exact fractions.
- Virtual tree: standard compressed-tree construction for a set of nodes in a rooted tree via binary-lifting LCA + inclusion of pairwise LCAs.

## Sources
- https://en.wikipedia.org/wiki/Karatsuba_algorithm
- https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html (linear sieve variants)
- https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Massey_algorithm
- Standard competitive-programming references for tree diameter and virtual trees (e.g. CP-Algorithms, Codeforces blogs).

## Finding
All six algorithms are compatible with the existing Template + self-check example mechanism. Phrase-specific matchers avoid stealing broad "multiply", "sieve", "tree", or "interpolate" templates. Virtual-tree implementation uses binary lifting (already a pattern in earlier packs) and is self-contained.

## Implementation
- New pack `code_synth_p277.py` with six Templates:
  - `karatsuba_mul`
  - `mobius_sieve`
  - `berlekamp_massey`
  - `tree_diameter`
  - `lagrange_interpolate`
  - `virtual_tree`
- Loader in `code_synth.py` now imports `code_synth_p277` first.
- Unit test `test_p277_karatsuba_mobius_berlekamp_diameter_lagrange_virtual` added.
- Six smoke rows appended to `evals/datasets/smoke.jsonl`.

## Files Changed
- code_synth_p277.py (new)
- code_synth.py (loader)
- tests/unit/test_code_synth.py
- evals/datasets/smoke.jsonl
- research/cycle579.md
- research/baseline.md
- research/implemented.md

## Tests
- `pytest tests/unit/test_code_synth.py::test_p277_...` → PASSED (1.0)
- Neighbor probes: "multiply two integers" still hits `multiply`; "sieve of eratosthenes" still hits `count_primes`.
- `run_orbit.py doctor` → Overall: READY.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| Unique templates | 1738 | 1744 | +6 |
| Smoke rows | 1856 | 1862 | +6 |
| New asks verified | 0/6 | 6/6 | +6 |
| Doctor | READY | READY | — |

## Result
Six previously unmatched textbook algorithms now synthesize verified source. No neighbor regressions. Educational coverage of number theory, recurrence, and tree techniques expanded.

## Problems
None observed. Virtual-tree example is minimal (two leaves + root); more complex trees can be added later if needed.

## Next Research Target
- Additional unmatched textbook items (e.g. slope trick, offline dynamic connectivity, Berlekamp–Massey over rationals, persistent segment tree as a distinct template).
- GitHub pack parity for p277+.
- TinyLM fused INT4 kernel that beats eager unpack, or source restore from `_bc.pyc` if still truncated.
