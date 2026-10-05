# Cycle 457 — CI camel/snake match

Date: 2026-10-05

## Problem
CI run 37387586444 (commit d11adb8) failed
`tests/unit/test_code_synth.py::test_p168_md5_jaccard_bytes_kebab_html_cosine`
at line 4018: `match_template("... camel case to snake case")` was None
(AttributeError on `.name`). Locally the same prompt hit broad `snake_case`
from p175 (`"snake case" in low`), so the assertion `== camel_to_snake` failed
the other way.

## Implementation
- p174 (loaded before p160) registers direction-specific `camel_to_snake` and
  `snake_to_camel`. First name wins, so the spaced phrases resolve even if a
  later pack's matcher is narrower.
- Local p175 `snake_case` ignores prompts that also say camel/kebab; `camel_case`
  ignores snake/kebab. p175 was not pushed (not on main; extra templates could
  shift other matches).

## Tests
- Direct call: p168 and p169 pass; verify_source ok for camel_to_snake,
  snake_to_camel, unix_to_iso8601, snake_case, camel_case.
- classify: add-two-numbers and balanced-parentheses -> code; fusion search ->
  search; "what is your name" -> chat.
- doctor: READY (PyYAML / fastapi / Ollama optional).
- latest.json smoke accuracy still 0.9985 (1338 rows, not re-run this cycle).

## GitHub
Push p174 + this note. https://github.com/John433-max/ORBIT-AI/actions/runs/37387586444
