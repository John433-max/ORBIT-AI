# Cycle 439 — GitHub parity for p157/p158

## Problem
Local smoke already covered cycle 438 (even-or / missing-integer steal fix) and cycle 439 dict helpers, but GitHub `code_synth.py` loaded only through `code_synth_p156`. Those packs were absent, so main still routed 3688 to `is_even` and dict merge/invert/zip asks to the draft stub.

## Implementation
Pushed to `John433-max/ORBIT-AI` main (no secrets):

- `code_synth_p157.py` (commit file sha `3bc4d7a0`)
- `code_synth_p158.py` (`523a2fbd`)
- `code_synth.py` loader lists p158 then p157 before p156 (`e89ea82c`)

Remote loader was the previous main file plus those two import names. Missing packs still skip, so CI collection is unchanged if a pack is absent.

## Tests
- Direct `synthesize_and_verify`: 3688 → `even_numbers_bitwise_or`; 2996 → `missing_integer`; 2839/2873/2900/2946/2178 verified; `is_even` and `running_sum` still match generic phrasing.
- `test_p157_even_or_missing_ops_triplet_groups_shifts_split` and `test_p158_merge_invert_zip_sorted_keys` pass when invoked directly (pytest module not installed in this environment).

## Benchmark
Full smoke eval at 2026-10-05T02:09:31Z was 1219/1219 before these rows were the parity target. New local rows `code_1183`–`code_1193` were not re-run as a full eval this cycle; route checks above passed.

## Next
Serve extras (fastapi/uvicorn) remain optional doctor warnings. Ollama is down, so TinyLM fallback is correct.
