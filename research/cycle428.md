# Improvement Cycle 428

## Problem
Coding asks such as "implement candy leetcode 135", "paint house leetcode 256", "out of boundary paths leetcode 576", "champagne tower 799", "new 21 game 837", and "predict the winner 486" routed to a NotImplementedError stub (or, for bare "leetcode N" with no implement/write, to main chat and the toy-scale hedge).

## Research
Existing pattern (Cycle 207 / 405): deterministic templates with official LeetCode examples as self-checks; ROUTES strict pattern must include leetcode ids or score_request returns chat. Problem ids must be whole tokens (135 must not match 1351).

## Implementation
- code_synth_p149.py: six verified templates (candy alias, paint house, out-of-boundary paths, champagne tower, new 21 game, predict the winner).
- code_synth.py loader lists p149 before older packs.
- agents.py ROUTES code pattern includes `\bleetcode\s*\d+`.
- smoke rows code_1126–code_1131.

## Tests
Probes: coding verified, identity stays ORBIT, fusion search stays research_agent.
Smoke after whole-id matcher fix: 1172/1172.

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke | 1166/1166 (100%) | 1172/1172 (100%) |
| coding | 1123/1123 | 1129/1129 |

## Next
GitHub still missing packs after p137; push p149 + loader + agents route + smoke.
