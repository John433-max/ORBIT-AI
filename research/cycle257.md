# Improvement Cycle 257

## Problem
GitHub `code_synth_p1.py` is 12 098 B / ~24 templates. Local pack is 47 705 B / 68 templates.
Smoke on main already includes coding rows past `is_prime` (median, leap year, fizzbuzz, two_sum).

## Research
Local doctor READY; smoke 269/269 (coding 242/242). Probes:
- write a python function that adds two numbers -> coding_agent + Verified
- search for recent news about fusion energy -> research_agent
- what is your name -> main_chat_agent ORBIT identity

## Implementation
Full 47 KB p1 is awkward as one GitHub contents payload here.
Shipped a name-deduping loader plus `code_synth_p1b.py` (12 templates GH p1 is missing):
minimum, reverse_list, two_sum, median, title_case, count_occurrences, is_leap_year,
fizzbuzz, binary_search, transpose, is_anagram, dot_product.
Local unique count stays 253 (p1 already contains those names).

## Files
- code_synth.py (load p1b; skip duplicate names)
- code_synth_p1b.py (12 templates)
- research/cycle257.md

## Tests
- doctor: READY (fastapi/uvicorn warning, Ollama optional)
- smoke: 269/269
- pytest test_code_synth + test_thinking + test_agents: 92 passed
- probes pass as above

## Next
More p1 extras (merge_sorted through lis), then p2/p3 packs.
Do not overwrite GH thinking.py with a placeholder.
Do not overwrite slim GH agents.py with the 80 KB local file until CI-safe slim-parity is prepared.
