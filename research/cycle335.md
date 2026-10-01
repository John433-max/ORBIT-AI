# Improvement Cycle 335 — GitHub pack parity p70–p71

Date: 2026-10-01

## Problem
Local coding path is green (713 smoke rows, 686 templates, probes pass).
GitHub main still stopped the code_synth loader at p69 and lacked p70/p71
modules, so CI/runtime on the public tree could not match local Easy coverage.

## Research
After coding/search/identity probes passed, GitHub pack parity is next.
Do not replace GH agents.py (15 KB CI surface) with local 85 KB file.

## Implementation
- code_synth.py loader includes code_synth_p70 / code_synth_p71
- code_synth_p70.py and code_synth_p71.py
- this note

## Tests
Local p70/p71 unit tests passed (2 passed / 6.20s). Probes unchanged.

## Next
Remaining missing GH packs (p2/p3, p28–p32, p44, p47, p49, p53–57, p59, p62, p64–66, p68).
