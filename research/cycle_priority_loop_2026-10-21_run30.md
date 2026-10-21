# ORBIT Improvement Run — 2026-10-21 run30

## Baseline
- doctor: READY (API deps WARNING optional; Ollama offline OPTIONAL)
- smoke accuracy: 2090/2090 = 100% (2026-10-21_061711_eval.json)
- HEAD: 22673ff (main == origin/main)

## Failing probes
- "how do I reverse a string in python" → main_chat_agent generic hedge (not code)
- "how to reverse a string in python" / "how can I write a function…" same miss
- Priority 1/2/3 probes (write function, search fusion, identity) already pass

## Chosen priority
1. Coding path — natural "how do I / how to / how can I … in python" asks were excluded by the early how-do/how-does return False in `_wants_code_written`, so they never reached code_synth even when a template matched.

## Changes
- agents.py: before the how-do exclusion, treat "how do I|how to|how can I" + (in python|function|implement|write|code|reverse|sort|binary search|…) as a code ask. Numeric science ("how do I calculate the factorial of 5") still returns False and stays on calculator.
- evals/datasets/smoke.jsonl: +5 coding rows (code_howto_1..5).

## Tests
- doctor READY
- live probes: how-to coding → real def + Verified; factorial-of-5 → calculator 120; lab/search/identity/prose unchanged
- full eval: 2095/2095 = 100% (coding 2026/2026)

## Benchmark before → after
- smoke: 2090/2090 → 2095/2095 (held 100%; +5 how-to coding rows)
- how-to reverse/sort/binary/add: hedge → real code
- coding category: 2021 → 2026

## GitHub push
YES — agents.py + smoke.jsonl + this note

## Next priority remaining
4. GitHub parity (this push).
5. Model provider defaults — Ollama still offline (OPTIONAL).
6. Serve/deps — fastapi/uvicorn still WARNING; document-only unless CI needs serve job.
