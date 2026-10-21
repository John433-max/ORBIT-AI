# ORBIT Improvement Run 23 — 2026-10-21

## Baseline
- doctor: READY (PyYAML optional, fastapi/uvicorn warning, Ollama offline)
- smoke before this run: 2085/2085 = 1.0
- priority probes: coding (real add), search (honest no-live-web), identity (I'm ORBIT) all green
- remaining gap: document inventory phrasings ("list my documents", "show me my documents", "which documents are loaded", "list the documents") routed to main_chat generic hedge

## Chosen priority
Priority 3 — RAG-empty / eval expansion. Highest real miss after coding/search/identity.

## Research
thinking.py already classified these as docs. OrbitAI.chat uses Orchestrator.handle (no think method), so agents.py `_route` is the live path. Its document regex only matched bare "list documents" / "what documents".

## Changes
- agents.py `_route`: expanded document inventory regex (possessive / show / which). Concurrent commit 123baa6 already landed this on main during this run.
- tests/unit/test_code_route_search.py: `test_document_inventory_phrases_route_to_document` (landed as eacb970).
- evals/datasets/smoke.jsonl: rag_list_1..4 (this commit).

## Tests
- py_compile agents.py OK
- document inventory unit test OK; binary_search and look-this-up routes OK
- targeted score 9/9 (new rag rows + code/search/identity/perm/file_list)
- non-document regression: write-function-that-lists-documents stays code; list files stays chat
- full eval after fix: 2090/2090 = 100% (rag 10/10, coding 2021/2021, search 11/11, permission 11/11)

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| list my documents | main_chat hedge | document "No documents loaded…" |
| show me my documents | main_chat hedge | document "No documents loaded…" |
| which documents are loaded | main_chat hedge | document "No documents loaded…" |
| list the documents | main_chat hedge | document "No documents loaded…" |
| smoke accuracy | 2085/2085 (1.0) | 2090/2090 (1.0) |
| rag rows | 6/6 | 10/10 |

## GitHub push
YES — smoke.jsonl rag_list_1..4 + this note. agents.py + unit test already on origin/main (123baa6, eacb970, merge abd8042).

## Next priority remaining
1–3 green. 4 parity for this smoke commit. 5 Ollama still offline (TinyLM correct fallback). 6 serve/deps already documented and installed in CI.
