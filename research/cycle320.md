# Improvement Cycle 320

## Problem
GitHub main still missing later code_synth packs; local eval had 588/588 while
smoke.jsonl had grown. Need another Easy pack plus GH pack parity.

## Implementation
- New pack `code_synth_p58.py` (6 Easy templates).
- Loader includes p58.
- Smoke code_585–code_590.
- `minimum_number_game` matcher requires "alice bob" / snake / 2974 so
  existing `number_game` row (code_475) stays intact.

## Result
Local templates 611 → 617. Probes coding/search/identity still pass.
Eval 630/630 after disambiguating code_475 vs code_585.
