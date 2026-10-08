# Improvement Cycle 504

## Problem
Coding, search, and identity probes already passed. Smoke was 1618/1618. Several natural "write a function" asks still returned no template (sort people by height, merge 2d arrays by summing, diagonal prime, longest balanced substring, distinct-diagonal difference, minimum length after removals, closest primes). "average value of even numbers divisible by three" matched the two-argument `average` template.

## Research
HumanEval scores generated functions by executing hidden tests (Chen et al., 2021, https://arxiv.org/abs/2107.03374). ORBIT verifies templates against tiny examples before reporting Verified. Pack order is the default winner; a later template wins only when its name tokens are a strict superset present in the ask. Loading p220 first keeps specific matchers ahead of broad ones.

SOURCE: Chen et al., Evaluating Large Language Models Trained on Code, 2021. https://arxiv.org/abs/2107.03374
DATE: 2026-10-07
TECHNIQUE: example-checked phrase templates
WHAT IT IMPROVES: coding-path coverage for unmatched asks
REQUIREMENTS: no new dependencies
TRADE-OFFS: phrase templates are not a general code model
RELEVANCE TO ORBIT: smoke coding is template-backed
EXPECTED BENEFIT: eight new smoke rows verify; two-number average stays `def average`
IMPLEMENTATION PLAN: code_synth_p220, loader entry, smoke code_1580–1587, unit lock

## Finding
Those eight asks had no dedicated template. `average` was stealing the divisible-by-three phrasing because its matcher is broad and loaded later only wins on token score.

## Implementation
- code_synth_p220.py (8 templates)
- code_synth.py loads p220 first
- smoke code_1580–code_1587
- test_p220_sort_people_merge_diagonal_balanced

## Tests
- test_p220 passed
- new smoke rows scored via OrbitAI.ask

## Next
GitHub pack parity for p217–p220. Serve extras still optional (fastapi/uvicorn warning).
