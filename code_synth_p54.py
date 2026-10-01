"""Cycle 316: common words once / subtract product-sum / most frequent even /
largest local 3x3 / equal char counts / maximum 69 number."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_common_words",
            "def count_common_words(words1, words2):\n"
            '    """Words that appear exactly once in each list (LeetCode 2085)."""\n'
            "    from collections import Counter\n"
            "    c1, c2 = Counter(words1), Counter(words2)\n"
            "    return sum(1 for w, n in c1.items() if n == 1 and c2.get(w) == 1)\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]common[_ ]words\b|"
                    r"\bcommon[_ ]words[_ ]with[_ ]one[_ ]occurrence\b|"
                    r"\bcount_common_words\b",
                    low,
                )
            ),
            (
                ((["leetcode", "is", "amazing", "as", "is"], ["amazing", "leetcode", "is"]), 2),
                ((["b", "bb", "bbb"], ["a", "aa", "aaa"]), 0),
                ((["a", "ab"], ["a", "a", "a", "ab"]), 1),
            ),
        ),
        T(
            "subtract_product_and_sum",
            "def subtract_product_and_sum(n):\n"
            '    """Digit product minus digit sum of n (LeetCode 1281)."""\n'
            "    p, s = 1, 0\n"
            "    while n:\n"
            "        d = n % 10\n"
            "        p *= d\n"
            "        s += d\n"
            "        n //= 10\n"
            "    return p - s\n",
            lambda low: bool(
                re.search(
                    r"\bsubtract[_ ](?:the[_ ])?product[_ ](?:and|minus)[_ ](?:the[_ ])?sum\b|"
                    r"\bsubtract_product_and_sum\b|"
                    r"\bproduct[_ ]and[_ ]sum[_ ]of[_ ]digits\b",
                    low,
                )
            ),
            (
                ((234,), 15),
                ((4421,), 21),
                ((10,), -1),
            ),
        ),
        T(
            "most_frequent_even",
            "def most_frequent_even(nums):\n"
            '    """Smallest even value with the highest frequency, else -1 (LeetCode 2404)."""\n'
            "    from collections import Counter\n"
            "    freq = Counter(x for x in nums if x % 2 == 0)\n"
            "    if not freq:\n"
            "        return -1\n"
            "    best_n, best_v = 0, 10**9\n"
            "    for v, n in freq.items():\n"
            "        if n > best_n or (n == best_n and v < best_v):\n"
            "            best_n, best_v = n, v\n"
            "    return best_v\n",
            lambda low: bool(
                re.search(
                    r"\bmost[_ ]frequent[_ ]even\b|"
                    r"\bmost_frequent_even\b",
                    low,
                )
            ),
            (
                (([0, 1, 2, 2, 4, 4, 1],), 2),
                (([4, 4, 4, 9, 2, 4],), 4),
                (([29, 47, 21, 41, 13, 37, 25, 7],), -1),
            ),
        ),
        T(
            "largest_local",
            "def largest_local(grid):\n"
            '    """Max of each 3x3 window in an n x n grid (LeetCode 2373)."""\n'
            "    n = len(grid)\n"
            "    out = [[0] * (n - 2) for _ in range(n - 2)]\n"
            "    for i in range(n - 2):\n"
            "        for j in range(n - 2):\n"
            "            m = 0\n"
            "            for r in range(i, i + 3):\n"
            "                for c in range(j, j + 3):\n"
            "                    if grid[r][c] > m:\n"
            "                        m = grid[r][c]\n"
            "            out[i][j] = m\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blargest[_ ]local(?:[_ ]values)?\b|"
                    r"\blargest_local\b",
                    low,
                )
            ),
            (
                (([[9, 9, 8, 1], [5, 6, 2, 6], [8, 2, 6, 4], [6, 2, 2, 2]],), [[9, 9], [8, 6]]),
                (([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 2, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],), [[2, 2, 2], [2, 2, 2], [2, 2, 2]]),
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[9]]),
            ),
        ),
        T(
            "are_occurrences_equal",
            "def are_occurrences_equal(s):\n"
            '    """True if every character in s has the same count (LeetCode 1941)."""\n'
            "    from collections import Counter\n"
            "    vals = list(Counter(s).values())\n"
            "    return all(v == vals[0] for v in vals)\n",
            lambda low: bool(
                re.search(
                    r"\bare[_ ]occurrences[_ ]equal\b|"
                    r"\bequal[_ ]number[_ ]of[_ ]occurrences\b|"
                    r"\bare_occurrences_equal\b",
                    low,
                )
            ),
            (
                (("abacbc",), True),
                (("aaabb",), False),
                (("zzzz",), True),
            ),
        ),
        T(
            "maximum_69_number",
            "def maximum_69_number(num):\n"
            '    """Largest number after changing at most one 6 to 9 (LeetCode 1323)."""\n'
            "    s = list(str(num))\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch == '6':\n"
            "            s[i] = '9'\n"
            "            break\n"
            "    return int(''.join(s))\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum[_ ]69[_ ]number\b|"
                    r"\bmaximum_69_number\b|"
                    r"\bmax(?:imum)?[_ ]69\b",
                    low,
                )
            ),
            (
                ((9669,), 9969),
                ((9996,), 9999),
                ((9999,), 9999),
            ),
        ),
    ]
