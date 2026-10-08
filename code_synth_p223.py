"""Cycle 507: unmatched write-a-function asks.

Wrong-template steals (sum of squares, cartesian product, vowels and
consonants, word-length counts) and NotImplemented drafts (prefixes,
consecutive duplicates). Matchers stay narrow so sum_list, list_product,
count_vowels, and count_words keep their existing prompts.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "sum_of_squares",
            "def sum_of_squares(nums):\n"
            '    """Return the sum of squares of numeric items."""\n'
            "    total = 0\n"
            "    for x in nums:\n"
            "        total += x * x\n"
            "    return total\n",
            lambda low: (
                "square" in low
                and ("sum" in low or "squares" in low)
                and "magic" not in low
                and "perfect" not in low
                and "difference" not in low
            ),
            (
                (([1, 2, 3],), 14),
                (([],), 0),
                (([-2],), 4),
            ),
        ),
        T(
            "cartesian_product",
            "def cartesian_product(a, b):\n"
            '    """All pairs (x, y) with x from a and y from b."""\n'
            "    return [(x, y) for x in a for y in b]\n",
            lambda low: "cartesian" in low and "product" in low,
            (
                (([1, 2], ["a"]), [(1, "a"), (2, "a")]),
                (([], [1]), []),
            ),
        ),
        T(
            "count_vowels_consonants",
            "def count_vowels_consonants(s):\n"
            '    """Return (vowel_count, consonant_count) for letters in s."""\n'
            "    vowels = 0\n"
            "    consonants = 0\n"
            "    for ch in str(s).lower():\n"
            "        if not ch.isalpha():\n"
            "            continue\n"
            "        if ch in 'aeiou':\n"
            "            vowels += 1\n"
            "        else:\n"
            "            consonants += 1\n"
            "    return vowels, consonants\n",
            lambda low: "vowel" in low and "consonant" in low,
            (
                (("Orbit",), (2, 3)),
                (("a1b",), (1, 1)),
            ),
        ),
        T(
            "word_length_counts",
            "def word_length_counts(s):\n"
            '    """Map each word length to how many words have that length."""\n'
            "    counts = {}\n"
            "    for word in str(s).split():\n"
            "        n = len(word)\n"
            "        counts[n] = counts.get(n, 0) + 1\n"
            "    return counts\n",
            lambda low: (
                "word" in low
                and "length" in low
                and "count" in low
                and "longest" not in low
            ),
            (
                (("hi there cat",), {2: 1, 5: 1, 3: 1}),
                (("  ",), {}),
            ),
        ),
        T(
            "string_prefixes",
            "def string_prefixes(s):\n"
            '    """Return every non-empty prefix of s, shortest first."""\n'
            "    text = str(s)\n"
            "    return [text[:i] for i in range(1, len(text) + 1)]\n",
            lambda low: (
                "prefix" in low
                and "string" in low
                and "common" not in low
                and "longest" not in low
                and "count" not in low
            ),
            (
                (("ab",), ["a", "ab"]),
                (("",), []),
            ),
        ),
        T(
            "remove_consecutive_duplicates",
            "def remove_consecutive_duplicates(items):\n"
            '    """Drop items equal to the previous item; keep first of each run."""\n'
            "    out = []\n"
            "    for x in items:\n"
            "        if not out or out[-1] != x:\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: (
                "consecutive" in low
                and "duplicate" in low
                and "from a list" not in low
                and "character" not in low
                and "string" not in low
            ),
            (
                (([1, 1, 2, 2, 1],), [1, 2, 1]),
                (([],), []),
            ),
        ),
    ]
