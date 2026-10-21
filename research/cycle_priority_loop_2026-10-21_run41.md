# ORBIT Improvement Run — 2026-10-21

## Baseline
- doctor: READY (PyYAML optional, API deps WARNING, Ollama OPTIONAL down)
- smoke accuracy: 1.0 (2101/2101, 427.8s) from full eval
- probes:
  - coding add → coding_agent, `def add` Verified
  - search fusion news → research_agent, honest "No live web available"
  - identity → "I'm ORBIT…"
  - **what is the capital of France → generic hedge** (failing)

## Chosen priority
Research/search quality for unmatched factual questions, plus TinyLM generate restore (provider path was dead).

## Research
- Explicit search verbs already route to ResearchAgent (priority 2 green).
- Unmatched question-form asks ("what is the capital of France") hit MainChatAgent and returned the generic "How can I help?" hedge. The weak-chat detector only matched toy-scale / short text, so research and model fallback never ran.
- `tinylm.generate` was missing. `generate_chat_tinylm` and TinyLMProvider.generate failed with `No module named 'tinylm.generate'` even though health_check passed.
- Provider auto already prefers Ollama when healthy (router.py). Ollama is down here, so TinyLM is the educational fallback and must not invent facts.

## Changes
- `agents.py`: treat the generic ORBIT hedge as weak for question-form asks. Prefer a healthy non-TinyLM provider, else ResearchAgent (honest no-live-web), else TinyLM provider.
- `orbit_ai.py`: wire `ModelRouter` into Orchestrator so the facade sees the configured provider.
- `tinylm/generate.py`: restore `generate_numpy` / `sample_numpy` / `bench_numpy` (and torch wrappers) so chat.generate and the provider can decode.
- smoke row `search_general_1` + unit tests for hedge→research and generate_numpy.

## Tests
- unit: generate greedy/eos, weak-chat provider, hedge→research — pass
- probes: capital → no live web; coding/search/identity/hi/time unchanged
- targeted eval (all non-coding + 50 coding): 120/120
- chat.generate: ok=True (was missing module)

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| "what is the capital of France" | generic hedge | honest "No live web available…" |
| tinylm.generate import | ModuleNotFoundError | generate_numpy works |
| chat.generate ok | False | True |
| targeted smoke | — | 120/120 |
| full smoke (prior) | 1.0 (2101) | +1 row; non-coding still green |

## GitHub push
Focused files if credentials allow.

## Next priority remaining
Priorities 1–3 green. Optional: fastapi extras install in CI, longer TinyLM persona quality, full smoke re-run after this row.
