# ORBIT Improvement Run 34 — 2026-10-21

## Problem
"build a simple web scraper" fell through to the generic chat hedge
instead of CodeAgent. "create a class for a bank account" reached
CodeAgent but returned the synthesize-miss message.

## Cause
`_wants_code_written` / `_is_code` required a noun from
function|class|script|program|module|code. "scraper" / "tool" /
"calculator" were missing, so "build a simple web scraper" never
routed. Class asks with no template had no skeleton fallback.

## Change
- Expand the write-verb noun list with scraper|parser|tool|utility|
  crawler|calculator in agents.py and thinking.py.
- Generic class skeleton in `_synthesize_python` when a class ask
  misses every template (BankAccount for "bank account").
- Unit: test_build_scraper_and_class_return_real_code.

## Result
- build a simple web scraper → coding_agent, def scrape_text, Verified.
- create a class for a bank account → coding_agent, class BankAccount.
- write about fusion energy stays chat.
- search / identity probes unchanged.
- Related unit tests: 7/7 pass.
