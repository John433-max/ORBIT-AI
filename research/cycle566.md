# Improvement Cycle 566

## Problem
Tests run 38111075836 (commit 340ff3b, Cycle 565) failed unit tests:

```
tests/unit/test_thinking.py::test_code_verb_factorial_is_code_not_search
assert not _wants_code_written("factorial of 5")
AssertionError: assert not True
```

## Root cause
Cycle 565 correctly treats "code" as a write-verb so "code a factorial function" synthesizes.
`_wants_code_written` then falls through to `code_synth.match_template`, which hits the factorial template for "factorial of 5".

Locally this was masked: local `science_math.looks_like_science_math` includes the "factorial" keyword and returns False first.
On GitHub main, `science_math.py` does not list "factorial", so the template match wins and the new unit test fails.

## Research
SOURCE: CI logs for https://github.com/John433-max/ORBIT-AI/actions/runs/38111075836
DATE: 2026-10-11
TECHNIQUE: Explicit numeric-math guard before template match, independent of science_math keyword list.
WHAT IT IMPROVES: Coding-path routing does not steal pure factorial evaluations.
REQUIREMENTS: No new deps.
TRADE-OFFS: "factorial of N" / "N!" stay math even if a template name matches. Write-verb asks ("code a factorial function") still synthesize.
RELEVANCE TO ORBIT: Unblocks CI after Cycle 565; keeps coding vs math separation.
EXPECTED BENEFIT: Unit test passes on CI science_math; probes unchanged.

## Implementation
`agents.py` `_wants_code_written`: after write-verb / leetcode / starts-with checks, return False for `\bfactorial\s+(?:of\s+)?\d+` and `\d+\s*!`.

## Tests
- Simulated CI science_math (no factorial keyword): `factorial of 5` False; `code a factorial function` True; `code factorial` True.
- `pytest tests/unit/test_thinking.py`: 10 passed.
- Probes: add function Verified; code factorial Verified; factorial of 5 = 120; fusion search has results; name is ORBIT.
- Smoke eval: 1817/1817 (100%), coding 1765/1765.

## Benchmark

| Metric | Before (CI) | After | Difference |
|---|---:|---:|---:|
| unit test_code_verb_factorial | fail | pass | fixed |
| smoke accuracy | 1817/1817 (claimed by 565) | 1817/1817 | unchanged |
| probe "factorial of 5" | would synthesize on CI | 5! = 120 | fixed |
| probe "code a factorial function" | Verified | Verified | unchanged |

## Result
Kept. Smallest routing guard so numeric factorial is math even when science_math on main lacks the keyword.

## Next Research Target
Optional: push local science_math factorial solver so GH calculator path matches local. Remaining: more Easy templates / fastapi extras already documented.
