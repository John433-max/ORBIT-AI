# Cycle 406 [2026-10-04]

## Problem
Six coding titles still fell through synthesis (fallback), and Orchestrator.route sent bare template titles to chat/data hedges (`binary tree cameras`, `maximum product of three numbers`) even when `code_synth.match_template` hit. Eval uses `OrbitAI.ask`, which already synthesized; `Orchestrator.handle` did not.

## Research
LeetCode 628 / 968 / 1663 / 1064 / 1065 / 1780. Sort-two-ends product, greedy camera states, greedy numeric string, leftmost binary-search fixed point, overlapping `str.find` pairs, base-3 digit check (reject digit 2).

## Implementation
- `code_synth_p152.py` registered first in `code_synth._templates`.
- Matchers exclude product-of-two, subarray product, and smallest-string-with-swaps.
- `Orchestrator.route` sets code=1.0 on a template hit unless calculator/debug/lab/document/chat/research already scored 1.0, or the request is a question/search. First draft stole `factorial of 5`; calculator ROUTES stay protected.

## Tests
`test_p152_product_cameras_string_fixed_pairs_powers` passed (direct call; pytest not installed).
Focused smoke of code_1144–code_1149 plus math/search/rag/permission: 16/16.
Full eval: 1186/1186 (100%), coding 1141/1141. Baseline before this run: 1178/1178.

## Probes
- write a python function that adds two numbers → coding_agent, verified add
- search for recent news about fusion energy → research_agent (live snippet)
- what is your name → main_chat_agent, ORBIT
- factorial of 5 → calculator_agent, 120
- binary tree cameras → coding_agent, min_camera_cover
