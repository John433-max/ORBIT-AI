# Improvement Cycle 543

## Problem
"write code that reads a json file and returns the keys" routed to code but fell through to a draft stub (`def write_code_that_reads_a_json_file_and_re`, `Draft from:`).

## Research
Existing code_synth packs had no JSON object-key template. SMTP-style refusals are for outbound network; local JSON parse is in-scope.

## Finding
A small template that accepts a JSON object string or an existing file path, verified on two official-style examples, closes the miss without a network call.

## Implementation
- `code_synth_p240.py` `json_keys`
- loader lists `code_synth_p240` before p239
- smoke row `code_json_keys_1`
- unit `test_json_file_keys_phrase` (string examples + temp file)

## Benchmark
- before: draft stub, not Verified
- after: `synthesize_and_verify` verified=True checked=2; agent answer contains `def json_keys` and `Verified`; score_row ok

## Next
GitHub pack push; full smoke recount after the new row.
