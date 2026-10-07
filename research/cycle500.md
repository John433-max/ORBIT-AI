# Improvement Cycle 500

## Problem
Six natural-language coding asks still fell through to the draft stub: odd counts in a range, numbered-sentence sort, sum of unique values, equivalent string arrays, shuffle-string-by-indices, and arithmetic-progression check. Two existing templates also missed common phrasing: "rotates an array to the right by k" and "intersects two arrays".

## Research
HumanEval scores generated functions by executing hidden tests (Chen et al., 2021, https://arxiv.org/abs/2107.03374). ORBIT already verifies templates against tiny examples before reporting Verified.

LeetCode 1523 counts odds in an inclusive range with `(high+1)//2 - low//2`. 1859 sorts words by a trailing 1-based index. 1748 sums values with count 1. 1662 compares concatenated string arrays. 1528 places characters at given indices. 1502 checks a constant difference after sorting.

SOURCE: Chen et al., Evaluating Large Language Models Trained on Code, 2021. https://arxiv.org/abs/2107.03374
DATE: 2026-10-07
TECHNIQUE: example-checked phrase templates plus matcher widening
WHAT IT IMPROVES: coding-path coverage for unmatched write-a-function asks
REQUIREMENTS: exclusive lowercase phrases; no new dependencies
TRADE-OFFS: sort_sentence assumes a single trailing digit; count_odds is inclusive
RELEVANCE TO ORBIT: coding smoke is template-backed
EXPECTED BENEFIT: six new verified asks and two recovered existing templates
IMPLEMENTATION PLAN: pack p216 first in the loader; widen rotate_array and the live intersection matcher

## Finding
Pre-probe misses confirmed. Neighbors three_consecutive_odds, unique_occurrences, and string rotation (can_rotate_to) still win their phrases. The live intersection template is in code_synth_p84.py (packs load before p1 and dedupe by name). `\barray\b` does not match "arrays", so the intersects alternative must allow a plural.

## Implementation
- code_synth_p216.py: count_odds, sort_sentence, sum_of_unique, array_strings_are_equal, restore_string, can_make_arithmetic_progression
- loader lists p216 first
- code_synth_p25.py rotate_array accepts right-rotate phrasing
- code_synth_p84.py intersection accepts "intersects … arrays" and "array intersection"
- smoke code_1552–code_1557
- unit test test_p216_odds_sentence_unique_equal_shuffle_ap

## Tests
- test_p216 unit function passed
- subset eval 6/6 coding

## Benchmark
Subset eval of the six new rows: 6/6. Full smoke eval recorded separately after this note.

## Tests
- test_p216_odds_sentence_unique_equal_shuffle_ap passed, including interval and restore-string aliases
- First full eval 1593/1595: p216 names shadowed older matchers (count_odds interval, restore_string). Widened those matchers.
- Second full eval 1595/1595 at 100%.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke accuracy | 1586/1586 (100%) | 1595/1595 (100%) | +9 rows, accuracy held |
| coding rows | 1541/1541 | 1550/1550 | +9 verified |
| doctor | READY | READY | unchanged |

## Result
Kept. Coding path covers the six missed asks and the two phrasing gaps without dropping prior aliases.

## Next Research Target
GitHub parity for p216 plus loader/matcher edits, or remaining unmatched write-a-function probes (k-distance ones, binary substrings, restore IP).
