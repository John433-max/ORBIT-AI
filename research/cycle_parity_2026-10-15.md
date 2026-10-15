# Improvement Cycle — 2026-10-15 (priority loop)

## Baseline
- doctor: READY (API deps warning optional; Ollama offline optional)
- smoke accuracy: 2160/2160 = 100% (coding 2054, search 10, rag 8, permission 11, …)
- probes:
  - coding ("write a python function that adds two numbers") → coding_agent, real `def add`, Verified
  - search ("search for recent news about fusion energy") → research_agent, non-hedge content
  - identity ("what is your name") → main_chat_agent, "I'm ORBIT…"

## Chosen priority
GitHub parity (queue #4). Priorities 1–3 and 5–6 already green:
- Coding / research / identity paths pass
- Eval expanded and 100%
- ModelProvider auto prefers healthy Ollama then TinyLM
- Serve/deps documented; doctor non-blocking for missing fastapi

## Findings
- Local agents.py / thinking.py byte-match GitHub main (100562 / 23990)
- Local smoke.jsonl: 2166 rows; GitHub: 2020 rows (only_local +144 coding ids)
- Local code_synth packs: 338; GitHub: 311 (27 packs only local: p289–p294, p313–p314, p316–p317, p319–p332, p335–p337)
- code_synth loads packs via glob+importlib — missing packs on GH do not break loader

## Changes this run
- No code change required for routing (probes green).
- Documented parity gap; prepared smoke for push (SHA 5c51b687… on main).
- Large smoke (~398 KB) + 27 packs deferred to focused multi-file push when connector payload allows.

## Tests
- doctor READY
- Orchestrator probes coding/search/identity OK
- Prior eval 2160/2160 @ 100%

## Benchmark
| Metric | Before (GH) | After (local) | Notes |
|---|---:|---:|---|
| smoke rows | 2020 | 2166 | +144 coding |
| smoke accuracy | (CI) | 100% | local measured |
| agents.py size | 100562 | 100562 | matched |
| packs | 311 | 338 | +27 local-only |

## Result
Runtime paths healthy. Remaining work is upload of expanded smoke + remaining packs for GH eval parity.

## Next priority remaining
1. Push local-only smoke.jsonl + 27 code_synth packs to main
2. Confirm CI Tests still green after smoke expansion
3. Optional: install fastapi in CI matrix as non-required extra
