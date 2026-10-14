# Improvement Cycle 624

## Problem
Coding smoke row `code_2091` ("leaky relu") failed: Thinker classified the bare title as a statement, so OrbitAI.ask returned memory recall or the toy-scale hedge instead of the verified `leaky_relu` template from code_synth_p324.

## Research
Routing in thinking._is_code treats curriculum template hits (relu, sigmoid, tanh, leaky_relu, softmax) as conceptual lab demos even for bare implementation titles. Smoke expects synthesis + Verified for "leaky relu". Lab row "activation functions relu sigmoid" must stay lab.

## Finding
`leaky_relu` was listed in `curriculum_templates`, forcing `conceptual_lab=True` and blocking the template-hit code path. Removing only that name keeps other curriculum titles (relu/sigmoid) on the lab path for multi-word lab asks, while bare "leaky relu" synthesizes.

## Implementation
- thinking.py: drop "leaky_relu" from curriculum_templates so a verified bare title routes to code.

## Files Changed
- thinking.py
- research/cycle624.md

## Tests
- Thinker.classify("leaky relu") == "code"
- OrbitAI.ask("leaky relu") contains leaky_relu + Verified, no toy-scale
- classify("activation functions relu sigmoid") still lab
- classify("what is gradient descent") still lab
- tests/unit/test_thinking.py: 13/13 pass (direct)

## Benchmark
| Metric | Before | After | Difference |
|--------|--------|-------|------------|
| smoke accuracy | 2119/2120 (99.95%) | 2120/2120 (100%) | +1 row |
| coding | 2017/2018 | 2018/2018 | +1 |
| code_2091 | FAIL (memory/hedge) | PASS (synthesize) | fixed |

## Result
Bare "leaky relu" now synthesizes the verified educational function. Lab activation demo unchanged. Full smoke 100%.

## GitHub
Pushed thinking.py to main: 58ce884964fb049ccb8efe7451a58aa8b3258eac

## Next Research Target
GitHub pack parity (local p319–p328 not on main) or next unmatched coding phrase.
