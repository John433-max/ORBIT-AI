# CI fix: word_wrap generated source was a syntax error

## Problem
Tests run 37412776508 (and follow-ups through 93d3e2f) failed unit tests.
`code_synth_p171.word_wrap` is loaded before `code_synth_p165`, and its source
string used `"return '\n'.join(...)"`. Inside the pack's double-quoted literal
that `\n` is a real newline, so `verify_source` raised
`unterminated string literal` and `test_all_templates_verify` failed.

## Implementation
Escape the join separator as `'\\n'` so the generated function contains a
newline escape, matching the p165 greedy wrapper.

## Benchmark
- Before: 1301 templates, 1 bad (`word_wrap` syntax error).
- After: 1301 templates, 0 bad. `synthesize_and_verify("write a python function that word wraps text")` verified=True, checked=2.
- pytest `tests/unit/test_code_synth.py -k "word_wrap or p165 or p171 or all_templates_verify or harmonic"`: 4 passed.
