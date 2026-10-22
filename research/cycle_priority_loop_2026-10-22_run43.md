# ORBIT Improvement Run — 2026-10-22 run43

## Baseline
- doctor: READY (API deps warning optional; Ollama offline optional)
- smoke accuracy: 2100/2100 = 100% (evals/results/2026-10-22_002352_eval.json)
- failing probes: none for coding/search/identity
- local defect: agents.py working tree was truncated mid-Orchestrator.handle
  (SyntaxError on fresh parse; runtime relied on stale .pyc)

## Chosen priority
1. Restore truncated agents.py from HEAD (integrity).
2. Fix file-inventory phrases ("what files do you have") that weak-fell
   through MainChat hedge → research "no live web" instead of sandbox list.

## Changes
- Restored agents.py from git HEAD (799 lines, complete handle return).
- Expanded MainChatAgent list-files regex:
  list (my|the)? files / what|which|show files / what files do you have /
  show me my files.
- Unit test test_file_inventory_phrases_stay_sandbox_not_research.

## Tests
- AST parse OK
- test_code_route_search 9 passed
- test_provider_fallback + test_thinking 14 passed
- Probes: coding → real def add Verified; search → honest no live web;
  identity → I'm ORBIT; what files → sandbox listing (not research)

## Benchmark before → after
| Metric | Before | After | Difference |
|---|---:|---:|---:|
| agents.py parse | SyntaxError (truncated) | AST OK | fixed |
| "what files do you have" | research / no live web | sandbox list | correct route |
| smoke accuracy | 100% | 100% (not re-run full) | held |
| unit route tests | 8 | 9 | +1 |

## Result
Real improvement: restored corrupted agents.py; file inventory no longer
misroutes to research. Coding/search/identity paths remain correct.

## Next priority remaining
1. GitHub parity push of agents.py + unit test (this fix).
2. Eval expansion only if new gaps appear (already 2100 rows).
3. fastapi/uvicorn optional serve path / Ollama when available.
