# Improvement Cycle 360

## Problem
Several Easy string prompts still fell through to the NotImplemented stub: adjacent duplicates (1047), make-the-string-great (1544), rearrange spaces (1592), equal-char gap (1624), second-largest digit (1796), prefix-of-array (1961). Nearby asks (defang IP, pangram, replace digits) already resolved and were rejected as duplicates.

## Research
SOURCE: LeetCode problem statements 1047, 1544, 1592, 1624, 1796, 1961 (algorithm descriptions only)
DATE: 2026-10-02
TECHNIQUE: verified deterministic templates with phrase matchers
WHAT IT IMPROVES: coding-task success on previously unmatched asks
REQUIREMENTS: existing code_synth Template + verify_source
TRADE-OFFS: more pack surface; matchers must stay phrase-specific so "remove duplicates" and "prefix" do not steal sorted-array or prefix-count routes
RELEVANCE: CodeAgent still answers these without a model
EXPECTED BENEFIT: 6 additional verified smoke rows, no regression on p85

## Finding
Stack-pop for adjacent equals (1047) and case-inverse pairs (1544), even space redistribution (1592), first-index gap (1624), second distinct digit (1796), and concatenation prefix (1961) fit the existing Template contract. First 1592 example expected string omitted the leftover space (10 spaces / 3 gaps); corrected to the algorithm result before keeping the change.

## Implementation
- code_synth_p86.py: remove_all_adjacent_duplicates, make_good, reorder_spaces, max_length_between_equal_characters, second_highest, is_prefix_string
- code_synth.py loader lists p86
- tests/unit/test_code_synth.py::test_p86_adjacent_great_spaces_gap_digit_prefix
- evals/datasets/smoke.jsonl code_754–code_759

## Files Changed
- code_synth_p86.py (new)
- code_synth.py
- tests/unit/test_code_synth.py
- evals/datasets/smoke.jsonl
- research/cycle360.md

## Tests
- pytest test_p86: pass (6/6 verified)
- pytest test_p85: pass (no adjacent regression)

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| unique templates | 758 | 764 | +6 |
| smoke rows | 794 | 800 | +6 |
| coding smoke rows | 753 | 759 | +6 |
| new coding rows verified | 0/6 unmatched | 6/6 | +6 |
| adjacent p85 | pass | pass | 0 |

Before counts are loaded templates and smoke lines minus the six added in this cycle.

## Result
Kept. Unmatched Easy string prompts now return verified functions.

## Problems
First 1592 expected string dropped the remainder space; fixed before the test was recorded as passing.

## Next Research Target
Another unmatched Easy pack, or GitHub pack parity for p86.
