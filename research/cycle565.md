# Improvement Cycle 565

## Problem
Natural-language coding asks that use the verb "code" instead of "write/implement" were misrouted when the topic also matched a math keyword.

Probe: `code a factorial function`
- Thinker classified it as calc (science_math keyword `factorial`), calc failed ("expression must contain a number"), then fell back to live web search about factorial.
- Direct CodeAgent path executed the sentence as Python and returned a sandbox syntax error.
- Contrast: `write a python function that adds two numbers` and `factorial of 5` were already correct.

## Research
SOURCE: Existing ORBIT routing (`thinking._is_code`, `agents._wants_code_written`, `Orchestrator.route`). HumanEval-style natural language ("write a function…") is the established pattern; "code a function" is the same intent with a different verb.
DATE: 2026-10-11
TECHNIQUE: Treat `code` / `program` as write-verbs equivalent to implement/write, before the math-keyword short-circuit.
WHAT IT IMPROVES: Coding-path success on "code a … function" / "code <template>" without stealing numeric asks ("factorial of 5").
REQUIREMENTS: No new deps.
TRADE-OFFS: A bare "code …" prefix now prefers synthesis when it is not a fenced snippet. Pure math ("factorial of 5") is unchanged.
RELEVANCE TO ORBIT: Priority 1 coding path was returning search/syntax instead of real code.
EXPECTED BENEFIT: Probe returns verified `def factorial`; smoke stays ≥ previous accuracy.

## Implementation
- `agents.py`: `_wants_code_written` and `route()` `code_write` include `code|program`.
- `thinking.py`: `_is_code` and `_explicit_code_ask` same verb expansion (before math short-circuit).
- Smoke row `code_factorial_verb_1`.
- Unit test `test_code_verb_factorial_is_code_not_search`.

## Tests
- `pytest tests/unit/test_thinking.py`: 10 passed.
- Targeted OrbitAI.ask: code factorial Verified; factorial of 5 = 120; search fusion still research; identity ORBIT.

## Next
GitHub parity of this fix; remaining optional API extras already documented.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| doctor | READY | READY | — |
| smoke accuracy | 1816/1816 (100%) | 1817/1817 (100%) | +1 row, still 100% |
| coding category | 1764/1764 | 1765/1765 | +1 |
| probe "code a factorial function" | web search / syntax error | verified `def factorial` | fixed |
| probe "factorial of 5" | 5! = 120 | 5! = 120 | unchanged |
| probe fusion search | research + sources | research + sources | unchanged |
| probe name | I'm ORBIT | I'm ORBIT | unchanged |

## Result
Kept. Smallest routing fix: "code" is a write-verb. No regression.

## Next Research Target
GitHub parity of remaining local-only smoke rows (need matching templates on main). Optional fastapi extras already documented.
