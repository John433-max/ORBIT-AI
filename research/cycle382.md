# Cycle 382

## Problem
GitHub Tests run 37089068657 on 4735ec1 failed both 3.11 and 3.12.
Local repro of `tests/unit` on that commit: 2 failed, 196 passed, 2 skipped.

- `test_p97_origin_common_missing_special_day_average` expected `def minimum_average` for LeetCode 3194, but pack p67 loads first and returns `def find_minimum_average`. Smoke has both needles (`code_647` and `code_825`).
- `test_p103_circular_similar_ends_fish_lunch_parens_teemo` expected `def shortest_to_char` for "shortest distance to a character leetcode 821". p10 matcher required `char` as a whole word or "distance to character" without "a", so the prompt fell through to NotImplemented.

## Implementation
- p10 matcher accepts "character" and `leetcode 821`.
- p67 source aliases `minimum_average` to `find_minimum_average`.
- p97 source aliases `find_minimum_average` to `minimum_average` so either load order satisfies both needles.

## Tests
- `test_p97_origin_common_missing_special_day_average` PASS
- `test_p103_circular_similar_ends_fish_lunch_parens_teemo` PASS
- synthesize_and_verify on the 3194 prompt and both shortest-to-char prompts: verified True

## Result
Keep. Push to main.
