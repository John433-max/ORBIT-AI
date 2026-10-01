# Cycle 354 — GitHub code_synth pack parity (CI Tests fix)

## Problem
Tests workflow on Cycle 352 (`608654b`, run 36939498743) failed unit tests.
Shallow main (`b0af692`) reproduced 26 failures in `tests/unit/test_code_synth.py` (90 passed).

## Cause
Published packs diverged from the local source of truth. `code_synth_p1.py` on GitHub was 12KB and lacked early templates (`merge_sorted`, balanced parentheses, running sum, Kadane, stock profit). The broad `maximum` matcher stole "maximum product difference". Smaller matcher drift in p3/p36/p39/p51/p58/p60/p61/p67 failed later pack tests.

## Change
Copied local packs that differed by size onto main:
`code_synth_p1.py`, `code_synth_p3.py`, `code_synth_p36.py`, `code_synth_p39.py`, `code_synth_p51.py`, `code_synth_p58.py`, `code_synth_p60.py`, `code_synth_p61.py`, `code_synth_p67.py`.

## Tests
GitHub tree + these packs: `tests/unit` 177 passed, 2 skipped.
`tests/unit/test_code_synth.py` 116 passed (was 26 failed).

## Rejected
Rewriting match ranking in `code_synth.py` — pack order is smoke-sensitive (Cycle 283). Restoring missing templates is the smaller compatible fix.
