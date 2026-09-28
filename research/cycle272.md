# Improvement Cycle 272

## Problem
GitHub coding-path packs lag local: remote code_synth.py only loaded through p12 and was missing p5/p8–p11/p13/p14 (and large p2/p3). Local smoke is 366/366 coding 326.

## Implementation
Keep GH agents.py slim (CI-safe). Push missing mid-size packs + loader p13/p14 entries.
Chunk 1: code_synth.py + p5 + p8 + p14 + this note.

## Tests
- doctor READY
- eval 366/366
- probes: coding verified add; research fusion news; identity ORBIT
- pytest synth+thinking+agents 104 passed

## Next
Push p9–p11, p13; then p2/p3 if size allows. fastapi extras. agents.py remains local-only.
