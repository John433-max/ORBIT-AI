# Improvement Cycle 304

## Problem
GitHub main is missing several local code_synth packs (p28–p32, p41).
CI still collects because `code_synth.py` skips missing packs, but GH coding
coverage lags the local 525-template set.

## Research
No new algorithm. Priority 4 (GitHub parity) after local probes passed.

## Implementation
Push tested local packs p28–p32 and p41 to main. Do not overwrite slim
`agents.py` (16KB remote vs 85KB local).

## Tests
- doctor READY (fastapi/uvicorn warning, Ollama optional)
- latest smoke 534/534 accuracy 1.0
- probes: coding sandbox + verified add; research_agent fusion news;
  identity ORBIT
- pytest tests/unit/test_code_synth.py + test_thinking.py: 84 passed

## Next
Push p2/p3 (large) or slim-parity agents.py; fastapi serve extras.
