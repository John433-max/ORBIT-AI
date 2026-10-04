"""Cycle 404: stubs and a wrong-template hit on array product.

Official examples:
- LeetCode 1464 Maximum Product of Two Elements:
  [3,4,5,2] -> 12; [1,5,4,5] -> 16; [3,7] -> 12.
- LeetCode 1094 Car Pooling:
  trips=[[2,1,5],[3,3,7]] capacity=4 -> False; capacity=5 -> True.
- LeetCode 763 Partition Labels:
  "ababcbacadefegdehijhklij" -> [9,7,8]; "eccbbbbdec" -> [10].
- LeetCode 6 Zigzag Conversion:
  "PAYPALISHIRING", 3 -> "PAHNAPLSIIGYIR"; 4 -> "PINALSIGYAHRPI"; 1 -> same.
- LeetCode 8 String to Integer (atoi):
  "42" -> 42; "   -42" -> -42; "4193 with words" -> 4193;
  "words and 987" -> 0; "-91283472332" -> -2147483648.
- LeetCode 451 Sort Characters By Frequency (stable: count desc, char asc):
  "tree" -> "eert"; "cccaaa" -> "aaaccc"; "Aabb" -> "bbAa".
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "max_product_two",
            "def max_product(nums):\n"
            '    """(max-1)*(second-1) in an array (LeetCode 1464)."""\n'
            "    first = second = 0\n"
            "    for raw in nums:\n"
            "        x = int(raw)\n"
            "        if x >= first:\n"
            "            second = first\n"
            "            first = x\n"
            "        elif x > second:\n"
            "            second = x\n"
            "    return (first - 1) * (second - 1)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1464\b", low)
                or "maximum product of two elements" in low
                or "max product of two elements" in low
            ),
            examples=(
                (([3, 4, 5, 2],), 12),
                (([1, 5, 4, 5],), 16),
                (([3, 7],), 12),
            ),
        ),
        T(
            "car_pooling",
            "def carPooling(trips, capacity):\n"
            '    """Whether all trips fit in capacity (LeetCode 1094)."""\n'
            "    diff = [0] * 1001\n"
            "    for num, start, end in trips:\n"
            "        diff[int(start)] += int(num)\n"
            "        diff[int(end)] -= int(num)\n"
            "    cur = 0\n"
            "    limit = int(capacity)\n"
            "    for delta in diff:\n"
            "        cur += delta\n"
            "        if cur > limit:\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1094\b", low)
                or "car pooling" in low
                or "car pool" in low
            ),
            examples=(
                (([[2, 1, 5], [3, 3, 7]], 4), False),
                (([[2, 1, 5], [3, 3, 7]], 5), True),
            ),
        ),
        T(
            "partition_labels",
            "def partitionLabels(s):\n"
            '    """Greedy partition sizes so each letter stays in one part (LeetCode 763)."""\n'
            "    last = {ch: i for i, ch in enumerate(s)}\n"
            "    out = []\n"
            "    start = end = 0\n"
            "    for i, ch in enumerate(s):\n"
            "        end = max(end, last[ch])\n"
            "        if i == end:\n"
            "            out.append(end - start + 1)\n"
            "            start = i + 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*763\b", low)
                or "partition labels" in low
            ),
            examples=(
                (("ababcbacadefegdehijhklij",), [9, 7, 8]),
                (("eccbbbbdec",), [10]),
            ),
        ),
        T(
            "zigzag_conversion",
            "def convert(s, numRows):\n"
            '    """Zigzag row read (LeetCode 6)."""\n'
            "    rows_n = int(numRows)\n"
            "    if rows_n <= 1 or rows_n >= len(s):\n"
            "        return s\n"
            "    rows = [''] * rows_n\n"
            "    r = 0\n"
            "    step = 1\n"
            "    for ch in s:\n"
            "        rows[r] += ch\n"
            "        if r == 0:\n"
            "            step = 1\n"
            "        elif r == rows_n - 1:\n"
            "            step = -1\n"
            "        r += step\n"
            "    return ''.join(rows)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*6\b", low)
                or "zigzag conversion" in low
                or "zigzag convert" in low
            ),
            examples=(
                (("PAYPALISHIRING", 3), "PAHNAPLSIIGYIR"),
                (("PAYPALISHIRING", 4), "PINALSIGYAHRPI"),
                (("PAYPALISHIRING", 1), "PAYPALISHIRING"),
            ),
        ),
        T(
            "my_atoi",
            "def myAtoi(s):\n"
            '    """Parse a 32-bit signed integer from a string (LeetCode 8)."""\n'
            "    i = 0\n"
            "    n = len(s)\n"
            "    while i < n and s[i] == ' ':\n"
            "        i += 1\n"
            "    sign = 1\n"
            "    if i < n and s[i] in '+-':\n"
            "        sign = -1 if s[i] == '-' else 1\n"
            "        i += 1\n"
            "    value = 0\n"
            "    while i < n and s[i].isdigit():\n"
            "        value = value * 10 + (ord(s[i]) - 48)\n"
            "        i += 1\n"
            "    value *= sign\n"
            "    lo, hi = -2147483648, 2147483647\n"
            "    if value < lo:\n"
            "        return lo\n"
            "    if value > hi:\n"
            "        return hi\n"
            "    return value\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*8\b", low)
                or "string to integer" in low
                or "atoi" in low
            ),
            examples=(
                (("42",), 42),
                (("   -42",), -42),
                (("4193 with words",), 4193),
                (("words and 987",), 0),
                (("-91283472332",), -2147483648),
            ),
        ),
        T(
            "frequency_sort",
            "def frequencySort(s):\n"
            '    """Sort chars by descending frequency, then char ascending (LeetCode 451)."""\n'
            "    from collections import Counter\n"
            "    counts = Counter(s)\n"
            "    chars = sorted(counts, key=lambda ch: (-counts[ch], ch))\n"
            "    return ''.join(ch * counts[ch] for ch in chars)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*451\b", low)
                or "sort characters by frequency" in low
                or "frequency sort" in low
            ),
            examples=(
                (("tree",), "eert"),
                (("cccaaa",), "aaaccc"),
                (("Aabb",), "bbAa"),
            ),
        ),
    ]
