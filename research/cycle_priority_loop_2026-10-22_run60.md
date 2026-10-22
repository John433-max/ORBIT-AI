# ORBIT Improvement Run 60 — 2026-10-22

## Baseline
- doctor: READY (API deps warning, Ollama optional offline)
- smoke accuracy: 1.0 (2105/2105 from prior eval)
- probes: coding / search / identity all green

## Chosen priority
Serve/deps (priority 6): align requirements.txt + README with doctor/SETUP
(FastAPI optional via requirements-api.txt; CI already installs API extras).

## Changes
- requirements.txt: remove fastapi/uvicorn/httpx from "core required"; point
  to requirements-api.txt as the serve install path (comments only for those).
- README.md Installation: add `pip install -r requirements-api.txt` and note
  that core agents/TinyLM/eval work without FastAPI.

## Tests
- tests/unit/test_doctor_api_deps.py: 2 passed
- doctor READY; API deps still WARNING → requirements-api.txt
- probes: coding_agent, research_agent (no-live-web), main_chat identity

## Benchmark
| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke accuracy | 1.0 | 1.0 (not re-run full) | 0 |
| doctor severity for missing fastapi | warning | warning | aligned docs |

## Result
Kept. Docs and requirements now match doctor optional-API behavior.

## Next
Priority queue largely clear on local paths. Optional: install API deps in
this environment for serve smoke, or push full local agents.py if CI needs it.
