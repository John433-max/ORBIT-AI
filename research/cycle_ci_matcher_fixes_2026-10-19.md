# Improvement Cycle — CI matcher fixes (2026-10-19)

## Problem
Tests workflow consistently failed on `Unit tests (code_synth)` (runs 39195723997
on ce18004, 39196224805 on c8f7e76, and prior). Several template matchers were
too narrow or too broad, so `match_template` returned the wrong name or None.

## Root causes
| Ask | Wrong / None | Expected | Pack |
|---|---|---|---|
| tree diameter of an undirected tree | diameter_of_binary_tree | tree_diameter | p2 (optional binary) |
| construct … preorder and inorder traversal | inorder_traversal | build_tree | p3 |
| sums digits of a number | None | digit_sum | p230 |
| pairs adjacent elements | None | pairwise | p230 |
| splits pairs into two lists | None | split_pair_lists | p237 |
| removes duplicate characters preserving order | None | unique_chars | p161 |
| index of the maximum value | None | argmax_list | p407 |

## Changes
- `code_synth_p2.py`: diameter_of_binary_tree excludes "undirected"
- `code_synth_p3.py`: inorder_traversal excludes construct/build/preorder/postorder
- `code_synth_p230.py`: digit_sum accepts "sums digits"; pairwise accepts "pairs adjacent"
- `code_synth_p237.py`: split_pair_lists accepts "splits pairs"
- `code_synth_p161.py`: unique_chars accepts "duplicate characters preserving order"
- `code_synth_p407.py`: argmax_list accepts "index of the maximum value"

## Tests
- test_cycle525_take_drop_factors_letters_trim: pass
- test_p241_sudoku_and_matcher_fixes: pass
- test_add_multiply_subtract + thinking + code_route: 17 pass
- doctor: READY
- probes: coding → coding_agent + real `add`; search → research_agent; identity → main_chat_agent

## Next
Push focused packs to main so CI Tests goes green.

## GitHub
Pushed cc19d6d to main.
