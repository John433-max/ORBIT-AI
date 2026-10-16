# Improvement Cycle — CI OOM split for code_synth unit tests

## Problem
CI run 38948889191 (and follow-ups through d165fd2) failed on the Unit tests step.
Local reproduction with an origin/main sparse tree exited 137 (SIGKILL / OOM) while running
the full `tests/unit` suite including `test_code_synth.py` (~326 tests, ~2k templates).

Document ranking regressions from 4e8e216 were already fixed in d165fd2; remaining
red CI is consistent with runner memory pressure, not assertion failures on coding/search.

## Research
- GitHub-hosted runners ~7GB RAM.
- `code_synth.get_templates()` dynamically imports every `code_synth_p*.py` pack.
- GH has 328 packs / ~1959 templates; local full tree 358 packs / 2126 templates.
- Full `test_code_synth` alone takes ~6.5 min locally and holds all templates + verify state.

## Implementation
Split unit-test steps in both workflows:
1. Core: `pytest tests/unit --ignore=tests/unit/test_code_synth.py`
2. Code synth: `pytest tests/unit/test_code_synth.py --maxfail=5`

Separate processes so template load memory is not stacked on top of other unit suites.

## Files Changed
- .github/workflows/ci.yml
- .github/workflows/tests.yml
- research/cycle-ci-oom-split-2026-10-16.md

## Tests
- tests/unit excl. code_synth: 159 passed (local)
- tests/unit/test_code_synth.py: 326 passed in 388s (local)
- GH-sparse core unit files: 78 passed
- doctor: READY
- probes: coding → verified add; search → research_agent; identity → ORBIT
- smoke latest: 2065/2065 = 1.0

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| CI unit process | single (OOM risk) | split core + code_synth | lower peak RAM |
| smoke accuracy | 1.000 | 1.000 | — |
| coding probe | ok | ok | keep |

## Result
Keep. Push workflow split so main CI can complete without OOM on code_synth.

## Next Research Target
Confirm green CI after push; then GitHub parity for remaining local-only packs / full agents.py.
