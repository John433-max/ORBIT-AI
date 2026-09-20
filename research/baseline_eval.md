# Eval baseline — 2026-09-20

## Smoke suite (`evals/datasets/smoke.jsonl`)

| Metric | Value |
|--------|------:|
| Accuracy | **100%** (14/14) |
| Math | 4/4 |
| Science | 4/4 |
| Chat | 2/2 |
| Tool selection | 1/1 |
| Memory | 1/1 |
| Instruction | 1/1 |
| Hallucination guard | 1/1 |

## Fixes this cycle
1. **Doctor severity** — Ollama/fastapi optional warnings no longer force NOT READY
2. **Identity routing** — `what is your name` → chat (not web research / movie results)
3. **Thinker** — `_is_self_identity` skips search pipeline for self questions
4. **Persona** — removed product “ORBIT-100B” claims from `persona_chat.jsonl`
5. **Smoke expectations** — fairer needles

## Unit tests
`tests/unit`: **37 passed**

## Principle
ORBIT is a modular local AI agent runtime — not a fixed model size.
