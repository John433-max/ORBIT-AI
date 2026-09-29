"""Cycle 303: similar-string pairs / special squares / max ascending / largest group / balanced split / defuse bomb."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_pairs_of_similar_strings",
            "def count_pairs_of_similar_strings(words):\n"
            '    """Pairs whose letter sets match (LeetCode 2506)."""\n'
            "    from collections import Counter\n"
            "    freq = Counter(frozenset(w) for w in words)\n"
            "    return sum(n * (n - 1) // 2 for n in freq.values())\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]pairs[_ ]of[_ ]similar[_ ]strings\b|"
                    r"\bpairs of similar strings\b|"
                    r"\bsimilar string pairs\b",
                    low,
                )
            ),
            (
                ((["aba", "aabb", "abcd", "bac", "aabc"],), 2),
                ((["aabb", "ab", "ba"],), 3),
                ((["nba", "cba", "dba"],), 0),
            ),
        ),
        T(
            "sum_of_squares_of_special",
            "def sum_of_squares_of_special(nums):\n"
            '    """Sum squares of special elements (LeetCode 2778)."""\n'
            "    n = len(nums)\n"
            "    return sum(nums[i] * nums[i] for i in range(n) if n % (i + 1) == 0)\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ]of[_ ]squares[_ ]of[_ ]special\b|"
                    r"\bsum of squares of special elements\b|"
                    r"\bspecial elements square sum\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4],), 21),
                (([2, 7, 1, 19, 18, 3],), 63),
            ),
        ),
        T(
            "max_ascending_subarray",
            "def max_ascending_subarray(nums):\n"
            '    """Max sum of an ascending subarray (LeetCode 1800)."""\n'
            "    best = cur = nums[0] if nums else 0\n"
            "    for i in range(1, len(nums)):\n"
            "        if nums[i] > nums[i - 1]:\n"
            "            cur += nums[i]\n"
            "        else:\n"
            "            cur = nums[i]\n"
            "        if cur > best:\n"
            "            best = cur\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmax[_ ]ascending[_ ]subarray\b|"
                    r"\bmaximum ascending subarray sum\b|"
                    r"\bascending subarray sum\b",
                    low,
                )
            ),
            (
                (([10, 20, 30, 5, 10, 50],), 65),
                (([10, 20, 30, 40, 50],), 150),
                (([12, 17, 15, 13, 10, 11, 12],), 33),
            ),
        ),
        T(
            "count_largest_group",
            "def count_largest_group(n):\n"
            '    """Count digit-sum groups of max size (LeetCode 1399)."""\n'
            "    from collections import Counter\n"
            "    def digit_sum(x):\n"
            "        s = 0\n"
            "        while x:\n"
            "            s += x % 10\n"
            "            x //= 10\n"
            "        return s\n"
            "    freq = Counter(digit_sum(i) for i in range(1, n + 1))\n"
            "    if not freq:\n"
            "        return 0\n"
            "    m = max(freq.values())\n"
            "    return sum(1 for v in freq.values() if v == m)\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]largest[_ ]group\b|"
                    r"\bcount largest group\b|"
                    r"\bdigit sum groups\b",
                    low,
                )
            ),
            (
                ((13,), 4),
                ((2,), 2),
            ),
        ),
        T(
            "balanced_string_split",
            "def balanced_string_split(s):\n"
            '    """Max balanced R/L splits (LeetCode 1221)."""\n'
            "    bal = cuts = 0\n"
            "    for ch in s:\n"
            "        bal += 1 if ch == 'R' else -1\n"
            "        if bal == 0:\n"
            "            cuts += 1\n"
            "    return cuts\n",
            lambda low: bool(
                re.search(
                    r"\bbalanced[_ ]string[_ ]split\b|"
                    r"\bsplit a string in balanced strings\b|"
                    r"\bbalanced strings split\b",
                    low,
                )
            ),
            (
                (("RLRRLLRLRL",), 4),
                (("RLRRRLLRLL",), 2),
                (("LLLLRRRR",), 1),
            ),
        ),
        T(
            "defuse_the_bomb",
            "def defuse_the_bomb(code, k):\n"
            '    """Circular window decrypt (LeetCode 1652)."""\n'
            "    n = len(code)\n"
            "    out = [0] * n\n"
            "    if k == 0:\n"
            "        return out\n"
            "    for i in range(n):\n"
            "        if k > 0:\n"
            "            out[i] = sum(code[(i + j) % n] for j in range(1, k + 1))\n"
            "        else:\n"
            "            out[i] = sum(code[(i + j) % n] for j in range(k, 0))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdefuse[_ ]the[_ ]bomb\b|"
                    r"\bdefuse the bomb\b|"
                    r"\bdecrypt circular code\b",
                    low,
                )
            ),
            (
                (([5, 7, 1, 4], 3), [12, 10, 16, 13]),
                (([1, 2, 3, 4], 0), [0, 0, 0, 0]),
                (([2, 4, 9, 3], -2), [12, 5, 6, 13]),
            ),
        ),
    ]
