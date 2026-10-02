# Cycle 359: unmatched Easy coding templates (p85)

## Problem
Smoke coding coverage still fell through to the NotImplemented stub on several Easy prompts. First-match routing already covers sort-the-people (2418) and maximum-units (1710), so those were rejected as duplicates.

## Research
SOURCE: LeetCode problem statements 2125, 2486, 2299, 2259, 2109, 1833
DATE: 2026-10-02
TECHNIQUE: verified deterministic templates with phrase matchers
WHAT IT IMPROVES: coding-task success on previously unmatched asks
REQUIREMENTS: existing code_synth Template + verify_source
TRADE-OFFS: more pack surface; matchers must stay phrase-specific
RELEVANCE: CodeAgent still answers these without a model
EXPECTED BENEFIT: 6 additional verified smoke rows, no regression on adjacent templates

Rejected after probe: sort_people and maximum_units already resolve to sort_the_people and max_units_on_truck.

## Implementation
- code_synth_p85.py: number_of_beams, append_characters, strong_password_checker_ii, remove_digit, add_spaces, max_ice_cream
- code_synth.py loader lists p85
- tests/unit/test_code_synth.py
- evals/datasets/smoke.jsonl code_746–code_751

## Tests
- test_p85 function: pass (6/6 verified)
- test_p82 and test_p83 functions: pass
- OrbitAI.ask on the 6 new smoke rows: 6/6 expect_contains

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| unique templates | 752 | 758 | +6 |
| smoke rows | 785 | 791 | +6 |
| new coding rows verified | 0/6 unmatched | 6/6 | +6 |
| adjacent p82/p83 | pass | pass | 0 |

Before template count is loaded packs minus the new module (758−6).

## Result
Kept. Unmatched Easy prompts now return verified functions. Existing sort/units/remove-duplicates routes unchanged.

## Next
Another unmatched Easy pack (adjacent-duplicates 1047, string-great 1544, ice-cream already done) or GitHub pack parity for p85.
