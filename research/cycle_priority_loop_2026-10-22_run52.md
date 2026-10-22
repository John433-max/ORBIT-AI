# ORBIT Improvement Run 52 — 2026-10-22

## Baseline
- doctor: READY (API deps WARNING optional, Ollama OPTIONAL connection refused, PyYAML optional)
- smoke/eval accuracy: 2101/2101 = 1.0 (coding 2030, search 13, rag 10, permission 11, lab 7)
- probes (all green):
  - coding: "write a python function that adds two numbers" → coding_agent + code_synth Verified
  - search: "search for recent news about fusion energy" → research_agent, honest "No live web…"
  - identity: "what is your name" → main_chat_agent, ORBIT
  - lab: "how does a neural network work" → lab_agent three_neurons; transformer → next_token

## Chosen priority
Priorities 1–6 green. Highest remaining value from run 51: expand smoke eval with neural-network / transformer lab routing rows so the lab path stays covered. Also push the unpushed lab routing commit.

## Changes
- `evals/datasets/smoke.jsonl`: +2 rows (`lab_nn`, `lab_transformer`)
- `tests/unit/test_thinking.py`: `test_neural_network_and_transformer_route_to_lab`
- No routing code change (already in 91e6b8d)

## Tests
- doctor READY
- new smoke rows score ok against OrbitAI.ask (XOR/neuron/three_neurons; next-token/next_token)
- unit test classify → lab for NN and transformer phrases
- core probes unchanged green

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| smoke rows | 2101 | 2103 |
| smoke accuracy (prior full) | 2101/2101 | new rows scored ok (full re-eval deferred; prior 1.0 + 2/2) |
| lab NN/transformer | routed, no eval row | eval + unit coverage |
| coding/search/identity | green | green |

## GitHub push
YES if credentials allow: lab routing commit 91e6b8d + this eval/test expansion.

## Next priority remaining
All six priority items satisfied. Keep smoke ≥ 2103/2103. Optional: more lab phrase coverage or serve extras if API deps become required.
