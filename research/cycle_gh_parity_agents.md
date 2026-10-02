# Improvement Cycle GH-parity agents+thinking

## Problem
Local coding, search, and identity probes pass, and smoke eval is 785/785.
GitHub main still served a 15,911-byte agents.py and a 9,865-byte thinking.py
(CI restore). Local agents.py is 85,303 bytes (full orchestrator) and thinking.py
is 13,925 bytes (debug/file/data routes, code-before-math).

## Research
Routing stays keyword/rule-based (DESIGN.md). No new algorithm. Parity is the
gap: remote CI and clones could not reproduce the local code/search/identity path.

## Implementation
Copy tested local agents.py and thinking.py onto main. No secrets. Did not
overwrite code_synth.py (byte-identical) or run_orbit.py (same size).

## Tests
- doctor READY
- eval 785/785 (100%) before push
- probes: add-two-numbers → CodeAgent verified function; fusion search → sources;
  name → ORBIT identity
- pytest tests/unit/test_thinking.py test_agents.py test_permissions_and_state.py
  test_provider_fallback.py: 54 passed

## Benchmark
| Metric | Before (GH) | After (local, pushed) |
|---|---:|---:|
| agents.py bytes | 15911 | 85303 |
| thinking.py bytes | 9865 | 13925 |
| smoke accuracy | 785/785 | 785/785 (unchanged) |

## Next
Serve extras (fastapi/uvicorn) still optional-missing. Ollama probe needs httpx.
