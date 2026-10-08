"""Cycle 511: unmatched write-a-function asks.

Narrow matchers so last_word, is_even, double_elements, multiply,
and matrix count_negatives keep their existing prompts.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "first_word",
            "def first_word(s):\n"
            '    """Return the first whitespace-separated word, or empty string."""\n'
            "    words = str(s).split()\n"
            "    return words[0] if words else \"\"\n",
            lambda low: (
                "first word" in low
                and "last" not in low
                and "longest" not in low
            ),
            (
                (("hello world",), "hello"),
                (("only",), "only"),
                (("  a   b  ",), "a"),
                (("",), ""),
            ),
        ),
        T(
            "count_negative_values",
            "def count_negative_values(nums):\n"
            '    """Count strictly negative numbers in a flat sequence."""\n'
            "    return sum(1 for x in nums if x < 0)\n",
            lambda low: (
                "negative" in low
                and (
                    "how many" in low
                    or "counts negative" in low
                    or "count negative" in low
                    or "count of negative" in low
                )
                and "matrix" not in low
                and "grid" not in low
                and "sorted" not in low
                and "positive" not in low
                and "counting sort" not in low
            ),
            (
                (([1, -2, 0, -4],), 2),
                (([1, 2],), 0),
                (([],), 0),
            ),
        ),
        T(
            "double_odd_numbers",
            "def double_odd_numbers(nums):\n"
            '    """Return a new list with odd numbers doubled; evens unchanged."""\n'
            "    return [2 * x if x % 2 else x for x in nums]\n",
            lambda low: (
                "double" in low
                and "odd" in low
                and "index" not in low
                and "indices" not in low
            ),
            (
                (([1, 2, 3, 4],), [2, 2, 6, 4]),
                (([-3, 0],), [-6, 0]),
                (([],), []),
            ),
        ),
        T(
            "hyphen_between_chars",
            "def hyphen_between_chars(s):\n"
            '    """Insert a hyphen between every character."""\n'
            "    return \"-\".join(str(s))\n",
            lambda low: (
                ("hyphen" in low or "hyphens" in low)
                and ("character" in low or "between" in low)
                and "slug" not in low
                and "word" not in low
            ),
            (
                (("ab",), "a-b"),
                (("xyz",), "x-y-z"),
                (("",), ""),
            ),
        ),
        T(
            "product_of_evens",
            "def product_of_evens(nums):\n"
            '    """Return the product of even numbers; 1 if none are even."""\n'
            "    prod = 1\n"
            "    for x in nums:\n"
            "        if x % 2 == 0:\n"
            "            prod *= x\n"
            "    return prod\n",
            lambda low: (
                "product" in low
                and "even" in low
                and "difference" not in low
                and "except" not in low
                and "self" not in low
                and "odd" not in low
            ),
            (
                (([1, 2, 3, 4],), 8),
                (([1, 3],), 1),
                (([],), 1),
            ),
        ),
        T(
            "word_final_chars",
            "def word_final_chars(s):\n"
            '    """Return the last character of each whitespace-separated word."""\n'
            "    return \"\".join(w[-1] for w in str(s).split())\n",
            lambda low: (
                "last character" in low
                and ("each word" in low or "every word" in low or "of each" in low)
                and "first word" not in low
            ),
            (
                (("hello world",), "od"),
                (("a",), "a"),
                (("",), ""),
            ),
        ),
    ]
