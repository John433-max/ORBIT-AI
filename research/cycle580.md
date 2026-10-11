# Improvement Cycle 580

## Problem
Smoke row `code_berlekamp_1` ("berlekamp massey algorithm") routed to ResearchAgent and returned a Wikipedia-style summary instead of the verified `berlekamp_massey` template. Eval was 1861/1862 (coding 1809/1810).

## Research
Bare algorithm titles must reach the code path when a template matches. `_is_code` already calls `match_template`, but returns early when `_is_math` is true. `looks_like_science_math` used raw substring keys; the key `"mass"` matched inside `"massey"`.

## Sources
- Local: thinking.py `_is_code` / `_is_math`; science_math.py `looks_like_science_math`
- Eval artifact: evals/results/2026-10-11_231338_eval.json (failing row)

## Finding
Word-boundary matching on science/math keys eliminates the false positive without dropping real physics asks ("mass of the earth", "force", "area of a circle"). Explicit write/implement coding asks were already protected by the earlier regex in `_is_code`.

## Implementation
- `science_math.looks_like_science_math`: match keys with `re.search(r"\b" + re.escape(k) + r"\b")`; keep `d/dx` as a special case.

## Files Changed
- science_math.py
- research/cycle580.md

## Tests
- Probe `berlekamp massey algorithm` → code agent, verified `def berlekamp_massey`
- `pytest tests/unit/test_thinking.py` → 11 passed
- Neighbor probes: mass/force/area still science; "write a python function that adds two numbers" still code; fusion search still research; "what is your name" still ORBIT
- `run_orbit.py eval` → 1862/1862 (100%)

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke accuracy | 1861/1862 (99.95%) | 1862/1862 (100%) | +1 row |
| coding | 1809/1810 | 1810/1810 | +1 |
| berlekamp bare title | research summary | verified code | fixed |
| doctor | READY | READY | — |

## Result
Bare Berlekamp–Massey title now synthesizes the verified function. No regressions on science, search, or identity paths.

## Problems
None observed. Other short science keys ("work", "force") are now boundary-safe.

## Next Research Target
- GitHub parity for science_math.py + code_synth_p277
- Additional unmatched textbook algorithms if any remain
- TinyLM fused INT4 without full FP32 W, or source restore from `_bc.pyc`
