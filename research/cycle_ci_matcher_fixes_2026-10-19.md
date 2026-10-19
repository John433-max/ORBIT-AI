# Improvement Cycle — CI matcher fixes (2026-10-19)

## Problem
Tests workflow run 39194733341 failed on `Unit tests (code_synth)` after
`fix(code_synth): restore p407 RLE decompress matcher` (1f3ed90).

Root cause: several template matchers were too broad or too narrow.

| Ask | Wrong / None | Expected |
|---|---|---|
| tree diameter of an undirected tree | diameter_of_binary_tree | tree_diameter |
| construct binary tree from preorder and inorder | inorder_traversal | build_tree |
| takes the last n elements | last_element | last_n |
| sums digits of a number | None | digit_sum |
| pairs adjacent elements | None | pairwise |
| counts lines in text | None | line_count |

## Changes (local + pushed)
- `code_synth_p2.py`: require `binary tree` in diameter_of_binary_tree; exclude undirected
- `code_synth_p3.py`: inorder_traversal excludes preorder/postorder/construct/build
- `code_synth_p4.py`: last_n does not claim drops (drop_last owns remove); keeps of-a-list path
- `code_synth_p209.py`: last_element excludes last-n (PUSHED 3d26981)
- `code_synth_p230.py`: digit_sum accepts sums digits; pairwise accepts pairs adjacent
- `code_synth_p234.py`: line_count accepts counts lines in text (PUSHED c8f7e76)

## Tests (local)
- test_p204, test_p209, test_cycle525/526/527, test_p241, test_p277: 7 passed
- Probes coding/search/identity: OK
- doctor: READY

## Remaining push
Full `code_synth_p2.py`, `code_synth_p3.py`, `code_synth_p230.py`, complete `code_synth_p4.py`
still need to land on main for full CI green.
