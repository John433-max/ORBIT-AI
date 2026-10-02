# Improvement Cycle — Ollama stdlib transport

## Problem
`auto` provider routing prefers Ollama only when `health_check()` is ok.
That check imported `httpx` and treated `ModuleNotFoundError` as "Ollama down",
so a running daemon was unreachable in checkouts that skipped API extras.
Doctor reported `No module named 'httpx'` instead of a connection result.

## Research
Ollama's HTTP API (`GET /api/tags`, `POST /api/generate`, `POST /api/chat`)
is plain JSON. The Python stdlib `urllib.request` can speak it. httpx remains
preferred when installed (same client CI already pins in requirements.txt).

## Implementation
`orbit/models/ollama.py`: `_http_json` tries httpx, falls back to urllib.
Health payload includes `transport=httpx|urllib`.

## Tests
`tests/unit/test_model_providers.py::test_ollama_urllib_health_and_generate_without_httpx`
Local fake daemon (httpx not installed): health ok, generate + chat text match.

## Benchmark
| Metric | Before | After |
|---|---|---|
| Doctor Ollama detail | `No module named 'httpx'` | `<urlopen error [Errno 111] Connection refused>` (honest: no daemon) |
| Fake daemon health | impossible without httpx | ok, transport=urllib |
| Smoke accuracy | 877/877 | unchanged (routing code not on eval path) |

## Next
Serve extras still optional. Install `requirements-api.txt` when running `serve`.
