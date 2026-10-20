# Cycle: agents.py PLACEHOLDER restore (2026-10-19)

## Trigger
GitHub Actions Tests run 39333627001 failed on commit 9b9afeb
(title: fix(routing): document/RAG before research for empty-doc honesty).

## Problem
`agents.py` on `main` was repeatedly reduced to a literal stub
(`PLACEHOLDER` / `PLACEHOLDER_WILL_REPLACE` / 11 bytes). That breaks:
- `OrbitAI` import (`'{' was never closed` / SyntaxError)
- doctor (OrbitAI ERROR)
- coding / research / document routing
- CI unit tests that import Orchestrator / CodeAgent

## Baseline (local, before restore)
- doctor: NOT READY — OrbitAI syntax error agents.py:587
- agents.py: truncated mid-`return {` (~22KB incomplete)

## Fix
Restored full CI-surface `agents.py` (589 lines, ~22.5KB) matching
commit 4141e89 / API blob on main (sha a437fa5d...).

Routing order preserved: document/RAG before research for empty-doc honesty.

## Verification
- doctor: READY (2 non-blocking: fastapi optional, Ollama offline)
- probes:
  - write a python function that adds two numbers → coding_agent, `def add`, Verified
  - search for recent news about fusion energy → research_agent, honest "No live web"
  - what is your name → main_chat_agent, "I'm ORBIT..."
- tests/unit/test_provider_fallback.py: 1 passed

## GitHub
Full agents.py confirmed on main via API (size 22549).
Prior bad pushes of PLACEHOLDER_WILL_REPLACE were superseded.

## Next
- Eval expansion rows (coding + search + RAG-empty + permission denial)
- Optional: prefer Ollama when healthy
- Keep agents.py out of accidental truncate in CI restore commits
