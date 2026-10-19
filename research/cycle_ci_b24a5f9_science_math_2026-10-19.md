# Improvement Cycle — CI 39298876642 (b24a5f9) + science_math restore

## Problem
GitHub Actions Tests run 39298876642 failed on commit b24a5f9
("fix(agents+science_math): restore full modules after accidental trunc…").
That commit replaced `agents.py` and `science_math.py` with the literal
`PLACEHOLDER`, so pytest exited 2 during collection/import.

Later commits restored `agents.py`. `science_math.py` remained truncated
(header only, then a 382-line subset missing factorial / constants /
power / compound interest). Eval science+math rows failed as a result.

## Baseline
- doctor: READY (PyYAML warning, API deps optional, Ollama offline optional)
- smoke: 2076/2083 = 99.66% (math 6/9, science 1/5; coding/search/rag/permission/lab 100%)
- probes:
  - coding ("write a python function that adds two numbers") → coding_agent, real `def add`, Verified
  - search ("search for recent news about fusion energy") → research_agent, honest no-live-web
  - identity ("what is your name") → main_chat_agent, "I'm ORBIT…"

## Chosen priority
GitHub CI (queue #4) blocked by truncated `science_math.py`. Coding/search/identity
already green. Restoring the full closed-form module fixes the import surface
and the science/math eval rows without touching routing.

## Research
Prior good content was commit 6684985 (`def solve_science_math` present,
517 lines). orbit_clean/orbit_fixed copies were a 382-line subset that
omits try_factorial / try_constants / try_power / try_compound_interest.
Those four helpers are exactly the failing eval ids (math_fact, const_c,
power_2_10, compound) plus the science rows that depend on looks_like_science_math
to stay off the code_synth path.

## Implementation
Restored `science_math.py` from 6684985 (517 lines). No agents.py change.

## Validation
- doctor READY
- unit (excl. code_synth): 78 passed, 1 skipped
- probes: coding / search / identity unchanged; science prompts now hit calculator
  with closed forms (d/dx(x^2)=2*x, 100 km=100000 m, circle area, 5!=120,
  c≈299792458, 2^10=1024, compound A=1157.6250)
