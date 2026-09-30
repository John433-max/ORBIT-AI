# Improvement Cycle 324

## Problem
GitHub code_synth loader listed packs through p60; p61 and several earlier packs were local-only. Coding/search/identity probes already pass locally.

## Implementation
- Ship code_synth_p61.py (6 Easy templates).
- Local code_synth.py already imports p61 (missing packs skipped).
- Local smoke code_609-code_613 added for p61 (is_fascinating already code_608).
- Did not overwrite slim GitHub agents.py.

## Tests
- synthesize_and_verify True on 5 new prompts
- Orchestrator coding_agent + Verified on sampled p61 prompts
- doctor READY
