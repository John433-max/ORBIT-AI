# Cycle CI — hedge-route vs offline static facts (2026-10-23)

## Trigger
Workflow CI failed on commit `372d919` (docs-only: confirm static-fact smoke 2109/2109).
https://github.com/John433-max/ORBIT-AI/actions/runs/39900327280

## Root cause
`feat(research): offline static facts` made "what is the capital of France"
return Paris via `_offline_static_fact` instead of the research_fallback /
no-live-web path. `test_generic_hedge_question_uses_research` still expected
the hedge→research path (or Paris as an allowed body), and failed once the
MainChat short-circuit / static path changed labels.

## Fix (already on main)
- `4c87b33` / `a13e330`: adapt the unit test to use an unmatched fact
  ("who invented the telephone") so it still asserts research_fallback /
  no-hedge behavior without colliding with offline capital facts.
- Local `agents.py`: stop short-circuiting static geography in MainChatAgent;
  let weak-chat + `_offline_static_fact` hit ResearchAgent so the
  `research_fallback` source label is consistent.

## Verification
- doctor: READY (fastapi optional warning only)
- smoke: 2109/2109 (100%) — coding 2030, search 17, rag 10, permission 11
- unit: test_provider_fallback + offline_static_facts + code_route_search + thinking → 30 passed
- probes:
  - write a python function that adds two numbers → coding_agent, real `def add`, Verified
  - search for recent news about fusion energy → research_agent, honest no-live-web
  - what is your name → main_chat_agent, ORBIT identity
  - capital of France → research_agent, Paris (offline known fact)

## Result
CI failure was test drift after static-fact feature; test adapted on main.
No product regression. Smoke and probes remain 100%.
