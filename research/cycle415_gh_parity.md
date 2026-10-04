# Cycle 415 — GitHub parity for p137

## Problem
Local smoke was 1100/1100 after Cycle 414 (maze / union-find templates). GitHub main was still at cycle 413 (smoke 1094, no `code_synth_p137`).

## Change
Push focused files only: `code_synth_p137.py`, loader registration in `code_synth.py`, smoke rows `code_1054`–`code_1059`, `test_p137_maze_union`, and `research/cycle414.md`.

## Validation
Local `test_p137_maze_union` passed. Smoke accuracy 1100/1100 before push. Probes: add-two-numbers returns verified code; fusion search returns honest no-live-web; identity remains ORBIT.
