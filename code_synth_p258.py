"""Cycle 561: SkipList and BloomFilter class asks that returned NotImplemented drafts.

Educational self-contained demos so synthesize_and_verify can self-check.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "skip_list_class",
            "def skip_list_demo(values, query):\n"
            '    """Insert values into a deterministic SkipList then search."""\n'
            "    sl = SkipList()\n"
            "    for value in values:\n"
            "        sl.insert(value)\n"
            "    return sl.search(query)\n"
            "\n"
            "\n"
            "class _SLNode:\n"
            "    def __init__(self, value, level):\n"
            "        self.value = value\n"
            "        self.forward = [None] * (level + 1)\n"
            "\n"
            "\n"
            "class SkipList:\n"
            '    """Deterministic skip list (level from value parity)."""\n'
            "\n"
            "    def __init__(self, max_level=4):\n"
            "        self.max_level = max_level\n"
            "        self.level = 0\n"
            "        self.head = _SLNode(None, max_level)\n"
            "\n"
            "    def _height(self, value):\n"
            "        h = 0\n"
            "        x = abs(int(value)) if isinstance(value, int) else len(str(value))\n"
            "        while x & 1 and h < self.max_level:\n"
            "            h += 1\n"
            "            x >>= 1\n"
            "        return h\n"
            "\n"
            "    def insert(self, value):\n"
            "        update = [None] * (self.max_level + 1)\n"
            "        cur = self.head\n"
            "        for i in range(self.level, -1, -1):\n"
            "            while cur.forward[i] is not None and cur.forward[i].value < value:\n"
            "                cur = cur.forward[i]\n"
            "            update[i] = cur\n"
            "        height = self._height(value)\n"
            "        if height > self.level:\n"
            "            for i in range(self.level + 1, height + 1):\n"
            "                update[i] = self.head\n"
            "            self.level = height\n"
            "        node = _SLNode(value, height)\n"
            "        for i in range(height + 1):\n"
            "            node.forward[i] = update[i].forward[i]\n"
            "            update[i].forward[i] = node\n"
            "\n"
            "    def search(self, value):\n"
            "        cur = self.head\n"
            "        for i in range(self.level, -1, -1):\n"
            "            while cur.forward[i] is not None and cur.forward[i].value < value:\n"
            "                cur = cur.forward[i]\n"
            "        cur = cur.forward[0]\n"
            "        return cur is not None and cur.value == value\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? skip[- ]?list\b|"
                    r"\bskip[- ]?list class\b|"
                    r"\bclass for(?: a| the)? skip[- ]?list\b|"
                    r"\bimplements? a skip[- ]?list\b",
                    low,
                )
            ),
            examples=(
                (([1, 2, 3], 2), True),
                (([1, 2, 3], 9), False),
                (([], 1), False),
            ),
        ),
        T(
            "bloom_filter_class",
            "def bloom_filter_demo(items, query):\n"
            '    """Add items to a Bloom filter then test membership."""\n'
            "    bf = BloomFilter(bits=64, hashes=2)\n"
            "    for item in items:\n"
            "        bf.add(item)\n"
            "    return bf.might_contain(query)\n"
            "\n"
            "\n"
            "class BloomFilter:\n"
            '    """Tiny educational Bloom filter (bytearray + two hashes)."""\n'
            "\n"
            "    def __init__(self, bits=64, hashes=2):\n"
            "        self.bits = bits\n"
            "        self.hashes = hashes\n"
            "        self.table = bytearray(bits)\n"
            "\n"
            "    def _positions(self, item):\n"
            "        text = str(item)\n"
            "        h1 = hash(text) % self.bits\n"
            "        h2 = hash(text + \"#\") % self.bits\n"
            "        if h2 == 0:\n"
            "            h2 = 1\n"
            "        return [(h1 + i * h2) % self.bits for i in range(self.hashes)]\n"
            "\n"
            "    def add(self, item):\n"
            "        for pos in self._positions(item):\n"
            "            self.table[pos] = 1\n"
            "\n"
            "    def might_contain(self, item):\n"
            "        return all(self.table[pos] == 1 for pos in self._positions(item))\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? bloom[- ]?filter\b|"
                    r"\bbloom[- ]?filter class\b|"
                    r"\bclass for(?: a| the)? bloom[- ]?filter\b|"
                    r"\bimplements? a bloom[- ]?filter\b",
                    low,
                )
            )
            and "count" not in low,
            examples=(
                ((["apple", "banana"], "apple"), True),
                ((["apple", "banana"], "cherry"), False),
                (([], "x"), False),
            ),
        ),
    ]
