# Cycle 350 — code_synth_p81 Easy coverage

## Problem
Several Easy coding prompts still missed every template and fell through to a stub. Pack coverage stopped at p80 / code_727.

## Research
SOURCE: LeetCode wiki (doocs) official examples
DATE: 2026-10-02
TECHNIQUE: verified template + phrase matcher
PROBLEM SOLVED: first-match miss on distinct Easy prompts
HOW IT WORKS: CodeAgent calls synthesize_and_verify; a matcher that requires a distinctive phrase returns a function checked against official examples.
REQUIREMENTS: existing Template / synthesize_and_verify
TRADE-OFFS: first-match routing; phrases must not be substrings of broader matchers
RELEVANCE: CodeAgent uses code_synth before the model
EXPECTED BENEFIT: +6 verified coding smoke rows

Sources:
- https://leetcode.doocs.org/en/lc/3442/ examples "aaaaabbc"→3, "abcabcab"→1
- https://leetcode.doocs.org/en/lc/3330/ "abbcccc"→5, "abcd"→1, "aaaa"→4
- https://leetcode.doocs.org/en/lc/3427/ [2,3,1]→11, [3,1,1,2]→13
- https://leetcode.doocs.org/en/lc/3370/ 5→7, 10→15, 3→3
- https://leetcode.doocs.org/en/lc/3178/ (3,5)→1, (5,6)→2, (4,2)→2
- https://leetcode.doocs.org/en/lc/1925/ n=5→2, n=10→4

## Implementation
- `code_synth_p81.py`: max_freq_odd_even_diff, possible_string_count, variable_length_subarray_sum, smallest_number_all_set_bits, child_with_ball, count_square_sum_triples
- Loader lists `code_synth_p81`
- smoke.jsonl code_728–code_733
- unit test `test_p81_freq_typed_varsum_setbits_ball_triples`

Rejected collisions this cycle: defang/transpose/pangram/concatenation already matched under other names.

## Tests
- synthesize_and_verify on the six prompts: all verified
- full template example exec: new names match; 18 pre-existing KeyError name mismatches unchanged
- coding smoke def-check: 733 rows, mismatches 0, 76.45s

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| unique templates | 734 | 740 | +6 |
| coding smoke rows checked | 727 | 733 | +6 |
| coding def mismatches | 0/727 | 0/733 | +6 covered, 0 miss |

## Result
Kept. New prompts verify against official examples. No matcher exclusion was required.

## Next
GitHub pack parity for p81, or another unmatched Easy phrase that does not collide with existing first-matchers.
