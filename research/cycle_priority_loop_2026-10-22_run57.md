# ORBIT Improvement Run 57 — 2026-10-22

## Baseline
- doctor: READY (API deps WARNING, Ollama OPTIONAL connection refused)
- smoke/eval accuracy: 2103/2103 = 1.0 (latest.json 2026-10-22T16:15:22Z)
  - coding 2030/2030, search 13/13, rag 10/10, permission 11/11, lab 9/9
- probes before fix:
  - coding / search / identity: green
  - "explain transformers" / "how does attention work in transformers" / "what is self-attention" → offline research hedge (wrong)

## Chosen priority
Lab routing gap for transformer/attention conceptual explainers (related to priority 2 research path cleanliness + educational lab path).

## Research
Existing lab patterns only matched "how does a transformer" / "what is a transformer". Plural "transformers", bare "explain transformers", and "attention" / "self-attention" fell through to ResearchAgent offline message.

## Changes
- `lab_agent.py`: expand `looks_like_lab` for transformers?, (self-)?attention, explain …; map plural transformer + attention → `next_token` demo
- `thinking.py`: mirror `_is_lab` pattern
- `agents.py`: fallback `_looks_like_lab` includes attention
- `tests/unit/test_thinking.py`: cover explain transformers / attention / self-attention

## Tests
- test_thinking.py 13 passed
- test_code_route_search + lab filters: 27 passed, 1 skipped
- probes after: coding verified, search honest offline, identity ORBIT, transformer/attention → next_token lab caption

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| smoke accuracy | 2103/2103 | unchanged (routing only) |
| explain transformers | research offline | lab next_token |
| how does attention work in transformers | research offline | lab next_token |
| what is self-attention | research offline | lab next_token |
| priority probes (code/search/identity) | green | green |

## GitHub push
Pending focused commit of lab_agent.py, thinking.py, agents.py, test_thinking.py

## Next priority remaining
GitHub parity push of this fix; optional more Easy code_synth templates or TinyLM source polish.
