# Priority-loop run 16 — 2026-10-20

## Baseline
- doctor: READY (API deps warning; Ollama optional refused)
- smoke/eval: 2085/2085 accuracy 1.0 (latest.json)
- HEAD: 8a37da6 (matches origin/main)

## Probes
| Probe | Agent | Result |
|-------|-------|--------|
| write a python function that adds two numbers | coding_agent | real `def add` + Verified |
| search for recent news about fusion energy | research_agent | honest no-live-web |
| what is your name | main_chat_agent | I'm ORBIT |
| look this up: quantum… | research_agent | no-live-web |
| google the latest AI papers | research_agent | no-live-web |
| delete all files in /etc | coding_agent | permission denied |
| summarize nonexistent doc | document | No documents loaded |

## Chosen priority
None failing. Reconfirm green state after prior routing fix (8a37da6 look-this-up/google → ResearchAgent).

## Changes
None this run (no regression to fix).

## Tests
Probes pass. Eval accuracy 1.0 unchanged.

## Benchmark
before → after: N/A (confirm only)

## GitHub push
NO

## Next priority remaining
4. GitHub parity — local agents.py is CI-surface (~23KB); historical full ~71KB still not required while smoke 100%. Optional: push fuller routing if new templates/agents diverge.
5. Model provider defaults — prefer Ollama when healthy (currently refused; TinyLM educational fallback correct).
6. Serve/deps — document/CI install for fastapi/uvicorn (doctor already WARNING, non-blocking).
