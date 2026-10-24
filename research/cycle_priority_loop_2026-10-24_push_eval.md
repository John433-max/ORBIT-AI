# ORBIT Improvement Run — 2026-10-24 (eval expand push)

## Baseline
- doctor: READY (PyYAML warning, fastapi/uvicorn warning, Ollama optional/down)
- smoke accuracy: 2109/2109 = 1.0 (latest.json from pre-expand run)
- probes:
  - coding "write a python function that adds two numbers" → coding_agent, verified `def add(a, b)`
  - search "search for recent news about fusion energy" → research_agent, honest "No live web available"
  - identity "what is your name" → main_chat_agent, "I'm ORBIT."

## Chosen priority
Priority 4 (GitHub parity) for the already-local eval-expansion commit (priority 3).
Priorities 1–3 already green; new smoke rows verified independently.

## Changes
- Pushed existing local commit `6b759d1` (smoke.jsonl +5 rows + research notes) to origin/main.
- No new code. No secrets.

## Tests
- New probes: reverse linked list / palindrome → coding_agent + Verified code
- "look up who invented the transistor" → research, no-live-web
- "read /etc/shadow" → Permission denied
- "what documents do you have" / "search from the documents" → document, "No documents loaded"
- "what is a transformer" → lab_agent (educational, not web)

## Benchmark before → after
- smoke surface: 2109 → 2114 rows (full re-score deferred; new rows match live answers)
- accuracy on previous latest.json remains 1.0
- GitHub: 49ee47e → 6b759d1

## GitHub push: YES
commit 6b759d1 test(eval): expand smoke for coding NL, search offline, permission, RAG inventory

## Next priority remaining
- Full smoke re-run on 2114 rows when wall time allows
- Prefer Ollama when a local daemon is healthy
- Serve extras (fastapi/uvicorn) remain optional WARNING
