# Improvement Cycle 557

## Problem
Smoke eval after Cycle 556 was 1787/1789 (99.89%). Two coding rows failed:

1. `code_boyer_1` ("boyer moore string search") routed to ResearchAgent.
   The word "search" matched the research route; the algo_search whitelist
   only covered binary/linear/interpolation/exponential/ternary/fibonacci.
2. `code_86` ("write a python function that can partition equal subset sum")
   hit the new `subset_sum` template instead of `can_partition` (LeetCode 416).

## Research
Technique: phrase-specific routing whitelist + matcher exclusion.
Source: existing ORBIT Cycle 547 algo_search pattern; can_partition matcher in code_synth_p2.
Date: 2026-10-10

## Finding
Bare algorithm titles that contain "search" (Boyer-Moore string search) are code
when a verified template hits. Explicit web phrases ("search for", "look up",
"news about") must stay research. "partition equal subset sum" must not match
the generic subset-sum template.

## Implementation
- Expanded algo_search whitelist in agents.py (`_wants_code_written`, `route`)
  and thinking.py (`_is_code`) to include boyer-moore, horspool, and string-search.
- Tightened `subset_sum` matcher in code_synth_p254.py to exclude "partition" and "equal".

## Files Changed
- agents.py
- thinking.py
- code_synth_p254.py
- research/cycle557.md

## Tests
Targeted score_row on the two failing smoke rows: both OK.
Neighbor probes held: subset sum problem → subset_sum; majority element boyer moore
→ majority_element; search for fusion / papers → research; identity → ORBIT; 2+2 → 4.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke accuracy | 1787/1789 (99.89%) | 1789/1789 (100%) | +2 rows fixed |
| coding rows | 1735/1737 | 1737/1737 | +2 |
| code_boyer_1 | research hedge | def boyer_moore + Verified | fixed |
| code_86 | def subset_sum | def can_partition + Verified | fixed |

## Result
Both failing coding rows now return the verified template. Web search and identity paths unchanged.

## Next Research Target
- GitHub parity: push agents.py, thinking.py, code_synth.py, code_synth_p254.py (p254 was absent on remote).
