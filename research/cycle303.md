# Improvement Cycle 303

## Problem
Coding eval coverage still grows one Easy pack at a time. Local path already
routes "write a function…" to CodeAgent; missing templates fall through.

## Research
Continue verified template packs (HumanEval-style examples on each Template).
Rejected `destination_city` — already covered as `dest_city`.

## Implementation
- Added `code_synth_p42.py` (6 Easy templates): count_pairs_of_similar_strings,
  sum_of_squares_of_special, max_ascending_subarray, count_largest_group,
  balanced_string_split, defuse_the_bomb.
- Loader lists `code_synth_p42`.
- Smoke rows code_489–code_494.
- Unit `test_p42_similar_squares_ascending_dest_split_bomb`.

## Tests
- doctor READY (fastapi/uvicorn warning, Ollama optional)
- smoke 534/534 (coding 494/494)
- test_code_synth 79 passed
- probes: coding Verified; search research_agent honest no-live-web; identity ORBIT

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke | 528/528 | 534/534 |
| coding rows | 488 | 494 |
| templates | 519 | 525 |

## Next
GitHub parity: push p41 + p42 + smoke + loader. Keep slim agents.py on GH.
