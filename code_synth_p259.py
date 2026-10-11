"""Cycle 562: SegmentTree and CircularBuffer class asks that returned NotImplemented drafts.

Educational self-contained demos so synthesize_and_verify can self-check.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "segment_tree_class",
            "def segment_tree_class_demo(nums, updates, queries):\n"
            '    """Build a SegmentTree, apply updates, then range-sum queries."""\n'
            "    st = SegmentTree(nums)\n"
            "    for idx, val in updates:\n"
            "        st.update(idx, val)\n"
            "    return [st.query(left, right) for left, right in queries]\n"
            "\n"
            "\n"
            "class SegmentTree:\n"
            '    """1-based range-sum segment tree over a mutable array."""\n'
            "\n"
            "    def __init__(self, nums):\n"
            "        self.n = len(nums)\n"
            "        self.tree = [0] * (4 * self.n if self.n else 1)\n"
            "        self.nums = list(nums)\n"
            "        if self.n:\n"
            "            self._build(1, 0, self.n - 1)\n"
            "\n"
            "    def _build(self, node, start, end):\n"
            "        if start == end:\n"
            "            self.tree[node] = self.nums[start]\n"
            "            return\n"
            "        mid = (start + end) // 2\n"
            "        self._build(2 * node, start, mid)\n"
            "        self._build(2 * node + 1, mid + 1, end)\n"
            "        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]\n"
            "\n"
            "    def update(self, idx, val):\n"
            "        if not (0 <= idx < self.n):\n"
            "            return\n"
            "        self.nums[idx] = val\n"
            "        self._update(1, 0, self.n - 1, idx, val)\n"
            "\n"
            "    def _update(self, node, start, end, idx, val):\n"
            "        if start == end:\n"
            "            self.tree[node] = val\n"
            "            return\n"
            "        mid = (start + end) // 2\n"
            "        if idx <= mid:\n"
            "            self._update(2 * node, start, mid, idx, val)\n"
            "        else:\n"
            "            self._update(2 * node + 1, mid + 1, end, idx, val)\n"
            "        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]\n"
            "\n"
            "    def query(self, left, right):\n"
            "        if self.n == 0 or left > right:\n"
            "            return 0\n"
            "        left = max(0, left)\n"
            "        right = min(self.n - 1, right)\n"
            "        return self._query(1, 0, self.n - 1, left, right)\n"
            "\n"
            "    def _query(self, node, start, end, left, right):\n"
            "        if right < start or end < left:\n"
            "            return 0\n"
            "        if left <= start and end <= right:\n"
            "            return self.tree[node]\n"
            "        mid = (start + end) // 2\n"
            "        return (\n"
            "            self._query(2 * node, start, mid, left, right)\n"
            "            + self._query(2 * node + 1, mid + 1, end, left, right)\n"
            "        )\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)?(?: class(?: that)?(?: for| that implements)?(?: a| the)?| )?segment[- ]?tree(?: class)?\b|"
                    r"\bsegment[- ]?tree class\b|"
                    r"\bclass for(?: a| the)? segment[- ]?tree\b|"
                    r"\bimplements? a segment[- ]?tree\b|"
                    r"\bSegmentTree class\b",
                    low,
                )
            )
            and "sum" not in low
            and "fenwick" not in low,
            (
                (([1, 2, 3, 4], [(1, 10)], [(0, 2)]), [14]),
                (([5, 1, 3], [], [(0, 2), (1, 1)]), [9, 1]),
            ),
        ),
        T(
            "circular_buffer_class",
            "def circular_buffer_class_demo(capacity, ops):\n"
            '    """Push and pop on a fixed-capacity CircularBuffer."""\n'
            "    buf = CircularBuffer(capacity)\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        if op[0] == 'push':\n"
            "            out.append(buf.push(op[1]))\n"
            "        else:\n"
            "            out.append(buf.pop())\n"
            "    return out\n"
            "\n"
            "\n"
            "class CircularBuffer:\n"
            '    """Fixed-capacity ring buffer (overwrites oldest on overflow)."""\n'
            "\n"
            "    def __init__(self, capacity):\n"
            "        self.capacity = max(1, int(capacity))\n"
            "        self.buf = [None] * self.capacity\n"
            "        self.head = 0\n"
            "        self.size = 0\n"
            "\n"
            "    def push(self, value):\n"
            "        if self.size == self.capacity:\n"
            "            self.buf[self.head] = value\n"
            "            self.head = (self.head + 1) % self.capacity\n"
            "        else:\n"
            "            idx = (self.head + self.size) % self.capacity\n"
            "            self.buf[idx] = value\n"
            "            self.size += 1\n"
            "        return True\n"
            "\n"
            "    def pop(self):\n"
            "        if self.size == 0:\n"
            "            return None\n"
            "        value = self.buf[self.head]\n"
            "        self.buf[self.head] = None\n"
            "        self.head = (self.head + 1) % self.capacity\n"
            "        self.size -= 1\n"
            "        return value\n"
            "\n"
            "    def peek(self):\n"
            "        if self.size == 0:\n"
            "            return None\n"
            "        return self.buf[self.head]\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)?(?: class(?: that)?(?: for| that implements)?(?: a| the)?| )?circular[- ]?buffer(?: class)?\b|"
                    r"\bcircular[- ]?buffer class\b|"
                    r"\bclass for(?: a| the)? circular[- ]?buffer\b|"
                    r"\bring[- ]?buffer class\b|"
                    r"\bclass for(?: a| the)? ring[- ]?buffer\b|"
                    r"\bCircularBuffer class\b|"
                    r"\bimplements? a (?:circular|ring)[- ]?buffer\b",
                    low,
                )
            )
            and "deque" not in low
            and "queue" not in low,
            (
                ((3, [("push", 1), ("push", 2), ("push", 3), ("push", 4), ("pop",)]), [True, True, True, True, 2]),
                ((2, [("push", "a"), ("pop",), ("pop",)]), [True, "a", None]),
            ),
        ),
    ]
