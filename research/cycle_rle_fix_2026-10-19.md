# Improvement Cycle — RLE decompress matcher (2026-10-19)

## Problem
Eval 2082/2083 (99.95%): code_323 "decompress run-length encoded list" returned
`run_length_encode` instead of `decompress_rl_elist` (reason: missing:def decompress_rl_elist).

## Root cause
`code_synth_p407.py` was truncated (SyntaxError: unclosed `T(`). Runtime used stale
`__pycache__/code_synth_p407*.pyc` whose `run_length_encode` matcher lacked the
`"decompress" not in low` guard, so it won first-match over `decompress_rl_elist`.

## Implementation
- Restored complete `code_synth_p407.py` (encode + decompress_rl_elist + argmax +
  slugify + is_ipv4 + collatz_steps + rot13).
- Encode matcher: require encode/rle AND exclude decompress/decode.
- Decompress matcher: decompress + (run-length|rle) or name.

## Tests
- match_template(decompress query) → decompress_rl_elist
- match_template(encode query) → run_length_encode
- chat probe returns def decompress_rl_elist + Verified
- eval one-row code_323 → 1/1 (100%)
- pytest -k decompress/run_length: 5 passed (1 unrelated tree_diameter fail)

## Benchmark
| Metric | Before | After |
| code_323 | fail (encode) | pass (decompress) |
| full eval | 2082/2083 | (not re-run full; targeted 1/1) |

## Next
- Unrelated: test_p277 tree_diameter vs diameter_of_binary_tree order
- GitHub parity for agents.py / full code_synth packs
- Optional: serve deps (fastapi/uvicorn warning only)
