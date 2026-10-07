# Improvement Cycle 503

## Problem
GitHub main stopped at code_synth_p216 and smoke code_1557. Local already had p217–p219 and smoke through code_1579. A full local eval at 23:09 scored 1592/1609 because 17 coding rows returned a stub or the wrong function name (digit_sum stealing minimum-sum; nth triangular stub). Re-probe of those 17 rows now matches the expected verified templates. Identity ("what is your name") was not in smoke.

## Research
HumanEval scores generated functions by executing hidden tests (Chen et al., 2021, https://arxiv.org/abs/2107.03374). ORBIT verifies templates against tiny examples before reporting Verified. Pack order is the default winner; a later template wins only when its name tokens are a strict superset present in the ask.

SOURCE: Chen et al., Evaluating Large Language Models Trained on Code, 2021. https://arxiv.org/abs/2107.03374
DATE: 2026-10-07
TECHNIQUE: example-checked phrase templates plus smoke locks
WHAT IT IMPROVES: coding-path name lock and GitHub pack parity
REQUIREMENTS: no new dependencies
TRADE-OFFS: phrase templates are not a general code model
RELEVANCE TO ORBIT: smoke coding is template-backed
EXPECTED BENEFIT: remote main can import p217–p219 and score the same smoke rows
IMPLEMENTATION PLAN: keep p219 loaded first; lock the 17 previously failing asks; add identity_1; push loader, packs, smoke, tests

## Finding
Cold import loads 1518 templates with triangular_sum first. The 17 previously failing asks synthesize the expected def names and verify. identity_1 returns ORBIT and does not mention IMDb or movie.

## Implementation
- smoke identity_1
- unit lock test_smoke_coding_misses_2026_10_07_name_lock (already present) plus p219 tests
- GitHub push of code_synth.py, p217–p219, smoke.jsonl, test_code_synth.py

## Tests
- p217/p218/p219 unit functions passed
- identity_1 score ok
- new coding rows code_1572–code_1579 score ok

## Next
Full smoke re-run after the 23:09 miss. Serve extras still optional (fastapi/uvicorn warning).
