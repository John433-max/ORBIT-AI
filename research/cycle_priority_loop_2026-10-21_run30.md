# ORBIT Improvement Run 30 — 2026-10-21

## Problem
Coding path missed natural "how do I / how to / how can I … in python" phrasing
(routed to explain/chat hedge). Bare algorithm titles also matched "how does X work".

## Research
Internal routing patterns in `_wants_code_written`; prior cycles already handle
write/implement/leetcode. Need positive match for how-to + coding cues without
stealing pure science or explanation asks.

## Finding
Add early positive regex for (how do i|how to|how can i) + (in python|function|
implement|write|code|reverse|sort|binary search|…). Guard out "how does" and
numeric calculate/compute. Split bare algorithm title match so explain verbs
exclude it.

## Implementation
- agents.py: `_wants_code_written` — how-to block + bare-title explain guard
- evals/datasets/smoke.jsonl: +5 coding rows (code_howto_1..5)

## Tests
- Syntax OK
- Unit asserts on 10 routing cases ALL OK
- Live probes: how-do-I reverse → verified code; how does binary search → non-code;
  write add → verified; search → no live web; identity → ORBIT
- Eval: accuracy 1.0, coding 2026/2026 (was 2021), total n=2095 (was 2090)

## Benchmark before → after
| Metric | Before | After |
|--------|--------|-------|
| smoke accuracy | 2090/2090 (100%) | 2095/2095 (100%) |
| coding rows | 2021 | 2026 |
| how-do-I reverse route | fail / hedge | code + Verified |

## Result
Real improvement kept. Coding priority strengthened for natural language how-to asks.

## Next
GitHub parity (push agents.py + smoke), model provider Ollama prefer, serve deps docs.
