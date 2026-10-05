# Cycle 457 — CI camel_to_snake phrase

Date: 2026-10-05

## Problem
Tests run 37387586267 failed on d11adb8 (3.11 and 3.12):

`test_p168_md5_jaccard_bytes_kebab_html_cosine`
`match_template("write a function that converts camel case to snake case")` was None.

## Cause
`code_synth_p160` registers `camel_to_snake` before `code_synth_p4`, and names are deduped. The p160 matcher required `camelcase to snake` or `snake_case`, so spaced "camel case to snake case" missed. p4's broader matcher never ran.

## Fix
p160 also matches `camel case to snake` / `camel-case to snake`, still excluding "to camel" and dict asks.

## Expected
That unit assertion resolves to `camel_to_snake`. Local doctor/eval not re-run (workspace sandbox limit).
