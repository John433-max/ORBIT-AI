# Improvement Cycle 511

## Problem
Baseline eval on 1662 smoke rows was 1661/1662. code_1431 expects `list_span` for "statistical range of a list", but the Cycle 510 matcher only accepted span / max-minus-min. Six other natural asks still missed the router: first word, count negatives in a list, double odd numbers, hyphen between characters, product of evens, last character of each word.

## Research
SOURCE: Chen et al., HumanEval (arXiv:2107.03374), 2021
DATE: 2026-10-08
TECHNIQUE: example-checked deterministic templates plus a phrase alias on an existing template
WHAT IT IMPROVES: coding-agent fallthrough and a measured smoke miss
REQUIREMENTS: no new dependencies; new pack loads before older broad matchers
TRADE-OFFS: "statistical range" must not steal interquartile, summary, missing, BST, or CIDR range templates
RELEVANCE TO ORBIT: smoke coding path is the measured success metric
EXPECTED BENEFIT: restore code_1431 and add 6 verified rows

Rejected widening p63 `count_negatives` (matrix signature). New name `count_negative_values` so the LeetCode 1351 template stays loaded.

## Implementation
- code_synth_p227.py: six templates
- code_synth.py loads p227 first
- code_synth_p226.py list_span accepts "statistical range" and excludes interquartile/bst/query/cidr
- smoke code_1624–code_1629
- tests/unit/test_code_synth.py::test_p227_first_word_negatives_odds_hyphen_not_stolen

## Tests
- p226 and p227 unit functions passed
- steal guards: last_word, is_even, double_elements, multiply, count_negatives, interquartile_range, summary_ranges, missing_ranges
- OrbitAI new+fixed rows 7/7 in 14.19s

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke lines | 1662 | 1668 | +6 |
| code_1431 | miss (fallback) | Verified list_span | restored |
| new coding rows | fallback | 6/6 Verified | +6 |
| targeted OrbitAI | — | 7/7 in 14.19s | — |

Full eval after matcher tighten: 1668/1668 (100%) in 203.53s. Intermediate 1666/1668 was the over-broad negative matcher (code_650, code_1360); tightened before keep.

## Result
Kept. Statistical-range ask matches list_span; six previously unmatched asks return verified functions.

## Next
GitHub pack parity for p225–p227, or more unmatched natural asks (keep only letters, perfect cube, trailing zeros).
