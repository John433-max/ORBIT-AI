"""Cycle 270: additional verified Python templates (pack 13)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "gcd_of_strings",
            "def gcd_of_strings(str1, str2):\n"
            '    """Largest string X that divides both str1 and str2."""\n'
            "    a, b = str(str1), str(str2)\n"
            "    if a + b != b + a:\n"
            "        return ''\n"
            "    def _gcd(x, y):\n"
            "        while y:\n"
            "            x, y = y, x % y\n"
            "        return x\n"
            "    return a[:_gcd(len(a), len(b))]\n",
            lambda low: bool(
                re.search(
                    r"\bgcd of strings?\b|"
                    r"\bgcd_of_strings\b|"
                    r"\bgreatest common divisor of (?:two )?strings\b|"
                    r"\bstring gcd\b",
                    low,
                )
            ),
            ((("ABCABC", "ABC"), "ABC"), (("ABABAB", "ABAB"), "AB"), (("LEET", "CODE"), "")),
        ),
        T(
            "unique_occurrences",
            "def unique_occurrences(arr):\n"
            '    """True if each value frequency is unique."""\n'
            "    from collections import Counter\n"
            "    freq = Counter(arr)\n"
            "    return len(freq) == len(set(freq.values()))\n",
            lambda low: bool(
                re.search(
                    r"\bunique (?:number of )?occurrences\b|"
                    r"\bunique_occurrences\b|"
                    r"\bunique frequencies\b|"
                    r"\boccurrences are unique\b",
                    low,
                )
            )
            and "count how many" not in low,
            (
                (([1, 2, 2, 1, 1, 3],), True),
                (([1, 2],), False),
                (([-3, 0, 1, -3, 1, 1, 1, -3, 10, 0],), True),
            ),
        ),
        T(
            "kids_with_candies",
            "def kids_with_candies(candies, extra_candies):\n"
            '    """True for each kid if candies[i]+extra is a max."""\n'
            "    extra = int(extra_candies)\n"
            "    vals = [int(x) for x in candies]\n"
            "    m = max(vals) if vals else 0\n"
            "    return [c + extra >= m for c in vals]\n",
            lambda low: bool(
                re.search(
                    r"\bkids with (?:the )?greatest number of candies\b|"
                    r"\bkids_with_candies\b|"
                    r"\bgreatest number of candies\b|"
                    r"\bkids with candies\b",
                    low,
                )
            ),
            (([[2, 3, 5, 1, 3], 3], [True, True, True, False, True]), ([[4, 2, 1, 1, 2], 1], [True, False, False, False, False])),
        ),
        T(
            "remove_outer_parentheses",
            "def remove_outer_parentheses(s):\n"
            '    """Strip the outermost layer of each primitive parentheses group."""\n'
            "    s = str(s)\n"
            "    out = []\n"
            "    depth = 0\n"
            "    for ch in s:\n"
            "        if ch == '(':\n"
            "            if depth:\n"
            "                out.append(ch)\n"
            "            depth += 1\n"
            "        elif ch == ')':\n"
            "            depth -= 1\n"
            "            if depth:\n"
            "                out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bremove outermost parentheses\b|"
                    r"\bremove_outer_parentheses\b|"
                    r"\bremove outer(?:most)? parens\b|"
                    r"\bstrip outermost parentheses\b",
                    low,
                )
            ),
            ((("(()())(())",), "()()()"), (("(()())(())(()(()))",), "()()()()(())"), (("()()",), "")),
        ),
        T(
            "num_good_pairs",
            "def num_good_pairs(nums):\n"
            '    """Count pairs i < j with nums[i] == nums[j]."""\n'
            "    from collections import Counter\n"
            "    c = Counter(int(x) for x in nums)\n"
            "    return sum(n * (n - 1) // 2 for n in c.values())\n",
            lambda low: bool(
                re.search(
                    r"\bnumber of good pairs\b|"
                    r"\bnum_good_pairs\b|"
                    r"\bgood pairs\b|"
                    r"\bcount good pairs\b",
                    low,
                )
            )
            and "triplet" not in low
            and "three" not in low,
            (
                (([1, 2, 3, 1, 1, 3],), 4),
                (([1, 1, 1, 1],), 6),
                (([1, 2, 3],), 0),
            ),
        ),
        T(
            "shuffle_array",
            "def shuffle_array(nums, n):\n"
            '    """Return [x1,y1,x2,y2,...] from [x1..xn,y1..yn]."""\n'
            "    n = int(n)\n"
            "    a = list(nums)\n"
            "    out = []\n"
            "    for i in range(n):\n"
            "        out.append(a[i])\n"
            "        out.append(a[i + n])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bshuffles? the array\b|"
                    r"\bshuffle_array\b|"
                    r"\bshuffle array\b|"
                    r"\binterleave two halves\b",
                    low,
                )
            )
            and "string" not in low
            and "parity" not in low,
            (([[2, 5, 1, 3, 4, 7], 3], [2, 3, 5, 4, 1, 7]), ([[1, 2, 3, 4, 4, 3, 2, 1], 4], [1, 4, 2, 3, 3, 2, 4, 1])),
        ),
    ]
