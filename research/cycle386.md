# Cycle 386 — second-largest list coding path

## Problem
Natural-language "write a python function that returns the second largest number in a list" routed to the code agent but returned a NotImplemented draft stub. `second_largest_digit` (LeetCode 1796) did not cover list values.

## Implementation
- `code_synth_p107.py`: verified `second_largest` (distinct values, None if fewer than two). Matcher requires "second largest number/element/value/item" and excludes digit / 1796.
- Smoke `code_887` expects `def second_largest` and Verified.

## Tests
- `test_p107_partitions_pair_fruits_removal_index_second_largest` passed.
- Probe returns verified `second_largest`.
- Digit prompt still hits `second_largest_digit`.
- Smoke 921/921 → 927/927 (100%).

## GitHub
p107 was absent on main. Push p107 + smoke.
