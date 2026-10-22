# ORBIT Improvement Run 53 — 2026-10-22

## Baseline
- doctor: READY (API deps WARNING optional, Ollama OPTIONAL connection refused)
- smoke/eval accuracy: 2103 rows in smoke.jsonl; latest.json prior full pass 2101/2101 = 1.0 (coding 2030, search 13, rag 10, permission 11, lab 7+2)
- probes (all green before change):
  - coding: "write a python function that adds two numbers" → coding_agent + Verified
  - search: "search for recent news about fusion energy" → research_agent, pure offline
  - identity: "what is your name" → main_chat_agent, ORBIT
  - lab: "how does a neural network work" → lab_agent
- Gap: "how does binary search work" / "explain merge sort" hit research_agent offline and returned only the pure "No live web" dead-end even though code_synth has verified templates.

## Chosen priority
Priority 2 (research/search path) offline quality: keep routing to ResearchAgent, enrich offline algorithm explainers with local reference implementations. Do not invent web results; news/lookup stay pure offline.

## Research
- Existing design intentionally routes conceptual "how does X work" away from CodeAgent (agents.py + thinking.py question_form checks).
- code_synth already matches "how does binary search work" → binary_search template.
- Smallest change: ResearchAgent offline path tries _synthesize_python for conceptual non-news asks.

## Changes
- `agents.py` ResearchAgent.run: after failed live search, if conceptual and not news/papers, try code_synth; on hit return offline message + reference implementation + Verified; raw.edu_template=True.
- `tests/unit/test_code_route_search.py`: test_offline_algorithm_explainer_returns_local_template (algorithm explainer gets def; news does not).

## Tests
- pytest tests/unit/test_code_route_search.py: 10 passed
- Probes:
  - how does binary search work → research_agent + def binary_search + Verified
  - explain merge sort → research_agent + def merge_sort
  - search for recent news about fusion energy → pure offline (no def)
  - look up papers on attention → pure offline
  - write a python function… → coding_agent unchanged
  - what is your name → ORBIT unchanged
  - how does a neural network work → lab_agent unchanged

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| algorithm explainer offline | pure "No live web" | offline + local Verified template |
| news/search offline | pure offline | pure offline (unchanged) |
| coding / identity / lab | green | green |
| unit test_code_route_search | 9 | 10 passed |

## GitHub push
Pending focused commit of agents.py + test if credentials allow.

## Next priority remaining
Priorities 1–6 still satisfied. Optional: more smoke rows for offline edu explainers; serve extras when API deps required; keep smoke ≥ 2103.
