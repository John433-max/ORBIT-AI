# Cycle CI document-route + agents restore (2026-10-19)

## Trigger
CI run https://github.com/John433-max/ORBIT-AI/actions/runs/39333627076 failed on commit 9b9afeb
(`fix(routing): document/RAG before research for empty-doc honesty`).

## Root cause
That commit **truncated** `agents.py` (585 deletions → ~1.4 KB stub). Subsequent
attempts to restore via partial `create_or_update_file` / `push_files` also left
PLACEHOLDER / LOADING / 8-byte stubs on `main` when full content was not
embedded in the tool argument.

## Local fix (this cycle)
1. Restored full `agents.py` from known-good content (~22 KB).
2. Expanded document/RAG routing **before** research:
   - `search the documents…`, `knowledge base`, `RAG` / `retrieval`
   - Empty session → honest "No documents loaded…" (not research offline, not chat hedge)
3. Probes:
   - coding: `write a python function that adds two numbers` → coding_agent + real code
   - search: `search for recent news about fusion energy` → research_agent + no-live-web
   - identity: `what is your name` → ORBIT
   - docs: `answer from the documents` / `search the documents for fusion` → document + honest empty
4. Unit: `test_provider_fallback` + `test_thinking` + `test_code_route_search` → 15 passed

## GitHub status (at write time)
`agents.py` on `main` is still a stub from incomplete pushes. Full restore requires
pushing the complete ~22 KB file in one API call (content must be the full source,
not a placeholder). Local `/home/workdir/artifacts/orbit/agents.py` is the source of truth.

## Next
- Push full local `agents.py` in a single successful update (no truncation).
- Re-run CI; confirm Tests green.
- Eval expansion still queued after routing parity is stable on GitHub.
