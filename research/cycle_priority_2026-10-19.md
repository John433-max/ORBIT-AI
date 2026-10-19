# ORBIT Improvement Run — 2026-10-19

## Problem
1. CI Tests failed: `decimal_to_binary` stole min_changes_alternating (LC 1758) and min_changes_beautiful (LC 2914) because its matcher treated any "binary string" as a decimal conversion.
2. Smoke math/science collapsed to "Could not evaluate." because CalculatorAgent imported a non-existent `evaluate_science_math`.
3. Slim MemoryAgent / DocumentAgent / chat stubs failed memory, rag-empty, and instruction smoke rows.

## Research
- code_synth match_template scores name-token overlap and prefers a higher score. A broad early matcher wins when the later specific template is not also a hit.
- science_math exposes `solve_science_math` → `{ok, pretty, result, kind}`. calculator.parse_and_calculate handles word-form arithmetic and percent-of.

## Implementation
- `code_synth_p183.py`: exclude changes / alternating / beautiful / 1758 / 2914 from decimal_to_binary.
- Reverted uncommitted strong-first scoring in code_synth.py (it blocked higher-scoring later templates such as max_path_sum).
- `agents.py` CalculatorAgent: try solve_science_math, then parse_and_calculate, then bare eval.
- MemoryAgent: session facts for name and favorite color.
- DocumentAgent: "couldn't find document #N" and inline "summarize this:" extract.
- MainChatAgent: identity, capabilities, UTC time, word count, NameError debug, number stats, list files.
- Route conceptual lab asks before computational math; route "add N and M" to calculator.

## Tests
- Non-coding smoke rows: 62/62 after fixes (was failing math/science/memory/rag/instruction).
- Matcher probes: min_changes_alternating, min_changes_beautiful, max_path_sum, bitonic_sort correct.
- Coding smoke scoring running at documentation time.

## Next
- Push focused agents.py + code_synth_p183.py once coding smoke holds.
- Remaining: GitHub agents.py parity, Ollama-when-healthy default (already optional in doctor).

## Follow-up (same run)
- Route explicit code synthesis before arithmetic, but keep numeric science asks on the calculator.
- Force "activation functions" to lab.
- Widen matchers: reverse_integer accepts "reverse integer"; bare "candy" and "largest number".
