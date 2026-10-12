# Improvement Cycle 584

## Problem
GitHub parity lagged local: agents.py lacked the "Verified." note for class/source-only templates, and packs p280/p281 were local-only.

## Research
Routing and code_synth already perfect (eval 1880/1880 = 1.0). Highest remaining priority is GitHub parity for tested local improvements.

## Sources
- Local /workspace/artifacts/orbit (source of truth)
- https://github.com/John433-max/ORBIT-AI (main)

## Finding
- doctor READY (Ollama optional offline; TinyLM fallback correct)
- smoke accuracy 1.0 (1880/1880)
- coding probe: real add() + Verified
- search probe: live fusion news with sources
- identity probe: "I'm ORBIT"
- agents.py local had +3 lines for verified note
- p280/p281 verified locally (segmented_sieve, z_function, scapegoat OK)

## Implementation
Pushed focused files only:
- agents.py (verified note)
- code_synth_p280.py
- code_synth_p281.py

## Files Changed
- agents.py
- code_synth_p280.py (new)
- code_synth_p281.py (new)

## Tests
- doctor: READY
- eval: 1880/1880 accuracy 1.0
- unit probes: coding/search/identity pass
- synthesize+verify on new templates: OK

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke accuracy | 1.0 (1880) | 1.0 (1880) | 0 |
| GitHub packs | ≤p279 | p280+p281 | +2 |
| agents.py verified note | missing | present | + |

## Result
Parity improved. Local remains source of truth. No regressions.

## Problems
None.

## Next Research Target
Continue GitHub parity for any remaining local-only packs or agent improvements; optional serve/deps documentation already present.
