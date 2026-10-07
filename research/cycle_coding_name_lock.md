# Improvement Cycle — coding name lock (2026-10-07)

## Problem
Smoke eval at 23:09 scored 1592/1609 (98.94%). All 17 misses were coding:
name mismatches (`digit_sum` / `pivot_integer` / `minimum_sum` vs expected defs)
or NotImplemented stubs (LeetCode 2409/2894/2529/2446/2220/2215/2210 and
sha1/crc32/dice/thousands/query/hms/triangular).

## Finding
Packs edited at 23:05 (p67/p68/p169 matchers, p217–p219, code_synth loader)
already return the expected defs. The 23:09 eval raced those writes.
Rescore of the 17 prompts through Orchestrator.handle: 17/17.

## Implementation
- Regression `test_smoke_coding_misses_2026_10_07_name_lock` locks the 17 asks
  to template name + verified source, and keeps triangular_sum off nth triangular.
- GitHub main was missing p217–p219 and the p67/p68/p169 matcher tightenings.

## Tests
- name-lock function: PASS
- probes: add-two-numbers → coding_agent `def add`; fusion search → research_agent;
  "what is your name" → ORBIT identity (main_chat_agent).
