# Cycle GH parity p236-p239

Date: 2026-10-08

## Problem
GitHub main code_synth.py loader stopped at code_synth_p234. Local packs p236-p239 were not on main, so CI could not match zip-three, take-n, drop-n, and three-divisors asks that local smoke already covers.

## Change
Pushed code_synth_p236.py through code_synth_p239.py. p235.templates() now prepends those packs (p234 already imports p235), so the existing main loader picks them up without replacing code_synth.py.

## Local checks
- doctor: READY (PyYAML warning, API deps warning, Ollama optional refused)
- smoke: 1726/1726 before this chain edit
- match probes after chain: zip_three, permute_string, drop_n, is_three, add
- p235 chained templates: 22, verify fails 0
