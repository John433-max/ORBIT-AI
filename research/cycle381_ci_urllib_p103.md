# Improvement Cycle 381

## Problem
GitHub Tests/CI on 7943b8d failed (runs 37082005721 / 37082005711):
- test_p97 expected `def complete_day_pairs` but the template is `def count_complete_day_pairs` (LeetCode 3184).
- test_ollama_urllib_health_and_generate_without_httpx asserted transport `urllib` while CI installs httpx via requirements.txt, so health reported `httpx`.
Local pack code_synth_p103 (6 Easy templates) and smoke rows code_856–862 were not on main.

## Research
Ollama adapter already prefers httpx when installed and falls back to urllib (orbit/models/ollama.py). The failing test did not hide httpx, so it was not measuring the fallback. Needle mismatch was a test/template contract bug, not a routing failure.

## Implementation
- Align p97 needle with `count_complete_day_pairs`.
- Block httpx inside the urllib fallback test; production still prefers httpx when present.
- Publish code_synth_p103 + loader entry + smoke rows.

## Tests
Local: three targeted functions PASS (urllib isolation, p97, p103).
Prior smoke this run: 902/902 before the needle-only test edit (smoke rows already present locally).

## Result
Keep. Push to main.
