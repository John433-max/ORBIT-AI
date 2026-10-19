# CI matcher fixes 2026-10-19 (run 39195723974+)

## Problem
GitHub CI `test_code_synth` failed on main (ce18004 and follow-ups through 41eda0f).
Reproduced on a fresh clone of origin/main: 5 failures, 264 passed (maxfail=5).

## Failures
1. `reverses vowels in a string` → reverse_string (stole reverse_vowels)
2. `maximum average of a subarray of length k` → no match (find_max_average)
3. `splits pairs into two lists` → no match (split_pair_lists)
4. `rotate an array right by k` → no match (rotate_array)
5. (related) reverse_string broad matcher

## Fixes (minimal matcher widen + exclusion)
- code_synth_p0.py: reverse_string excludes "vowel"
- code_synth_p4.py: reverse_vowels accepts reverses/reversed/reversing + vowels
- code_synth_p26.py: find_max_average accepts "maximum average of a subarray of length"
- code_synth_p25.py: rotate_array accepts "rotate an array right by"
- code_synth_p237.py: split_pair_lists accepts "splits pairs into two lists"
- code_synth_p355.py: longest_increasing_subsequence excludes "patience" (lis_nlogn)

## Baseline
- doctor: READY
- smoke eval: 99.90% (2081/2083)
- probes: coding → coding_agent; search → research_agent; identity → ORBIT

## Next
Push these five pack files + p355 to main; re-run CI.

## Follow-up 2026-10-19T04:23Z
- Pushed p25 rotate_array, p26 find_max_average, p355 LIS patience exclusion
- code_synth match_template: prefer strong first match (score>=2) unless later hit is +2 tokens
  → bitonic_sort beats is_power_of_two on "bitonic sort power of two"
- Restored code_synth.py after accidental PLACEHOLDER
- Commits: 1c60694e, 745ad34c, 5078db3f, ff14cd71
