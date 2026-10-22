# ORBIT Improvement Run 51 — 2026-10-22

## Baseline
- doctor: READY (API deps WARNING, Ollama OPTIONAL refused)
- smoke/eval accuracy: 2101/2101 = 1.0 (coding 2030, search 13, rag 10, permission 11)
- probes (prior run): coding / research honest offline / ORBIT identity all green

## Chosen priority
Educational routing gap: "how does a neural network work" / "what is a neural network" hit research_fallback (honest offline) instead of LabAgent. Priorities 1–4 already green; this is a small lab-path completeness fix aligned with educational ML demos.

## Changes
- `lab_agent.py`: expand `looks_like_lab` for neural network / transformer conceptual phrases; map NN → `three_neurons`, transformer → `next_token`
- `thinking.py`: same patterns in `_is_lab`
- `agents.py`: fallback `_looks_like_lab` includes neural network | transformer

## Tests
- doctor READY
- probes:
  - "how does a neural network work" → lab three_neurons demo
  - "how does a transformer work" → lab next_token demo
  - coding add / reverse still code_synth Verified
  - search fusion → honest no live web
  - identity → ORBIT
  - calculate 15% of 80 → 12.0
  - explain backpropagation → lab backprop (unchanged)

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| smoke accuracy | 2101/2101 | 2101/2101 (unchanged; no eval row added) |
| neural network explainer | research offline | lab three_neurons |
| coding/search/identity | green | green |

## GitHub push
Pending focused commit of lab_agent.py + thinking.py + agents.py + this note.

## Next priority remaining
All six priority items still satisfied. Optional: add 1–2 smoke eval rows for neural-network / transformer lab routing; keep smoke ≥ 2101/2101.
