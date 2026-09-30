"""Cycle 312: all A's before B / capitalize title / groups of size k / even digit-sum / prefix count / min four-digit sum."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "check_string",
            "def check_string(s):\n"
            '    """True iff every A appears before every B (LeetCode 2124)."""\n'
            "    return 'ba' not in s\n",
            lambda low: bool(
                re.search(
                    r"\bcheck[_ ]if[_ ]all[_ ]a.?s?\b.{0,32}\bbefore\b.{0,24}\bb|"
                    r"\ball[_ ]a.?s[_ ]before[_ ]all[_ ]b|"
                    r"\bcheck_string\b",
                    low,
                )
            ),
            (
                (("aaabbb",), True),
                (("abab",), False),
                (("bbb",), True),
            ),
        ),
        T(
            "capitalize_title",
            "def capitalize_title(title):\n"
            '    """Capitalize words of length >2 else lower (LeetCode 2129)."""\n'
            "    out = []\n"
            "    for w in title.split(' '):\n"
            "        if len(w) <= 2:\n"
            "            out.append(w.lower())\n"
            "        else:\n"
            "            out.append(w[0].upper() + w[1:].lower())\n"
            "    return ' '.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bcapitalize[_ ]the[_ ]title\b|"
                    r"\bcapitalize_title\b",
                    low,
                )
            ),
            (
                (("capiTalIze tHe titLe",), "Capitalize The Title"),
                (("First leTTeR of EACH Word",), "First Letter of Each Word"),
                (("i lOve leetcode",), "i Love Leetcode"),
            ),
        ),
        T(
            "divide_string",
            "def divide_string(s, k, fill):\n"
            '    """Split s into groups of size k, pad last (LeetCode 2138)."""\n'
            "    groups = []\n"
            "    for i in range(0, len(s), k):\n"
            "        chunk = s[i:i + k]\n"
            "        if len(chunk) < k:\n"
            "            chunk = chunk + fill * (k - len(chunk))\n"
            "        groups.append(chunk)\n"
            "    return groups\n",
            lambda low: bool(
                re.search(
                    r"\bdivide[_ ]a[_ ]string[_ ]into[_ ]groups[_ ]of[_ ]size[_ ]k\b|"
                    r"\bdivide_string\b",
                    low,
                )
            ),
            (
                (("abcdefghi", 3, "x"), ["abc", "def", "ghi"]),
                (("abcdefghij", 3, "x"), ["abc", "def", "ghi", "jxx"]),
                (("a", 2, "x"), ["ax"]),
            ),
        ),
        T(
            "count_even",
            "def count_even(num):\n"
            '    """Count positives <= num whose digit sum is even (LeetCode 2180)."""\n'
            "    def even_sum(n):\n"
            "        s = 0\n"
            "        while n:\n"
            "            s += n % 10\n"
            "            n //= 10\n"
            "        return s % 2 == 0\n"
            "    return sum(1 for x in range(1, num + 1) if even_sum(x))\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]integers[_ ]with[_ ]even[_ ]digit[_ ]sum\b|"
                    r"\bcount_even\b",
                    low,
                )
            ),
            (
                ((4,), 2),
                ((30,), 14),
                ((1,), 0),
            ),
        ),
        T(
            "prefix_count",
            "def prefix_count(words, pref):\n"
            '    """Count words that start with pref (LeetCode 2185)."""\n'
            "    return sum(1 for w in words if w.startswith(pref))\n",
            lambda low: bool(
                re.search(
                    r"\bcounting[_ ]words[_ ]with[_ ]a[_ ]given[_ ]prefix\b|"
                    r"\bprefix_count\b",
                    low,
                )
            ),
            (
                ((["pay", "attention", "practice", "attend"], "at"), 2),
                ((["leetcode", "win", "loops", "success"], "code"), 0),
                ((["a", "ab"], "a"), 2),
            ),
        ),
        T(
            "minimum_sum",
            "def minimum_sum(num):\n"
            '    """Min sum of two 2-digit numbers from four digits (LeetCode 2160)."""\n'
            "    d = sorted(str(num))\n"
            "    return int(d[0] + d[2]) + int(d[1] + d[3])\n",
            lambda low: bool(
                re.search(
                    r"\bminimum[_ ]sum[_ ]of[_ ]four[_ ]digit[_ ]number\b|"
                    r"\bminimum_sum\b",
                    low,
                )
            ),
            (
                ((2932,), 52),
                ((4009,), 13),
                ((1111,), 22),
            ),
        ),
    ]
