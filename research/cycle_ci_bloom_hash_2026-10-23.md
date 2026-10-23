# Cycle CI-bloom-hash [2026-10-23]

## Problem
CI run 39902661627 failed on Python 3.11 unit tests (code_synth):
- test_all_templates_verify
- test_p258_skiplist_bloomfilter

Failure: bloom_filter_class verification expected False for unseen item "cherry" but got True (false positive).

Root cause: template used Python's built-in hash(), which is randomized per process (PYTHONHASHSEED). With bits=64, occasional collisions made examples non-deterministic across CI runners.

## Fix
In code_synth_p258.py, replaced hash(text) with a simple deterministic polynomial hash:

h1 = sum(ord(c) * (i + 1) for i, c in enumerate(text)) % self.bits
h2 = sum(ord(c) * (i + 3) for i, c in enumerate(text + "#")) % self.bits

Examples now pass under any hash seed.

## Tests
- Local: test_p258_skiplist_bloomfilter passed
- synthesize_and_verify("implement a bloom filter class") verified=True under seeds 0,20,42,99
- Probes: coding returns real add() function; search honest no-live-web; identity "I'm ORBIT"

## GitHub
Pushed 7bf5100 to main.

## Next
Monitor next CI; continue priority queue (coding/search already healthy).
