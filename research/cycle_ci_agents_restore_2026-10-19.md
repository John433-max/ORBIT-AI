# Improvement Cycle — CI agents.py PLACEHOLDER restore (2026-10-19)

## Problem
CI run 39333846655 failed on commit f9fec90. Root cause observed on origin/main:
agents.py repeatedly degenerated to PLACEHOLDER_WILL_REPLACE / LOADING stubs
(0–few bytes), breaking unit tests and routing.

## Research
- Inspected local agents.py (589 lines, AST OK, Orchestrator.handle works).
- Probes: coding → code_synth Verified; research → honest no-live-web;
  identity → ORBIT; empty doc → document agent honest empty.
- GitHub API: agents.py on main restored at c09962b (blob a437fa5) with full
  CI surface matching local.

## Finding
Highest-value fix is GitHub parity of the working CI-surface agents.py.
Local coding/search/identity/document routes already pass.

## Implementation
- Local: kept working 589-line agents.py; unit tests 78 passed (excl. code_synth).
- Origin: concurrent restore commits (87016d3, c09962b) already pushing full agents.
- Local git had index/log stale-handle issues; content verified independently.

## Tests
- doctor: READY (API deps warning optional)
- pytest tests/unit (excl. code_synth): 78 passed, 1 skipped
- test_provider_fallback: 1 passed
- Probes: code, research, identity, empty-doc all correct

## Benchmark before → after
| Metric | Before (broken GH) | After (local + GH restore) |
|--------|-------------------:|---------------------------:|
| agents.py lines on main | 0 / PLACEHOLDER | ~589 |
| coding probe | fail/hedge | coding_agent + Verified |
| research probe | hedge | honest no-live-web |
| identity | risk of web/movie | ORBIT |
| unit tests | CI fail | 78 pass local |

## Result
Priority paths healthy locally. GitHub main restored agents.py in concurrent
commits. No further local code change required this run.

## Next Research Target
- Confirm CI green on c09962b
- Eval expansion (coding + search + RAG-empty + permission denial rows)
- Optional: full local agents.py (71KB+) parity if CI surface stays slim
