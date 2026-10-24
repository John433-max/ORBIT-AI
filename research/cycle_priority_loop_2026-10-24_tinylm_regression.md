# ORBIT Improvement Run — TinyLM regression module restore

Date: 2026-10-24

## Baseline
- doctor: READY (API deps warning; Ollama optional down)
- smoke accuracy: 2109/2109 = 1.0 (evals/results/latest.json)
- probes: coding real `def add`+Verified; search honest no-live-web; identity ORBIT
- unit subset: thinking+provider+code_route+model_providers 36 passed
- gap: `status()['tinylm_lab']` reported `No module named 'tinylm.regression'`
  (tools/tinylm_lab.py + tinylm/cli.py import run_regression; file missing)

## Chosen priority
Priority queue 1–4 already green (coding/search/eval/GitHub parity).
Small highest-value fix: restore educational TinyLM regression suite so lab tool
and `OrbitAI.status()` report available=True.

## Research
- Local callers expect `run_regression() -> {ok: bool, checks: [{name, ok, detail?}]}`
- No bytecode/source recovery; implement minimal NumPy suite matching lab contract.

## Changes
- Added `tinylm/regression.py`:
  - imports / from_config
  - forward logits shape
  - greedy deterministic generate
  - cache_vs_full (use_cache when supported)
  - bench_numpy positive throughput

## Tests
- `run_regression()` → ok=True, 6/6 checks pass
- TinyLMLabTool action=regression → ok, content lists all pass
- TinyLMLabTool action=bench → ~1604 tok/s toy
- OrbitAI.status tinylm_lab: available=True, regression_ok=True
- probes still pass; unit 36 pass

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| tinylm_lab.available | False (missing regression) | True |
| regression_ok | n/a / error | True |
| smoke accuracy | 1.0 | 1.0 (unchanged) |
| coding/search/identity probes | pass | pass |

## GitHub push
YES — focused files via GitHub connector.

## Next priority remaining
- Serve/deps: optional fastapi/uvicorn install docs already noted by doctor
- Prefer Ollama when healthy (already in orbit/models/router.py auto path)
- Keep smoke ≥ 2109 and CI green on main
