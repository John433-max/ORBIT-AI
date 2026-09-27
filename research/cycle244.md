# Cycle 244 — code_synth pack split + GH note

Date: 2026-09-27

## Baseline
- doctor: READY (fastapi warning, Ollama optional)
- smoke: 216/216 coding 189
- probes: coding_agent verified add; research_agent fusion; identity ORBIT
- GH code_synth 18KB / ~32 templates vs local 204 templates

## Chosen priority
GitHub parity for coding templates. Single 232KB code_synth.py is an awkward single-file push.

## Implementation
Split catalog into code_synth_p1/p2/p3 (68 templates each).
code_synth.py lazy-loads packs via get_templates() to avoid import cycles.
Did not replace GitHub code_synth.py this commit (would drop templates until packs land).

## Tests
- test_code_synth + thinking + agents: 83 passed
- smoke 216/216 after split

## Next
Push p1+p2+p3 then slim code_synth.py; then full local agents.py with CI watch.
