# Cycle 384 — code_synth p106 Easy pack

## Problem
Smoke coding path was already 915/915. GitHub main stopped at p104; local p105 was unpublished. Next coding gap was Easy prompts not in the template index.

## Research
LeetCode 1979 is GCD of min and max, not of every element (official example [2,5,6,9,10] → 2). 1984 is a sliding window on sorted scores. 2164 places sorted even-index values ascending and odd-index values descending. 2273 drops a word only when it is an anagram of the previous kept word. 2287 is min count ratio. 3014 Word I assigns distinct letters onto 8 keys, so cost is `sum(i // 8 + 1)`.

## Implementation
- `code_synth_p106.py` loaded before p105/p1 so the array-GCD matcher wins over the two-argument gcd template.
- Smoke rows code_876–code_881.
- Unit test keeps gcd / sort_list / is_anagram regressions.

## Result
Smoke 915/915 → 921/921. Coding 875 → 881. p106 unit test passed after correcting 1979 to GCD(min, max).

