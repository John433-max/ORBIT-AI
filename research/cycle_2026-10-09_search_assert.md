# ORBIT Improvement Run — search/RAG eval assertions

Date: 2026-10-09

## Problem
Priority 2/3: smoke `search_1`, `search_2`, `search_4`, and `rag_empty_1` had empty `expect_contains`, so a generic toy-scale hedge scored as a pass.

## Research
SOURCE: ORBIT ResearchAgent `_offline_search_reply` (agents.py)
TECHNIQUE: accept either a live topic hit or the honest offline sentence; reject the educational hedge.
TRADE-OFFS: `expect_any` is OR, so a wrong-topic page that still mentions the keyword can pass. That is the existing live-search contract, not a new retrieval metric.

## Implementation
- `evals/runner.py` `score_row` honors `expect_any` (at least one needle).
- smoke rows now require topic or "don't have live web" / "no live web", and forbid `toy-scale`.
- `rag_empty_1` requires `couldn't find document #99`.
- `tests/unit/test_eval_score.py` covers AND, OR, and forbidden hedge.

## Tests
- scorer unit checks passed
- targeted ask: instruction_1, code_1, search_1, search_2, search_4, rag_empty_1, perm_1 all ok (7/7)
- dataset length unchanged: 1729

## Benchmark
| Metric | Before | After |
|---|---|---|
| doctor | READY (API warning, Ollama refused) | unchanged |
| full smoke file | 1729/1729 (latest.json 2026-10-09T06:14:02Z, empty search expects) | 1729 rows; tightened 4 rows not in that report |
| targeted probes | coding verified; fusion live; identity ORBIT | 7/7 including new assertions |
| search_1 empty expect | always ok | fails if neither fusion nor honest offline |

## Next
- GitHub parity for `evals/runner.py`, `evals/datasets/smoke.jsonl`, `tests/unit/test_eval_score.py`
- Priority 5 already prefers healthy Ollama then TinyLM
- Priority 6 serve extras already documented; fastapi still optional
