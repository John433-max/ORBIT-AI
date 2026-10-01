# Improvement Cycle 332 — GitHub pack parity (missing Easy packs)

Date: 2026-09-30

## Problem
Local coding path is healthy (701/701 smoke, probes pass) but GitHub
`code_synth.py` lists packs p1–p69 while several packs exist only locally.
CI therefore loads a thinner template set than the sandbox.

## Chosen work
Push missing mid-size packs that the GH loader already imports
(skipped if absent). Do not replace GH `agents.py` (14.8KB CI surface)
with the 85KB local orchestrator.

## Local baseline
- doctor: READY (fastapi/uvicorn warning; Ollama optional down)
- smoke: 701/701 (coding 661)
- probes: add-two-numbers → coding_agent verified; fusion search → research_agent with sources; name → ORBIT

## Missing on GitHub (local present)
p2, p3 (large), p28–p32, p44, p47, p49, p53–p57, p59, p62, p64–p66, p68

## Tests
- tests/unit/test_code_synth.py: 103 passed
- tests/unit/test_thinking.py: 5 passed
- templates loaded locally: 675
