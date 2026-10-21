# ORBIT Improvement Run 23 — 2026-10-21

## Baseline
- doctor: READY (API deps warning optional; Ollama optional offline)
- smoke accuracy: 1.0 (2085/2085) from evals/results/latest.json @ 2026-10-21T01:12:46
- probes before fix:
  - coding: real add() + Verified
  - search: honest "No live web available…"
  - identity: "I'm ORBIT…"
  - list my documents: generic chat hedge (FAIL)

## Chosen priority
RAG-empty honesty / eval expansion — document inventory phrases ("list my documents",
"show me my documents", "which documents are loaded") were not matched by the document
route and returned the generic chat identity line instead of the honest empty-RAG reply.

Also repaired a truncated agents.py (handle() cut mid-AgentResult) left from an
interrupted prior edit; restored complete handle from HEAD while keeping the routing fix.

## Changes
- agents.py _route: expand document inventory regex for possessive/show/which forms
- tests/unit/test_code_route_search.py: test_document_inventory_phrases_route_to_document
- Restored complete Orchestrator.handle after accidental truncation

## Tests
- pytest tests/unit/test_code_route_search.py → 4 passed
- Live probes via OrbitAI.ask: coding / search / identity / three inventory phrases OK

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| smoke accuracy | 1.0 (2085) | unchanged (routing-only) |
| list my documents | chat hedge | No documents loaded… (document agent) |
| show me my documents | chat hedge | No documents loaded… |
| which documents are loaded | chat hedge | No documents loaded… |
| coding / search / identity | pass | pass |

## GitHub push
YES — focused agents.py + test + this research note.

## Next priority remaining
1. GitHub parity for remaining local-only surface
2. Model provider defaults (Ollama when healthy)
3. Serve/deps fastapi/uvicorn docs/CI
