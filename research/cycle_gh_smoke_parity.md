# Improvement Cycle — GH smoke parity 2026-10-07

## Problem
Coding, search, and identity probes already pass locally. GitHub `evals/datasets/smoke.jsonl` was a 113-byte placeholder (`PLACEHOLDER_TOO_LARGE_SEE_LOCAL`), so remote clones could not reproduce the 1586-row smoke eval.

## Research
No new algorithm. Parity gap recorded in commit a10e46f ("GH smoke needs restore from local"). GitHub Contents API / git accepts the 286 KB JSONL (well under the 100 MB blob limit).

## Implementation
Copied local `evals/datasets/smoke.jsonl` onto main. No secrets. No agent or template changes.

## Tests
- doctor: READY (3 non-blocking: PyYAML, fastapi/uvicorn, Ollama refused)
- eval before push: 1586/1586 (100%) in 188s
- probes: add-two-numbers → verified `add`; fusion search → live sources; name → ORBIT identity

## Benchmark

| Metric | Before | After |
|---|---:|---:|
| GH smoke.jsonl bytes | 113 | 285787 |
| smoke rows | 1 placeholder | 1586 |
| local accuracy | 1586/1586 | 1586/1586 (unchanged) |

## Result
Pushed `58d3248370b37af5ebf425b7bf0ffb3196daa256`.

## Next
Serve extras still optional locally (CI already installs fastapi/uvicorn). Ollama is optional-down. Remaining Easy templates can be added to smoke if coverage still lags the pack library.
