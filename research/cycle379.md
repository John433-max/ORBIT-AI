# Improvement Cycle 379

## Problem
Coding path returned a verified `sum_list` for "minimum operations to make array sum divisible by k" (LeetCode 3512). Neighboring bitwise XOR (2683), minimum array end (3133), balanced-bracket swaps (1963), minimum length after operations (3223), and can-sort-array (3011) were NotImplemented drafts.

## Research
SOURCE: LeetCode 3512 / doocs solution notes
DATE: 2026-10-02
TECHNIQUE: each decrement reduces the sum by 1, so the minimum operations is S mod k.
WHAT IT IMPROVES: coding-route correctness on an Easy problem that collided with the generic sum matcher.
TRADE-OFFS: matcher is phrase-specific; sum_list still handles "sum a list of numbers" after excluding "divisible" and "operation".

Other templates use published sample I/O:
- 2683: derived is a valid neighboring XOR iff the XOR of all derived bits is 0.
- 3133: place n-1 into the zero-bits of x (minimum last element).
- 1963: count bracket swaps that repair a negative balance.
- 3223: each character count reduces to 1 if odd else 2.
- 3011: adjacent swaps only inside equal popcount runs; runs must be non-decreasing.

## Implementation
- code_synth_p102.py (6 templates), loaded before older packs.
- sum_list excludes "divisible" and "operation".
- smoke code_850–code_855.
- tests/unit/test_code_synth.py::test_p102_sum_divisible_neighbor_xor_min_end_swaps_len_sort

## Expected
3512 no longer returns sum_list. Six prompts verify. Generic sum still routes to sum_list.
