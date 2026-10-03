# Cycle 400 — unmatched coding pack p121

## Problem
Natural-language coding prompts for LeetCode 3042, 3069, 3010, 3095, 1769, and 3233 fell through to the unverified draft stub.

An earlier draft of this pack reused titles already in smoke (2544, 2574, 2716, 2769, 3028) and stole those rows because newer packs load first. That draft was replaced.

## Research
Official examples from doocs/leetcode README_EN:
- 3042 Count Prefix and Suffix Pairs I: ["a","aba","ababa","aa"] → 4; ["pa","papa","ma","mama"] → 2; ["abab","ab"] → 0.
- 3069 Distribute Elements Into Two Arrays I: [2,1,3] → [2,3,1]; [5,4,3,8] → [5,3,4,8].
- 3010 Divide an Array Into Subarrays With Minimum Cost I: first cost is nums[0]; other two starts are the two smallest later values. [1,2,3,12] → 6; [5,4,3] → 12; [10,3,1,1] → 12.
- 3095 Shortest Subarray With OR at Least K I: [1,2,3], k=2 → 1; [2,1,8], k=10 → 3; [1,2], k=0 → 1.
- 1769 Move All Balls to Each Box: "110" → [1,1,3]; "001011" → [11,8,5,4,3,4].
- 3233 Count of Numbers Which Are Not Special: special = square of a prime. [5,7] → 3; [4,16] → 11.

## Implementation
- code_synth_p121.py six verified templates.
- Loader prefers code_synth_p121.
- Smoke code_966–code_971. Restored code_960–code_965 after a filter bug.
- Matchers are title/id specific. 3065 stays on the existing min_operations template.

## Sources
- https://github.com/doocs/leetcode/blob/main/solution/3000-3099/3042.Count%20Prefix%20and%20Suffix%20Pairs%20I/README_EN.md
- https://github.com/doocs/leetcode/blob/main/solution/3000-3099/3010.Divide%20an%20Array%20Into%20Subarrays%20With%20Minimum%20Cost%20I/README_EN.md
- https://github.com/doocs/leetcode/blob/main/solution/3000-3099/3028.Ant%20on%20the%20Boundary/README_EN.md (not used; already covered)
- https://leetcode.com/problems/count-the-number-of-special-integers/ (3233 statement: special = prime square)
