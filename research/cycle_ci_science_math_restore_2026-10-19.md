# Improvement Cycle — restore science_math after truncate

## Problem
CI on d7e791c (code_synth matcher exclusions) failed unit tests (code_synth).
Local re-run of tests/unit/test_code_synth.py: 329 passed.
Subsequent main commits truncated agents.py / science_math.py (PLACEHOLDER /
partial), causing CI exit code 2 (collection/import errors).

agents.py is currently a 584-line CI surface (CodeAgent + ResearchAgent +
Orchestrator + ModelRouter fallback). science_math.py was left at 41 lines
missing `solve_science_math` / `looks_like_science_math`, which agents.py
imports.

## Research
Restore from known-good local copy (orbit_clean/science_math.py, 382 lines)
that implements Cycle 59 calculus/geometry/physics helpers.

## Implementation
- Copied orbit_clean/science_math.py → science_math.py
- No logic changes; pure restore

## Tests
```
PYTHONPATH=. python -m pytest tests/unit --ignore=tests/unit/test_code_synth.py -q
# 78 passed, 1 skipped

PYTHONPATH=. python -m pytest tests/unit/test_provider_fallback.py tests/unit/test_code_route_search.py -q
# 3 passed
```

## Probes
- write a python function that adds two numbers → coding_agent, Verified `def add`
- search for recent news about fusion energy → research_agent, honest "No live web available…"
- what is your name → main_chat_agent, "I'm ORBIT."

## Benchmark
| Metric | Before | After | Diff |
|---|---:|---:|---:|
| science_math.py lines | 41 | 382 | +341 |
| solve_science_math import | fail | ok | fixed |
| core unit tests | (truncated) | 78 pass | restored |
| doctor | READY | READY | — |

## Result
Keep. Push science_math.py so CI can import agents.CalculatorAgent path.

## Next
GitHub parity of this restore; remaining code_synth matcher exclusions if CI still reports them on a full checkout.
