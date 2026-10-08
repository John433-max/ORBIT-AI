"""Cycle 510: unmatched write-a-function asks.

Narrow matchers so sum_list, is_palindrome, is_even, and square-sum
templates keep their existing prompts.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "all_positive",
            "def all_positive(nums):\n"
            '    """Return True if every number is strictly positive."""\n'
            "    vals = list(nums)\n"
            "    return bool(vals) and all(x > 0 for x in vals)\n",
            lambda low: (
                "positive" in low
                and ("every" in low or "all" in low)
                and ("element" in low or "number" in low or "list" in low)
                and "largest" not in low
                and "negative" not in low
                and "odd" not in low
            ),
            (
                (([1, 2, 3],), True),
                (([1, 0, 2],), False),
                (([-1, 2],), False),
                (([],), False),
            ),
        ),
        T(
            "list_span",
            "def list_span(nums):\n"
            '    """Return max(nums) - min(nums); 0 for an empty list."""\n'
            "    vals = list(nums)\n"
            "    if not vals:\n"
            "        return 0\n"
            "    return max(vals) - min(vals)\n",
            lambda low: (
                (
                    "span" in low
                    or "max minus min" in low
                    or "max - min" in low
                    or "statistical range" in low
                    or ("difference" in low and "max" in low and "min" in low)
                    or ("max and min" in low and "difference" in low)
                )
                and "window" not in low
                and "subarray" not in low
                and "interquartile" not in low
                and "bst" not in low
                and "query" not in low
                and "cidr" not in low
            ),
            (
                (([1, 5, 3],), 4),
                (([7],), 0),
                (([],), 0),
            ),
        ),
        T(
            "odd_index_elements",
            "def odd_index_elements(nums):\n"
            '    """Return elements at odd indices (1, 3, ...)."""\n'
            "    return [x for i, x in enumerate(nums) if i % 2 == 1]\n",
            lambda low: (
                "odd" in low
                and ("index" in low or "indices" in low)
                and "even" not in low
                and "number" not in low
            ),
            (
                (([10, 20, 30, 40],), [20, 40]),
                (([1],), []),
                (([],), []),
            ),
        ),
        T(
            "list_is_palindrome",
            "def list_is_palindrome(nums):\n"
            '    """Return True if the list equals its reverse."""\n'
            "    vals = list(nums)\n"
            "    return vals == vals[::-1]\n",
            lambda low: (
                "palindrome" in low
                and "list" in low
                and "string" not in low
                and "linked" not in low
                and "phrase" not in low
            ),
            (
                (([1, 2, 1],), True),
                (([1, 2, 3],), False),
                (([],), True),
            ),
        ),
        T(
            "cube_elements",
            "def cube_elements(nums):\n"
            '    """Return each element cubed."""\n'
            "    return [x * x * x for x in nums]\n",
            lambda low: (
                ("cube" in low or "cubes" in low)
                and ("element" in low or "list" in low or "every" in low)
                and "sum" not in low
                and "square" not in low
            ),
            (
                (([1, 2, 3],), [1, 8, 27]),
                (([-2],), [-8]),
                (([],), []),
            ),
        ),
        T(
            "last_word",
            "def last_word(s):\n"
            '    """Return the last whitespace-separated word, or empty string."""\n'
            "    words = str(s).split()\n"
            "    return words[-1] if words else \"\"\n",
            lambda low: (
                "last word" in low
                and "longest" not in low
                and "shortest" not in low
                and "first word" not in low
            ),
            (
                (("hello world",), "world"),
                (("only",), "only"),
                (("  a   b  ",), "b"),
                (("",), ""),
            ),
        ),
    ]
