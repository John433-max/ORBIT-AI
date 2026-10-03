# Cycle 401 — unmatched coding pack p122

## Problem
Natural-language coding prompts for LeetCode 3295, 3318, 3324, 3471, 3576, and 3643 fell through to the unverified draft stub.

3289 (sneaky numbers) and 3300 (min element after digit sum) are missing from smoke ids but already implemented in `code_synth_p57.py`. Repeating them would not add a new function.

## Research
Official examples from leetcode.doocs.org statements:

- 3295 Report Spam Message (Medium): spam if at least two message words are in `bannedWords`. `["hello","world","leetcode"]` / `["world","hello"]` → true; `["hello","programming","fun"]` / `["world","programming","leetcode"]` → false.
- 3318 Find X-Sum of All K-Long Subarrays I (Easy): keep the top-x frequencies, breaking ties by larger value. `[1,1,2,2,3,4,2,3], k=6, x=2` → `[6,10,12]`; `[3,8,7,8,7,5], k=2, x=2` → `[11,15,15,15,12]`.
- 3324 Find the Sequence of Strings Appeared on the Screen (Medium): key 1 appends `a`, key 2 increments the last character. `"abc"` → `["a","aa","ab","aba","abb","abc"]`; `"he"` → `["a"…"h","ha"…"he"]`.
- 3471 Find the Largest Almost Missing Integer (Easy): value in exactly one window of length k. `[3,9,2,1,7], k=3` → 7; `[3,9,7,2,1,7], k=4` → 3; `[0,0], k=1` → -1.
- 3576 Transform Array to All Equal Elements (Medium): adjacent pair sign flips, at most k. `[1,-1,1,-1,1], k=3` → true; `[-1,-1,-1,1,1,1], k=5` → false.
- 3643 Flip Square Submatrix Vertically (Easy): reverse rows of the kxk square at (x, y). Official grids match the copied-matrix implementation.

## Implementation
- `code_synth_p122.py` six verified templates.
- Loader prefers `code_synth_p122`.
- Smoke `code_972`–`code_977`.
- Matchers are title/id specific. 3576 does not steal 3467 transform-by-parity. 3471 does not steal a generic largest-integer ask.

## Sources
- https://leetcode.doocs.org/en/lc/3295/
- https://leetcode.doocs.org/en/lc/3318/
- https://leetcode.doocs.org/en/lc/3324/
- https://leetcode.doocs.org/en/lc/3471/
- https://leetcode.doocs.org/en/lc/3576/
- https://leetcode.doocs.org/en/lc/3643/

## Tests
pytest is not installed in this environment. Direct probe of `synthesize_and_verify` on all six prompts: verified true, examples checked 2/2/2/3/2/2. Neighbor prompts still resolve to `transform_array` (3467) and do not hit `report_spam` / `largest_almost_missing`. p121 prefix-suffix still matches.

## Benchmark
Template load + six synthesize/verify calls: 13.206 s, peak traced memory 3.91 MB (includes full pack import, not decode). No token/s change; coding-route coverage +6 unmatched titles.

## Result
Keep. Six previously unmatched prompts now return verified template source.

## Next
Another unmatched Easy pack, or GitHub pack parity for p122.
