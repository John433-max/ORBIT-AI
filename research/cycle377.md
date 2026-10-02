# Improvement Cycle 377

## Problem
Several natural-language coding asks still missed every template and fell through to the unimplemented stub: split-the-array (3046), two-occurrence substring (3090), valid word (3136), prefix min-cost (3502), length-3 distinct substrings (3258), and ops to make values equal k (3375).

## Research
Existing packs already cover nearby Easy problems (harshad, score of a string, faulty keyboard). Matchers must stay phrase-or-id specific so later packs do not steal `permute` or `reverse_string`.

## Finding
Those six prompts returned no template before this pack. Examples match the public LeetCode samples.

## Implementation
`code_synth_p100.py` with six verified templates. Loader lists `code_synth_p100`. Smoke rows `code_838`–`code_843`. Unit test `test_p100_split_twoocc_valid_cost_distinct_equal_k`.

## Tests
- p100 examples verify
- smoke 883/883 (was 877/877)

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke accuracy | 877/877 (100%) | 883/883 (100%) | +6 coding rows |
| templates | 842 | 848 | +6 |

## Result
New asks return verified functions. Prior probes unchanged: add-two-numbers verified, fusion search honest no-live-web, identity ORBIT.

## Next
Ollama still optional (no httpx). fastapi/uvicorn still a doctor warning.
