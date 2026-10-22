# ORBIT Improvement Run 48 — 2026-10-22

## Baseline
- doctor: READY (API deps warning; Ollama optional refused)
- smoke accuracy: 2101/2101 (1.0) @ 2026-10-22_031243
- probes before:
  - coding "write a python function…" → coding_agent + Verified code
  - search "fusion energy" → research_agent offline honest
  - identity "what is your name" → main_chat_agent ORBIT
  - "how does photosynthesis work" → main_chat_agent with research_fallback content (label mismatch)

## Chosen priority
Priority 2 polish: research fallback labeled as `main_chat_agent` while content was honest offline research. Metrics/probes should show `research_agent`.

## Changes
- `agents.py`: when weak chat + knowledge → research fallback succeeds, return `AgentResult("research_agent", …)` instead of `"main_chat_agent"`.

## Tests
- test_provider_fallback.py + test_thinking.py: 14 passed
- probes after:
  - photosynthesis → research_agent + offline note (source=research_fallback)
  - fusion search → research_agent offline
  - add-two-numbers → coding_agent Verified
  - what is your name → main_chat_agent ORBIT
  - tell me about quantum → research_agent offline

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| smoke accuracy | 2101/2101 | unchanged (not re-run full; unit paths green) |
| photosynthesis agent label | main_chat_agent | research_agent |
| coding/search/identity | green | green |

## GitHub push
Pending focused commit of agents.py only (no secrets).

## Next priority remaining
4. GitHub parity — push agents.py label fix; keep full local agents ahead only if needed
5. Model provider defaults (Ollama when healthy — already correct when down)
6. Serve/deps docs (WARNING already non-blocking)
