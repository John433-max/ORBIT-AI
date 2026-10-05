# Cycle 456b — parentheses phrase + iso8601

Date: 2026-10-05

## Problem
"write a function that checks if parentheses are balanced" returned the NotImplemented draft. The live `valid_parentheses` matcher is in `code_synth_p84` (loaded before p1). Its regex required a space after `check`, so `checks if parentheses` missed. Unix timestamp → ISO-8601 had no template.

## Implementation
- `code_synth_p84.py` matcher also accepts "parentheses are balanced" and "checks if parentheses".
- `code_synth_p174.py` `unix_to_iso8601` (UTC, seconds) registered in `code_synth.py`.
- Smoke `code_1293`, `code_1294`.
- p173 `escape_html` kept importable (chr entity escapes).

## Tests
code_1285–code_1294 all ok in evals/results/latest.json (2026-10-05T23:15:43, 1336/1338). Remaining misses: lab_act (ReLU), code_1216 (luhn_valid).

## Probes
- add two numbers: verified `add`
- fusion search: live sources when web is up
- identity: ORBIT
