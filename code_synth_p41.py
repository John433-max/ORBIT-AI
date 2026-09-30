"""Cycle 302: kth distinct / sort sentence / replace all digits / number of pairs / most words / words containing."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "kth_distinct",
            "def kth_distinct(arr, k):\n"
            '    """Kth distinct string in arr, or empty (LeetCode 2053)."""\n'
            "    from collections import Counter\n"
            "    freq = Counter(arr)\n"
            "    seen = 0\n"
            "    for w in arr:\n"
            "        if freq[w] == 1:\n"
            "            seen += 1\n"
            "            if seen == k:\n"
            "                return w\n"
            "    return ''\n",
            lambda low: bool(
                re.search(
                    r"\bkth[_ ]distinct\b|"
                    r"\bk-?th distinct string\b|"
                    r"\bkth distinct string\b",
                    low,
                )
            ),
            (
                ((["d", "b", "c", "b", "c", "a"], 2), "a"),
                ((["aaa", "aa", "a"], 1), "aaa"),
                ((["a", "b", "a"], 3), ""),
            ),
        ),
        T(
            "sort_sentence",
            "def sort_sentence(s):\n"
            '    """Reorder words by trailing index (LeetCode 1859)."""\n'
            "    parts = s.split()\n"
            "    out = [''] * len(parts)\n"
            "    for p in parts:\n"
            "        out[int(p[-1]) - 1] = p[:-1]\n"
            "    return ' '.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bsort[_ ]sentence\b|"
                    r"\bsorting the sentence\b|"
                    r"\breorder words by trailing\b",
                    low,
                )
            ),
            (
                (("is2 sentence4 This1 a3",), "This is a sentence"),
                (("Myself2 Me1 I4 and3",), "Me Myself and I"),
            ),
        ),
        T(
            "replace_all_digits",
            "def replace_all_digits(s):\n"
            '    """Replace digits with shifted previous letters (LeetCode 1844)."""\n'
            "    chars = list(s)\n"
            "    for i in range(1, len(chars), 2):\n"
            "        chars[i] = chr(ord(chars[i - 1]) + int(chars[i]))\n"
            "    return ''.join(chars)\n",
            lambda low: bool(
                re.search(
                    r"\breplace[_ ]all[_ ]digits\b|"
                    r"\breplace all digits with characters\b|"
                    r"\breplace digits with characters\b",
                    low,
                )
            ),
            (
                (("a1c1e1",), "abcdef"),
                (("a1b2c3d4e",), "abbdcfdhe"),
            ),
        ),
        T(
            "number_of_pairs",
            "def number_of_pairs(nums, target):\n"
            '    """Count pairs i<j with nums[i]+nums[j]<target (LeetCode 2824)."""\n'
            "    n = len(nums)\n"
            "    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] + nums[j] < target)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]pairs\b|"
                    r"\bcount pairs whose sum is less than\b|"
                    r"\bpairs whose sum is less than target\b",
                    low,
                )
            ),
            (
                (([-1, 1, 2, 3, 1], 2), 3),
                (([-6, 2, 5, -2, -7, -1, 3], -2), 10),
            ),
        ),
        T(
            "most_words_found",
            "def most_words_found(sentences):\n"
            '    """Max words in any sentence (LeetCode 2114)."""\n'
            "    return max((len(s.split()) for s in sentences), default=0)\n",
            lambda low: bool(
                re.search(
                    r"\bmost[_ ]words[_ ]found\b|"
                    r"\bmaximum number of words found in sentences\b",
                    low,
                )
            ),
            (
                ((["alice and bob love leetcode", "i think so too", "this is great thanks very much"],), 6),
                ((["please wait", "continue to fight", "continue to win"],), 3),
            ),
        ),
        T(
            "find_words_containing",
            "def find_words_containing(words, x):\n"
            '    """Indices of words containing character x (LeetCode 2942)."""\n'
            "    return [i for i, w in enumerate(words) if x in w]\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]words[_ ]containing\b|"
                    r"\bfind words containing character\b|"
                    r"\bwords containing character\b",
                    low,
                )
            ),
            (
                ((["leet", "code"], "e"), [0, 1]),
                ((["abc", "bcd", "aaaa", "cbc"], "a"), [0, 2]),
                ((["abc", "bcd", "aaaa", "cbc"], "z"), []),
            ),
        ),
    ]
