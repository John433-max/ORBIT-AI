"""Cycle 276: additional verified Python templates (pack 18)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "uncommon_from_sentences",
            "def uncommon_from_sentences(s1, s2):\n"
            '    """Words that appear exactly once across two sentences."""\n'
            "    from collections import Counter\n"
            "    cnt = Counter((s1 or '').split()) + Counter((s2 or '').split())\n"
            "    return [w for w, c in cnt.items() if c == 1]\n",
            lambda low: bool(
                re.search(
                    r"\buncommon words?\s+from\s+two\s+sentences\b|"
                    r"\buncommon_from_sentences\b|"
                    r"\buncommon words? from sentences\b",
                    low,
                )
            ),
            (
                (["this apple is sweet", "this apple is sour"], ["sweet", "sour"]),
                (["apple apple", "banana"], ["banana"]),
            ),
        ),
        T(
            "buddy_strings",
            "def buddy_strings(s, goal):\n"
            '    """True if swapping two letters in s can make goal."""\n'
            "    s, goal = str(s), str(goal)\n"
            "    if len(s) != len(goal):\n"
            "        return False\n"
            "    if s == goal:\n"
            "        return len(set(s)) < len(s)\n"
            "    diffs = [(a, b) for a, b in zip(s, goal) if a != b]\n"
            "    return len(diffs) == 2 and diffs[0] == diffs[1][::-1]\n",
            lambda low: bool(
                re.search(
                    r"\bbuddy strings\b|"
                    r"\bbuddy_strings\b|"
                    r"\bswap two letters.{0,20}equal\b",
                    low,
                )
            ),
            ((("ab", "ba"), True), (("ab", "ab"), False), (("aa", "aa"), True)),
        ),
        T(
            "large_group_positions",
            "def large_group_positions(s):\n"
            '    """Inclusive index ranges of same-letter groups of length >= 3."""\n'
            "    s = str(s)\n"
            "    out = []\n"
            "    i, n = 0, len(s)\n"
            "    while i < n:\n"
            "        j = i\n"
            "        while j < n and s[j] == s[i]:\n"
            "            j += 1\n"
            "        if j - i >= 3:\n"
            "            out.append([i, j - 1])\n"
            "        i = j\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blarge group positions\b|"
                    r"\blarge_group_positions\b|"
                    r"\bpositions of large groups\b",
                    low,
                )
            ),
            ((("abbxxxxzzy",), [[3, 6]]), (("abc",), []), (("abcdddeeeeaabbbd",), [[3, 5], [6, 9], [12, 14]])),
        ),
        T(
            "find_error_nums",
            "def find_error_nums(nums):\n"
            '    """Return [duplicate, missing] in 1..n with one duplicate."""\n'
            "    a = [int(x) for x in nums]\n"
            "    n = len(a)\n"
            "    seen = [0] * (n + 1)\n"
            "    dup = 0\n"
            "    for v in a:\n"
            "        if seen[v]:\n"
            "            dup = v\n"
            "        seen[v] = 1\n"
            "    miss = next(i for i in range(1, n + 1) if not seen[i])\n"
            "    return [dup, miss]\n",
            lambda low: bool(
                re.search(
                    r"\bset mismatch\b|"
                    r"\bfind_error_nums\b|"
                    r"\berror nums\b|"
                    r"\bduplicate and missing\b|"
                    r"\bfind the (?:duplicate and missing|error numbers?)\b",
                    low,
                )
            )
            and "first missing" not in low
            and "kth missing" not in low,
            (([[1, 2, 2, 4],], [2, 3]), ([[1, 1],], [1, 2])),
        ),
        T(
            "has_alternating_bits",
            "def has_alternating_bits(n):\n"
            '    """True if binary representation of n has no two adjacent equal bits."""\n'
            "    n = int(n)\n"
            "    prev = n & 1\n"
            "    n >>= 1\n"
            "    while n:\n"
            "        bit = n & 1\n"
            "        if bit == prev:\n"
            "            return False\n"
            "        prev = bit\n"
            "        n >>= 1\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\balternating bits\b|"
                    r"\bhas_alternating_bits\b|"
                    r"\bbinary.{0,12}alternating\b",
                    low,
                )
            ),
            (((5,), True), ((7,), False), ((11,), False), ((10,), True)),
        ),
        T(
            "find_and_replace_pattern",
            "def find_and_replace_pattern(words, pattern):\n"
            '    """Words isomorphic to pattern (bijection of letters)."""\n'
            "    def sig(w):\n"
            "        m = {}\n"
            "        out = []\n"
            "        for ch in w:\n"
            "            if ch not in m:\n"
            "                m[ch] = len(m)\n"
            "            out.append(m[ch])\n"
            "        return tuple(out)\n"
            "    p = sig(pattern)\n"
            "    return [w for w in words if sig(w) == p]\n",
            lambda low: bool(
                re.search(
                    r"\bfind and replace pattern\b|"
                    r"\bfind_and_replace_pattern\b|"
                    r"\bwords matching pattern\b|"
                    r"\bisomorphic to pattern\b",
                    low,
                )
            )
            and "word pattern" not in low
            and "word_pattern" not in low,
            (([["abc", "deq", "mee", "aqq", "dkd", "ccc"], "abb"], ["mee", "aqq"]),),
        ),
    ]
