# Improvement Cycle — API deps install hint

## Problem
Doctor warned that fastapi/uvicorn were missing and told users to `pip install -r requirements.txt`. Those packages are optional serve extras in `requirements-api.txt`. CI workflows only installed `requirements.txt`, so serve imports never ran on GitHub Actions.

## Research
SETUP.md already documents `pip install -r requirements-api.txt`. Doctor severity for missing API deps is a non-blocking warning (keep that).

## Implementation
- `check_environment` and the serve ImportError now point at `requirements-api.txt`.
- `.github/workflows/tests.yml` and `ci.yml` install `requirements-api.txt` and import fastapi/uvicorn.
- `tests/unit/test_doctor_api_deps.py` locks the hint and the workflow step.

## Tests
- `python tests/unit/test_doctor_api_deps.py` assertions
- `py_compile` on `run_orbit.py`
- `run_orbit.py doctor` READY; API deps row cites `requirements-api.txt`
- Smoke not re-run: no routing/agent change. Prior smoke 1459/1459 (1.0) on 2026-10-06T22:10:52Z.

## Benchmark
| Metric | Before | After |
|---|---|---|
| doctor API hint | requirements.txt | requirements-api.txt |
| CI installs API extras | no | yes |
| smoke accuracy | 1.0 (1459/1459) | unchanged (not re-run) |
