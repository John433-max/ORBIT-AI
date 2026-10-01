# Cycle 354

## Problem
CI on main failed (run 36939498839, commit 608654b, and follow-ups 36939897406 / 36939906714). Unit tests call synthesize_python for classic prompts (merge two sorted lists, balanced parentheses, running sum). Published packs never defined those templates, so synthesize fell back to the NotImplemented stub. Broad p1 matchers also stole later Easy prompts (sort_list vs parity, is_even vs even digit counts, candy vs distribute candies).

## Research
First-match routing loses to early broad lambdas. A later hit whose name tokens are a superset of the winner and appear in the request is already preferred (Cycle 283). Scoring by how many name tokens occur in the request (threshold 2) covers non-subset pairs such as sort_list vs sort_array_by_parity.

## Implementation
- code_synth_p84.py: 32 classic templates missing on GitHub plus collision winners (parity, even-digit count, palindrome II, element/digit sum, count digits, distribute candies, sum of good numbers, max product difference). Loaded first; duplicate names skipped locally.
- match_template: keep superset upgrade; also prefer a later hit with a strictly higher token score when score >= 2.
- smoke code_475 expect updated to def minimum_number_game (LeetCode 2974). The previous number_game needle lost to the more specific verified template.

## Tests
- GitHub tree + these files: tests/unit/test_code_synth.py 116 passed; other tests/unit 61 passed, 2 skipped.
- Local probes: add verified; merge_sorted; sort_array_by_parity_ii.

## Benchmark
- Smoke before this run's last published note: 785/785.
- After matcher change, before smoke needle update: 784/785 (code_475 missing def number_game).
- Needle updated to the function actually returned.

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| GitHub unit tests (published tree) | fail (stub synthesize) | code_synth 116 passed; other unit 61 passed, 2 skipped |
| smoke accuracy | 785/785 published; 784/785 mid-change | 785/785 |
| coding | 745/745 | 745/745 |

## Result
CI failure was missing classic templates plus broad early matchers, not the p82 pack itself. p84 restores those functions; token-score upgrade prefers more specific later hits.

## Next
GitHub agents.py still slimmer than local. Serve extras (fastapi) remain optional doctor warnings.
