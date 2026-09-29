# Improvement Cycle 285

## Problem
GitHub `code_synth` loader listed p2/p3 but those packs were missing on main.
Local tree has 423 templates (p2=68, p3=135, p25=6). GH coding coverage lagged.

## Research
Smallest parity step that does not overwrite slim `agents.py` (CI history).

## Implementation
- Keep local `code_synth.py` loader including `code_synth_p25`.
- Publish `code_synth_p25.py` + loader to GitHub.
- Publish missing `code_synth_p2.py` / `code_synth_p3.py` when push size allows.

## Tests
- Local doctor READY
- smoke/eval 432/432 (100%)
- probes: coding_agent add(), research_agent fusion, identity ORBIT
- `python -m py_compile` p2/p3/p25/code_synth OK
- 423 templates load locally

## Next
Push remaining mid packs if this commit lands; then slim-parity agents.py only if CI stays green.
