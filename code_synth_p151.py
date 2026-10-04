"""Cycle 405: can-break, matrix rotation, valid words, good integer, partition string, min rounds.

Unmatched fallbacks on the local coding path (LeetCode 1433 / 1886 / 2047 / 2264 / 2405 / 2244).
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "check_if_can_break",
            "def check_if_can_break(s1, s2):\n"
            '    """True if either sorted string dominates the other (LeetCode 1433)."""\n'
            "    a, b = sorted(s1), sorted(s2)\n"
            "    return all(x >= y for x, y in zip(a, b)) or all(x <= y for x, y in zip(a, b))\n"
            "\n"
            "def checkIfCanBreak(s1, s2):\n"
            "    return check_if_can_break(s1, s2)\n",
            lambda low: bool(
                re.search(r"\bcan break another\b|\bleetcode 1433\b", low)
            ),
            (
                (("abc", "xya"), True),
                (("abe", "acd"), False),
                (("leetcodee", "interview"), True),
            ),
        ),
        T(
            "find_rotation",
            "def find_rotation(mat, target):\n"
            '    """True if target is mat rotated 0/90/180/270 degrees (LeetCode 1886)."""\n'
            "    def rot(g):\n"
            "        return [list(row) for row in zip(*g[::-1])]\n"
            "    cur = [list(row) for row in mat]\n"
            "    for _ in range(4):\n"
            "        if cur == target:\n"
            "            return True\n"
            "        cur = rot(cur)\n"
            "    return False\n"
            "\n"
            "def findRotation(mat, target):\n"
            "    return find_rotation(mat, target)\n",
            lambda low: bool(
                re.search(r"obtained by rotation|\bleetcode 1886\b", low)
            ),
            (
                (([[0, 1], [1, 0]], [[1, 0], [0, 1]]), True),
                (([[0, 1], [1, 1]], [[1, 0], [0, 1]]), False),
                (([[0, 0, 0], [0, 1, 0], [1, 1, 1]], [[1, 1, 1], [0, 1, 0], [0, 0, 0]]), True),
            ),
        ),
        T(
            "count_valid_words",
            "def count_valid_words(sentence):\n"
            '    """Count valid words: no digits, one hyphen, trailing punct (LeetCode 2047)."""\n'
            "    import re as _re\n"
            "    pat = _re.compile(r\"^[a-z]+(?:-[a-z]+)?[!.,]?$\")\n"
            "    return sum(1 for w in sentence.split() if pat.match(w))\n"
            "\n"
            "def countValidWords(sentence):\n"
            "    return count_valid_words(sentence)\n",
            lambda low: bool(
                re.search(r"\bvalid words\b|\bleetcode 2047\b", low)
            ),
            (
                (("cat and  dog",), 3),
                (("!this  1-s b8d!",), 0),
                (("alice and  bob are playing stone-game10",), 5),
            ),
        ),
        T(
            "largest_good_integer",
            "def largest_good_integer(num):\n"
            '    """Largest 3-same-digit substring, or empty (LeetCode 2264)."""\n'
            "    best = \"\"\n"
            "    for i in range(len(num) - 2):\n"
            "        chunk = num[i:i + 3]\n"
            "        if chunk[0] == chunk[1] == chunk[2] and chunk > best:\n"
            "            best = chunk\n"
            "    return best\n"
            "\n"
            "def largestGoodInteger(num):\n"
            "    return largest_good_integer(num)\n",
            lambda low: bool(
                re.search(r"3-same-digit|three same digit|\bleetcode 2264\b", low)
            ),
            (
                (("6777133339",), "777"),
                (("2300019",), "000"),
                (("42352338",), ""),
            ),
        ),
        T(
            "partition_string",
            "def partition_string(s):\n"
            '    """Min partitions so each part has unique chars (LeetCode 2405)."""\n'
            "    seen = set()\n"
            "    parts = 1\n"
            "    for ch in s:\n"
            "        if ch in seen:\n"
            "            parts += 1\n"
            "            seen = {ch}\n"
            "        else:\n"
            "            seen.add(ch)\n"
            "    return parts\n"
            "\n"
            "def partitionString(s):\n"
            "    return partition_string(s)\n",
            lambda low: bool(
                re.search(r"\boptimal partition of string\b|\bleetcode 2405\b", low)
            ),
            (
                (("abacaba",), 4),
                (("ssssss",), 6),
                (("abc",), 1),
            ),
        ),
        T(
            "minimum_rounds",
            "def minimum_rounds(tasks):\n"
            '    """Min rounds of 2 or 3 same-difficulty tasks, else -1 (LeetCode 2244)."""\n'
            "    from collections import Counter\n"
            "    rounds = 0\n"
            "    for freq in Counter(tasks).values():\n"
            "        if freq == 1:\n"
            "            return -1\n"
            "        rounds += (freq + 2) // 3\n"
            "    return rounds\n"
            "\n"
            "def minimumRounds(tasks):\n"
            "    return minimum_rounds(tasks)\n",
            lambda low: bool(
                re.search(r"\bminimum rounds\b|\bleetcode 2244\b", low)
            ),
            (
                (([2, 2, 3, 3, 2, 4, 4, 4, 4, 4],), 4),
                (([2, 3, 3],), -1),
                (([5, 5, 5, 5],), 2),
            ),
        ),
    ]
