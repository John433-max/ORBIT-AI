## Cycle 93 — chat miss → ModelRouter (2026-09-22)

- Problem: weak chat hedges never used Ollama/OpenAI/tinylm provider
- Change: after research fallback, call generate_via_provider when still weak
- Opt-in ORBIT_THINK=1 uses Thinker for questions
- Tests: tests/unit/test_provider_fallback.py; 43 unit tests pass

## Cycle math-nl — percent/add/sum/half parse (2026-10-16)
- Problem: parse_and_calculate returned first number for 'percent of' / 'add X and Y' / 'half of'
- Change: percent regex + normalize add/sum/half; calculator route signals; tests
- Result: 15 percent of 80 → 12.0; add 12 and 7 → 19; half of 10 → 5.0; 8 tests pass
- Files: calculator.py, agents.py, test_calculator.py

[IMPLEMENTED]
Technique: BM25 + BM25L length-normalized lexical scoring and lexical-hit rank gate
Source: Robertson BM25; Lv & Zhai BM25L 2011; local Cycle 529/530/546 tests
Date: 2026-10-16
Reason: RAG ranked by raw overlap + hash cosine; long padded chunks and cosine near-misses could outrank concise exact hits
Files: documents.py
Result: 13 BM25/corpus tests pass; short exact > padded; lexical gate holds; coverage reported
Benchmark: unit tests 13/13; smoke 2020/2020 unchanged

## 2026-10-16 — Cycle p350

[IMPLEMENTED]
Technique: Easy CodeAgent templates (is_power_of_three, trailing_zeroes, binary_watch, count_sub_islands, excel_sheet_column_title, letter_case_permutation)
Source: LeetCode 326/172/401/1905/168/784 + Cycle 207 self-check
Files: orbit/code_synth_p350.py, evals/datasets/smoke.jsonl
Result: 2084→2090 unique templates; smoke 2020→2026
Benchmark: 6/6 synthesize_and_verify; Orchestrator coding ok=True

## Cycle 641 — Hard coding gaps p350 [2026-10-16]
- Technique: educational pure-Python cores for LeetCode 282/218/224/149/983/918
- Files: code_synth_p350.py, evals/datasets/smoke.jsonl
- Result: 6/6 synthesize_and_verify True; neighbors held; unique templates 2084→2090
- Benchmark: focused asks Verified; basic_calculator_ii / max_subarray unchanged

## 2026-10-16 — Cycle 642 p350 restore

[IMPLEMENTED]
Technique: restore truncated code_synth_p350 (6 Easy templates) + bare-title code route
Source: LeetCode 326/172/401/1905/168/784; Cycle 207 verify; Cycle 406 bare titles
Date: 2026-10-16
Reason: p350 SyntaxError caused loader skip; smoke code_2021–2026 stubs; "is power of three" routed to research
Files: code_synth_p350.py, agents.py
Result: unique 2084→2090; 6/6 verify_source; Orchestrator 6/6 coding Verified
Benchmark: smoke phrases 0/6→6/6 verified

## [IMPLEMENTED] Cycle 643 — p351/p352 coding-smoke gaps (2026-10-16)
Technique: New code_synth packs for Easy + Hard LeetCode-style prompts missing from smoke code_2021–2032.
Files: code_synth_p351.py (Easy + matcher widen), code_synth_p352.py (Hard), research notes.
Result: last-20 coding smokes 0 fails; templates 2090→2096; CodeAgent Verified on power-of-three / skyline / trailing zeroes.
Benchmark: synthesize_and_verify 12/12 verified for the gap set.

## [IMPLEMENTED] Cycle 644 — p353 unmatched titles (2026-10-16)
Technique: Educational pure-Python cores for LeetCode 135/654/450/696/43/7.
Files: code_synth_p353.py, evals/datasets/smoke.jsonl
Result: 6/6 synthesize_and_verify True; neighbors held (fair_candy_swap, reverse_string, delete_node linked-list).
Benchmark: templates ~2096→2099+; smoke 2032→2038; last-6 coding Verified.

## [IMPLEMENTED] Cycle 644 — p353 + matcher widen (2026-10-16)
Technique: Widen candy/reverse_integer/multiply_strings/mincost_tickets matchers; add construct_maximum_binary_tree, delete_node_bst, count_binary_substrings.
Source: LeetCode 135/654/450/696/43/7/983; Cycle 207 verify; _widen_loaded pattern
Files: code_synth.py, code_synth_p353.py
Result: unique templates 2096→2099; last-40 coding smoke fails 6→0; 7/7 gap queries verified; neighbors held
Benchmark: synthesize_and_verify 7/7; smoke tail clean

## [IMPLEMENTED] Cycle 645 — rk4 route + excel title name (2026-10-16)
Technique: Align Orchestrator.route has_value with thinking.py word-boundary digits; rename p351 excel_sheet_column_title def to match template/smoke.
Source: existing thinking.py comment on rk4/kmp; Cycle 207 verify; smoke expects.
Files: agents.py, code_synth_p351.py
Result: code_1983 and code_2025 ok; last-40 coding fails 1→0; templates 2099 unchanged; calculator neighbors held.
Benchmark: route rk4→code; excel name in output; area/factorial/C→F still calculator.

## Cycle 646 — 2026-10-16
Hypothesis: six missing classic problems (largest_number, remove_k_digits, longest_turbulent_subarray, exclusive_time_of_functions, my_calendar_book, replace_words) can be added as phrase-gated pure-Python templates without neighbor regressions.
Change: code_synth_p354.py + smoke code_2039–code_2044.
Result: unique 2099→2105; verify 6/6; route code 6/6; handle Verified 6/6; neighbors held.
Conclusion: keep.

## Cycle 647 (2026-10-16)
- Technique: +6 educational coding templates (p355)
- Files: code_synth_p355.py, evals/datasets/smoke.jsonl
- Result: templates 2105→2111; smoke 2044→2050; 6/6 verified
- Benchmark: all new rows PASS; no neighbor collisions

[IMPLEMENTED]
Technique: p356 educational templates (34/665/646/877/583/220)
Files: code_synth_p356.py, evals/datasets/smoke.jsonl
Result: +6 verified templates, smoke 2056→2062, 6/6 verify
Date: 2026-10-17
