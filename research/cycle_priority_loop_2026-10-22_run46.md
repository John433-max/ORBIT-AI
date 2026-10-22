# ORBIT Improvement Run 46

## Baseline
- doctor: READY (API deps warning, Ollama optional refused)
- smoke accuracy: 100% (2101/2101)
- failing probes: "how does binary search work" → calculator "Could not evaluate."

## Chosen priority
Coding/search/identity paths were already green. Highest remaining bug: conceptual
"how does X work" explainers routed to CalculatorAgent because science_math matched
the English word "work" as physics W=F·d.

## Changes
- science_math.looks_like_science_math: early reject for "how does/do … work" unless
  force/energy/physics context; removed bare "work" from single-token keys; added
  "work done" / "calculate work" multi phrases.
- agents._is_computational_math + _route calculator branch: same conceptual guard
  so bare "factorial" cannot steal "how does factorial work".

## Tests
- test_thinking + test_code_route_search + test_provider_fallback: 23 passed
- unit -k science|math|factorial|route: 16 passed, 1 skipped
- probes: binary-search explainer → research offline; factorial of 5 → 120;
  coding/search/identity unchanged; lab "tiny language model" still lab.

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| how does binary search work | calculator fail | research offline |
| how does factorial work | calculator fail | main_chat |
| factorial of 5 | 120 | 120 |
| physics work done | calculator | calculator |
| coding/search/identity | green | green |
| smoke | 2101/2101 | (not re-run full; targeted tests green) |

## GitHub push: pending (focused science_math.py + agents.py)

## Next priority remaining
GitHub parity of this routing fix; optional expand eval row for "how does X work";
serve/deps docs if needed.
