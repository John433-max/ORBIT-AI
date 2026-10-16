# Improvement Cycle — GitHub parity + coding/calculator polish

## Problem
Local tree was ahead of origin/main with uncommitted routing, matcher, and calculator improvements. Smoke had been 2051/2062 (99.47%); new rows and word-math forms were untested on main.

## Research
- Bare coding titles ("is power of three") match verified templates but look like questions; route should still prefer code when no "?" and no explain/what-is form.
- Calculator word forms ("15 percent of 200", "add 3 and 5", "half of N") are common and were only partially covered.
- code_synth matchers for candy / reverse_integer / multiply_strings / mincost_tickets needed widening without neighbor collisions (existing _widen_loaded pattern).

## Implementation
- agents.py: bare_title route exception; word-boundary digit check for has_value; fallback metering on python.execute / web.search.
- calculator.py: percent/add/sum/half word normalizers.
- code_synth.py: widened matchers.
- thinking.py: "list my files".
- documents.py: BM25L + section-aware chunking (already in tree).
- tools/chat_tool.py: per-conversation KV session map.
- smoke.jsonl: code_2021–code_2065.
- code_synth_p350–p356 and remaining untracked packs.

## Tests
- Full smoke: 2065/2065 = 100% (was 2051/2062).
- Unit: tests/unit/test_code_synth.py + test_calculator.py → 334 passed.
- Probes: code route + Verified; search → research_agent with live results; identity → ORBIT.

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke accuracy | 0.9947 (2051/2062) | 1.000 (2065/2065) |
| coding | 1989/2000 | 2003/2003 |
| search | 9/9 | 9/9 |
| unit (synth+calc) | — | 334 passed |

## Result
Keep. Push focused files + packs to main.
