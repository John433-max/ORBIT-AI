## Cycle 93 — chat miss → ModelRouter (2026-09-22)

- Problem: weak chat hedges never used Ollama/OpenAI/tinylm provider
- Change: after research fallback, call generate_via_provider when still weak
- Opt-in ORBIT_THINK=1 uses Thinker for questions
- Tests: tests/unit/test_provider_fallback.py; 43 unit tests pass
