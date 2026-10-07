# Phrase matchers for swap_case / chunk_list / rotate_string

## Problem
Tests run 37575101627 failed on 37b077a:
- test_p202: "swaps the case of a string" matched None (regex required swaps?[- ]case)
- test_p204 / test_p205: "splits a list into chunks of size n" matched None (regex required "split " not "splits")

running_diff list-guard was correct: consecutive differences of a list stays running_diff; bare consecutive differences stays consecutive_diffs.

## Change
- code_synth_p199.py: swaps?(?: the)?[- ]case
- code_synth_p1.py, p1c.py, p84.py: splits? ... list ... chunks
- code_synth_p4.py: rotates? (?:a )?string, exclude list

## Tests
test_p202, test_p204, test_p205, test_p206 passed locally after the patch.
