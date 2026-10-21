# ORBIT Improvement Run 31 — 2026-10-21

## Problem
Coding path missed "build a binary tree class" / "build a class for a binary tree".
Routed to the generic main-chat hedge ("I'm ORBIT… How can I help?") because:
- "build" was not a write-verb next to class/function
- the class alternation required a trailing space (`class `), so end-of-string "class" missed
No binary-tree class template existed, so a template-miss would still not return real code.

## Research
Internal routing in `_wants_code_written` / thinking `_is_code`. Prior cycles already
cover write/implement/how-to. "build" is a common natural-language write verb for
class asks. Existing packs cover stack/queue/graph/trie classes but not a plain
BinaryTree class.

## Finding
Add "build" to the write-verb proximity pattern and drop the trailing-space
requirement on `def`/`class` so "… class" at end of string matches. Guard the
broad identifier pattern (do not treat "build a house" / "build confidence" as code).
Inline a verified BinaryTree + TreeNode fallback for template-miss class asks,
excluding invert/diameter/serialize/etc. which already have function templates.

## Implementation
- agents.py: `_wants_code_written` build-verb + class boundary; `_explicit_write_ask` build;
  `_synthesize_python` BinaryTree class fallback
- thinking.py: `_is_code` / `_explicit_code_ask` build-verb + class boundary
- evals/datasets/smoke.jsonl: +3 coding rows (code_build_1..3)

## Tests
- Syntax OK
- Routing asserts 14/14
- BinaryTree fallback exec: insert 5,2,8,1 → inorder [1,2,5,8]
- Live probes: build binary tree class → Verified code; search → no live web;
  identity → ORBIT; build a house → non-code
- New smoke rows + anchors: 10/10

## Benchmark before → after
| Metric | Before | After |
|--------|--------|-------|
| "build a binary tree class" | hedge | class BinaryTree + Verified |
| smoke rows | 2095 | 2098 |
| coding rows | 2026 | 2029 |

## Result
Real improvement kept. Coding priority strengthened for "build … class" asks.

## Next
Full eval confirmation; GitHub parity (push agents.py + thinking.py + smoke);
model provider Ollama prefer (already implemented, offline here); serve deps docs.
