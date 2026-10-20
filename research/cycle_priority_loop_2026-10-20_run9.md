# ORBIT Priority Loop — 2026-10-20 run9

## Baseline
- doctor: READY (2 non-blocking: fastapi/uvicorn missing, Ollama connection refused)
- smoke accuracy: 100.00%  2083/2083
  - coding: 2021/2021
  - search: 9/9
  - rag: 6/6
  - permission: 10/10
  - lab: 7/7
  - math/science/chat/memory/instruction/hallucination/tool_selection: all 100%
- probes:
  - coding → coding_agent + verified `def add(a, b)` + binary_search
  - search → honest "No live web available..."
  - identity → "I'm ORBIT. Named after the project..."
  - permission → deny destructive fs
  - rag-empty → "No documents loaded..."

## Chosen priority
None failing. Priority queue items 1–3 satisfied; 5–6 correct by design.
Item 4 (GitHub parity): local agents.py ~22.5KB CI-surface works; full historical 71KB not required while CI green.

## Changes
No code changes. Verification-only run after background task completion.

## Tests
- doctor READY
- eval 2083/2083 (latest.json)
- five probes pass (code/search/identity/permission/rag-empty)

## Benchmark before → after
Unchanged (ceiling for current smoke set).

## GitHub push
YES — research docs run5–run9 (docs only, no secrets)

## Next priority remaining
1. Optional eval expansion (multi-turn coding, more RAG-empty variants) if accuracy ever slips.
2. GitHub pack parity for remaining code_synth_p* if CI needs full tree (currently slim+packs sufficient).
3. Serve extras (fastapi) only on user request.
4. Ollama preferred when healthy; TinyLM educational fallback correct.
