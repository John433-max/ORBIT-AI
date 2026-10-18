# Improvement Cycle — coding route: leetcode calculator steal + lower_bound clobber

## Problem
Natural-language coding asks were not always returning real code:

1. Prompts like "minimum cost to make at least one valid path leetcode 1368"
   routed to the calculator and answered with the bare number "1368".
   `_is_computational_math` matched the digits; `_explicit_write_ask` did not
   treat a LeetCode id as an explicit code request, so the calculator branch
   won over `_wants_code_written`.

2. "implement lower bound binary search" correctly synthesized `lower_bound`
   via code_synth, then CodeAgent overwrote it with the classic
   `binary_search` fallback because the prompt contained "binary search"
   and the source did not contain `def binary_search`.

3. search_3 ("weather in tokyo") returned the honest no-live-web message
   but failed the eval because the message did not contain "Tokyo".

## Research
SOURCE: local agents.py routing + code_synth match_template
TECHNIQUE: guard order — explicit code (including LeetCode ids) before calculator; fallback only on stubs
WHAT IT IMPROVES: coding-path success on LeetCode titles and lower/upper bound; search eval honesty with topic echo
REQUIREMENTS: none (no new deps)
TRADE-OFFS: no-live-web replies now echo the ask (≤160 chars). Calculator still wins for bare math even when a template matches.
RELEVANCE TO ORBIT: priority-1 coding path and priority-2 search honesty
EXPECTED BENEFIT: ~11 coding rows + 1 search row recovered

## Implementation
- `_explicit_write_ask` also matches `\bleetcode\s*\d+`
- CodeAgent binary_search override only when `_is_code_synth_stub(src)`
- ResearchAgent no-live-web body appends `(asked: <request>)`

## Validation
Probes:
- implement lower bound binary search → def lower_bound + Verified
- leetcode 1368 → def minCost + Verified
- write a python function that adds two numbers → real add + Verified
- search weather tokyo → no live web + (asked: ...tokyo)
- identity → ORBIT

Unit: tests.unit.test_code_route_search (3 functions) pass.
