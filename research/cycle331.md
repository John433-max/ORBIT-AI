# Improvement Cycle 331

## Problem
Coding/search/identity probes already pass. Smoke snapshot 689/689.
Highest remaining: GitHub pack parity (remote loader stopped at p63; local through p68)
plus Easy coverage expansion.

## Research
Keep packs split. Do not replace slim GitHub `agents.py`.
Tighten `divide` so LeetCode 2520 ("digits that divide") is not stolen
because `_TWO` matches the `2` in `2520`.

## Implementation
- `code_synth_p69.py`: generate_key (3270), find_missing_and_repeated_values (2965),
  find_the_array_conc_val (2562), sum_of_encrypted_int (3079), max_frequency_elements (3005).
  count_digits kept on p51 with a broader matcher (the number / leetcode 2520).
- `code_synth_p1.py` divide excludes digits-that-divide / 2520.
- Loader lists `code_synth_p69`.
- smoke `code_656`–`code_661`.
- unit `test_p69_key_missing_digits_concat_encrypt_freq`.

## Result
Local probes unchanged (code + search + ORBIT identity).
Templates 675 (p69 count_digits deduped vs p51).
