# Improvement Cycle 625 — RAG-empty document routing

## Problem
Natural language like "answer from documents: …" and "summarize the document that does not exist …" scored as statement/chat and returned the toy-scale hedge instead of DocumentAgent's honest empty-RAG reply.

## Root cause
1. thinking.classify used singular document only.
2. ROUTES document pattern lacked answer-from-documents and summarize-the-document.
3. AGENT_SIGNALS document lacked from-documents phrases.

## Changes (local artifacts/orbit)
- thinking.py: plural documents?, answer/from-documents → docs.
- agents.py ROUTES + AGENT_SIGNALS document patterns expanded.
- smoke.jsonl +4 rows (rag/search/permission).

## Tests (local)
- Thinker.classify and Orchestrator probes: document_agent honest empty.
- Coding/search/identity/permission OK.
- test_thinking.py 13 passed.

## GitHub
Placeholder push briefly broke thinking.py; full agents.py + thinking.py re-push from local still required after this note.
