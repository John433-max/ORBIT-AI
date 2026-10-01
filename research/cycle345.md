# Cycle 345 — GitHub pack parity + doctor API severity

## Problem
Doctor reported NOT READY because a missing FastAPI/uvicorn line was concatenated into the blocking Dependencies row whenever any other install check failed. SETUP.md already says API deps are non-blocking. GitHub main listed packs through p79 but was missing the pack files for p2, p3, p28–p32, p44, p47, p49, p53–p57, p59, p62, p64–p66, p68, p73–p78.

## Change
- `run_orbit.py` doctor: API deps always a separate WARNING row.
- Pushed missing `code_synth_p*.py` packs and kept loader p79 from Cycle 344.

## Measurement
- doctor before: NOT READY (1 blocking: PyYAML+fastapi bundled as ERROR)
- doctor after PyYAML present + severity split: READY (API deps WARNING, TinyLM WARNING, Ollama OPTIONAL)
- probes unchanged: add() verified; search honest no-live-web; identity ORBIT
- clone import after packs: 691 templates; add template verified

## GitHub
2629667 Parity: missing code_synth packs p2-p3/p28-p78 and split doctor API deps.
