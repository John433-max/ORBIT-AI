# ORBIT Improvement Run — 2026-10-19 (document route before research)

## Problem
Phrases like "answer from documents", "from your documents", and "search from the documents"
routed to main_chat or research instead of DocumentAgent, so empty-RAG asks got a generic
chat hedge rather than the honest "No documents loaded" reply.

## Research
Local routing order in Orchestrator._route: research matcher ran before document and matched
any "search …" string. thinking.py already had broader document patterns (plural documents,
answer/from documents); agents.py lagged.

## Finding
Minimal fix: evaluate document/RAG patterns first (aligned with thinking.py), then research.

## Implementation
- agents.py `_route`: move + expand document regex before research branch.
  - plural `documents?`
  - `from (your|my|the|uploaded)? documents?`
  - `(answer|query|search|look) … from … documents?`
  - knowledge base / indexed documents

## Files Changed
- agents.py

## Tests
- Manual probes: coding, search offline, identity, document empty phrases, permission deny, calc — all correct.
- pytest tests/unit/test_thinking.py tests/unit/test_code_route_search.py: 14 passed
- Prior eval baseline: 2083/2083 accuracy 1.0 (not re-run full; routing-only change)

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| answer from documents | main_chat generic | document honest empty |
| search from the documents | research offline | document honest empty |
| from your documents | main_chat generic | document honest empty |
| coding / search news / identity | pass | pass |
| smoke accuracy (prior) | 2083/2083 | unchanged expected |

## Result
Real improvement on empty-RAG honesty without breaking coding or live-search-offline paths.

## Next priority remaining
- GitHub push of this agents.py fix
- Model provider prefer Ollama when healthy
- Serve/deps docs (fastapi already WARNING in doctor)
