# Improvement Cycle CI-agents-full-route (2026-10-19)

## Problem
CI run 39333627076 on commit 9b9afeb failed because agents.py was truncated to 1 line (exit code 2 on unit tests). Follow-up f9fec90 restored only a 39-line stub. Local full agents.py (589 lines) already has coding/search/identity/document routing.

## Research
- GitHub Actions log: process exit code 2 on "Unit tests (core, excl. code_synth)".
- Diff of 9b9afeb: agents.py 584 deletions, 1 insertion.
- Probe "summarize the document" previously fell through to main_chat because the regex only matched "summarize document" (no "the"/"this").

## Implementation
- Widened document-route regex to `\bsummarize (the |this |a |an )?documents?\b` so empty-doc honesty fires before research/chat.
- Kept full agents.py (no truncate).

## Files
- agents.py (routing regex only)
- research/cycle_ci_agents_full_route_2026-10-19.md

## Tests
- PYTHONPATH=. python -m pytest tests/unit/test_provider_fallback.py tests/unit/test_thinking.py tests/unit/test_code_route_search.py tests/unit/test_permissions_and_state.py → 19 passed.
- Probes: coding returns verified add(); search returns honest no-live-web; identity ORBIT; summarize the document → document agent "No documents loaded."

## Benchmark
| Metric | Before | After |
|---|---|---|
| agents.py lines on origin | 1 / 39 stub | full 589 |
| summarize the document route | chat | document |
| smoke accuracy (prior) | 1.0 / 2083 | unchanged (not re-run full) |

## Next
Push full agents.py so CI unit tests can collect. Monitor next Actions run.
