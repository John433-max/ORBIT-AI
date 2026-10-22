# ORBIT Improvement Run 49 — 2026-10-22

## Baseline
- doctor: READY (API deps WARNING optional; Ollama OPTIONAL connection refused; provider=auto → tinylm)
- smoke accuracy: 2101/2101 (1.0) → evals/results/2026-10-22_041111_eval.json
- by_category: coding 2030/2030, search 13/13, rag 10/10, permission 11/11, all others 100%
- probes:
  - coding "write a python function that adds two numbers" → coding_agent + Verified code_synth
  - search "fusion energy" → research_agent honest offline
  - identity "what is your name" → main_chat_agent ORBIT
  - "how does photosynthesis work" → research_agent offline (label fix from run 48 holds)

## Chosen priority
4. GitHub parity — local was ahead 1 (02dda9c label fix from run 48). Priorities 1–3 already green.

## Changes
- No new code this run. Confirmed baseline and pushed the pending commit.
- Restored accidental local delete of research/cycle_priority_loop_2026-10-22_run43.md (working tree only; not in the pushed commit).

## Tests
- run_orbit.py eval: 2101/2101 (100%)
- probes: coding / search / identity / photosynthesis all correct agents

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| smoke accuracy | 2101/2101 (prior latest.json) | 2101/2101 (2026-10-22_041111) |
| GitHub main | 41fa8c0 | 02dda9c |
| coding/search/identity | green | green |

## GitHub push
YES — 41fa8c0..02dda9c main → main
Commit: fix(route): label knowledge research_fallback as research_agent
Files: agents.py, research/cycle_priority_loop_2026-10-22_run48.md, tests/unit/test_code_route_search.py
No secrets.

## Next priority remaining
5. Model provider defaults — Ollama preferred when healthy (currently refused; TinyLM educational fallback is correct).
6. Serve/deps — document/CI install for fastapi/uvicorn (doctor already marks optional).
Keep smoke ≥ 2101/2101 on any future change.
