"""Cycle 509: unmatched write-a-function asks.

Narrow matchers so sum_list, count_words, remove_vowels, and title-case
templates keep their existing prompts.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_capitals",
            "def count_capitals(s):\n"
            '    """Count ASCII uppercase letters in a string."""\n'
            "    return sum(1 for ch in str(s) if 'A' <= ch <= 'Z')\n",
            lambda low: (
                ("capital" in low or "uppercase" in low)
                and ("letter" in low or "character" in low)
                and "grade" not in low
                and "camel" not in low
                and "title" not in low
            ),
            (
                (("AbC",), 2),
                (("hello",), 0),
                (("A1B",), 2),
            ),
        ),
        T(
            "count_lowercase",
            "def count_lowercase(s):\n"
            '    """Count ASCII lowercase letters in a string."""\n'
            "    return sum(1 for ch in str(s) if 'a' <= ch <= 'z')\n",
            lambda low: (
                ("lowercase" in low or "lower-case" in low or "lower case" in low)
                and ("letter" in low or "character" in low)
            ),
            (
                (("AbC",), 1),
                (("HELLO",), 0),
                (("a1b",), 2),
            ),
        ),
        T(
            "first_repeated_char",
            "def first_repeated_char(s):\n"
            '    """Return the first character that appears twice, else None."""\n'
            "    seen = set()\n"
            "    for ch in str(s):\n"
            "        if ch in seen:\n"
            "            return ch\n"
            "        seen.add(ch)\n"
            "    return None\n",
            lambda low: (
                "first" in low
                and "repeat" in low
                and ("character" in low or "char" in low)
                and "drop" not in low
                and "remove" not in low
                and "consecutive" not in low
            ),
            (
                (("abca",), "a"),
                (("abc",), None),
                (("aab",), "a"),
            ),
        ),
        T(
            "average_word_length",
            "def average_word_length(s):\n"
            '    """Mean length of whitespace-separated words; 0.0 if empty."""\n'
            "    words = str(s).split()\n"
            "    if not words:\n"
            "        return 0.0\n"
            "    return sum(len(w) for w in words) / len(words)\n",
            lambda low: (
                "average" in low
                and "word" in low
                and "length" in low
                and "each" not in low
                and "count" not in low
            ),
            (
                (("a bb",), 1.5),
                (("hi",), 2.0),
                (("",), 0.0),
            ),
        ),
        T(
            "count_spaces",
            "def count_spaces(s):\n"
            '    """Count space characters in a string."""\n'
            "    return str(s).count(' ')\n",
            lambda low: (
                "space" in low
                and ("count" in low or "number" in low)
                and "word" not in low
                and "namespace" not in low
            ),
            (
                (("a b c",), 2),
                (("abc",), 0),
                (("  x",), 2),
            ),
        ),
        T(
            "double_elements",
            "def double_elements(nums):\n"
            '    """Return a new list with every element doubled."""\n'
            "    return [2 * x for x in nums]\n",
            lambda low: (
                "double" in low
                and ("element" in low or "each" in low)
                and ("list" in low or "array" in low)
                and "matrix" not in low
            ),
            (
                (([1, 2, 3],), [2, 4, 6]),
                (([],), []),
                (((-1, 4),), [-2, 8]),
            ),
        ),
    ]
