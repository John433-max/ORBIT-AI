# Improvement Cycle 313

## Problem
GitHub main lagged local code_synth_p51. Local eval 588/588 already includes code_543-548.

## Implementation
Shipped code_synth_p51.py (6 Easy templates). Did not overwrite slim GitHub agents.py.

## Tests
doctor READY; smoke 588/588; unit test_code_synth+thinking+provider_fallback 93 passed.
