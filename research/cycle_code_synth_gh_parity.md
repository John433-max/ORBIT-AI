# Cycle: GitHub code_synth loader parity

Date: 2026-10-09

## Problem
Local `code_synth.py` (26224 B, blob `af0d0bf73b0aeb5be1f17c53ebb2da79b4c4c1ea`) keeps Cycle 207–463 matcher overrides (`_widen_loaded`: swap_case, chunk_list, rotate_string, last_n, pairwise, drop_last, …).

GitHub main `code_synth.py` (5062 B, blob `b67e623bc97822bf0af0b3eb19c2ca6558966685`, commit `ea588e3c`) is a thin glob loader written after a PLACEHOLDER break. It discovers packs but does not apply `_widen_loaded`, so phrases that smoke and unit tests pin to those names can miss on a fresh clone.

`agents.py`, `thinking.py`, and `run_orbit.py` blob-hashes already match main.

## Change
Push local `code_synth.py` (hardcoded pack order + widen overrides). Pack order is unchanged because smoke depends on first-hit order. `code_synth_p1b` / `p1c` names are already covered by later packs (0 new names).

## Checks
- doctor READY (PyYAML warning, fastapi warning, Ollama optional refused)
- eval 1729/1729 (100%), 241.1 s
- probes: add-two-numbers verified; fusion search with sources; identity ORBIT
- matcher asserts: swap_case, chunk_list, rotate_string, last_n, pairwise, add
