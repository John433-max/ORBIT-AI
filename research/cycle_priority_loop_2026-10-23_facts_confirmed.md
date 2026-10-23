# ORBIT Improvement Run — 2026-10-23 (static facts confirmed + unit tests)

## Baseline
- doctor: READY (PyYAML WARNING optional; API deps WARNING fastapi/uvicorn optional; Ollama OPTIONAL connection refused)
- smoke accuracy: 2105/2105 = 1.0 (evals/results/2026-10-23_041333_eval.json) before expanded smoke
- failing probes: none
  - coding: `write a python function that adds two numbers` → coding_agent, Verified `add(a, b)`
  - search: `search for recent news about fusion energy` → research_agent, honest "No live web available…"
  - identity: `what is your name` → main_chat_agent, "I'm ORBIT…"
  - capitals: Paris / Tokyo with offline label

## Chosen priority
Priorities 1–3 already green. Confirm expanded smoke (static capital facts + news honesty) and push GitHub parity for the unpushed local commits.

## Changes
- Already in 6c011e2: `_offline_static_fact` in agents.py (Paris/Tokyo/Berlin/…); news/price/office-holder still honest no-live-web; smoke +4 rows.
- 808bf15: unit tests `tests/unit/test_offline_static_facts.py` (capitals, news skip, labeled handle, fusion still offline).

## Tests
- doctor: READY
- probes: coding / search / identity / capitals pass
- unit: test_offline_static_facts + test_code_route_search + test_thinking + test_permissions_and_state = 32 passed
- full eval: **2109/2109 = 100%** (evals/results/2026-10-23_042532_eval.json)
  - search 13→17 (new fact rows); coding 2030/2030; rag 10/10; permission 11/11

## Benchmark before → after
| Metric | Before | After |
|---|---:|---:|
| smoke n / ok | 2105/2105 | 2109/2109 |
| accuracy | 1.0 | 1.0 |
| search rows | 13/13 | 17/17 |
| capital of France | offline fact (local) | offline fact, smoke-locked |
| news fusion | No live web | No live web |
| doctor | READY | READY |

## GitHub push
YES — 6c011e2 + 808bf15 (static facts + unit tests). origin/main was 9d68aeb; CI on that commit was success.

## Next priority remaining
1. Model provider defaults — auto already prefers Ollama when healthy, TinyLM fallback. Ollama currently refused; no change needed until a healthy Ollama is present.
2. Serve/deps — already optional WARNING; README points at requirements-api.txt.
3. Optional: more stable offline facts only if they stay labeled and do not steal news.
