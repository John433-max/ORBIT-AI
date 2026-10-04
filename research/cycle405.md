# Improvement Cycle 405

## Problem
Coding asks that say `implement <problem>` without the word `function` were routed to the code agent, then executed as Python. Sandbox rejected them with `syntax error: invalid syntax`. Separate asks for next greater element III (556), city skyline (807), and bulls and cows (299) synthesized draft stubs.

## Research
LeetCode problem statements (examples only, not copied solutions):
- 556: next permutation of digits; 12 -> 21; 21 -> -1; no greater or > 2^31-1 -> -1.
- 807: raise each cell to min(row max, col max). Official grid -> 35.
- 299: bulls = same index, cows = shared digits minus bulls. "1807"/"7810" -> "1A3B"; "1123"/"0111" -> "1A1B".

## Finding
`_wants_code_written` required `function|code|python` within a short window of `implement`. Thinker already classified these as coding, so the miss became a sandbox syntax error instead of synthesis. A leetcode-id / leading implement|write gate returns code (or a draft) without executing the sentence.

## Implementation
- Broaden `_wants_code_written` for `leetcode N` and leading `implement`/`write` that is not already a Python statement. Fenced snippets still execute.
- `code_synth_p127.py` for 556, 807, 299. Loader lists p127 first.
- Smoke code_1002–code_1005 (atoi without the word function).
- Unit test `test_p127_next_greater_iii_skyline_bulls`.

## Files Changed
- agents.py
- code_synth.py
- code_synth_p127.py
- evals/datasets/smoke.jsonl
- tests/unit/test_code_synth.py
- research/cycle405.md

## Tests
Direct call of the new unit test passed. `print(2 + 2)` still sandbox stdout 4. Next-greater element I still `next_greater_element`.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| Smoke rows | 1041 | 1045 | +4 |
| Smoke accuracy | 1041/1041 | 1045/1045 | held |
| implement skyline (Thinker) | toy-scale hedge / memory dump in eval | verified function | fixed |
| implement atoi (Thinker) | toy-scale hedge / memory dump in eval | verified myAtoi | fixed |
| 556 / 299 | draft stub | verified | fixed |

## Result
Kept. Eval path uses Thinker, so `_is_code` needed the same gate as CodeAgent. First eval after only the CodeAgent change was 1043/1045; after the Thinker fix, 1045/1045.

## Problems
GitHub main still lacked `code_synth_p126.py` at the start of this run.

## Next Research Target
Reconstruct itinerary (332) still stubs after the route fix. Push remaining local packs if this commit does not include them.

