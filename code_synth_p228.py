"""Cycle 513: list mean and sum-of-evens were stolen by binary average / sum_list.

Max-min difference is handled by widening list_span in p226.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "mean_list",
            "def mean_list(nums):\n"
            '    """Return the arithmetic mean of a list, or 0.0 if empty."""\n'
            "    vals = list(nums)\n"
            "    if not vals:\n"
            "        return 0.0\n"
            "    return sum(vals) / len(vals)\n",
            lambda low: (
                ("average" in low or "mean" in low)
                and ("list" in low or "array" in low or "numbers in a list" in low)
                and "two" not in low
                and "moving" not in low
                and "subarray" not in low
                and "level" not in low
                and "salary" not in low
                and "word" not in low
                and "weighted" not in low
                and "distinct" not in low
                and "minimum average" not in low
                and "maximum average" not in low
                and "divisible" not in low
                and "query" not in low
                and "geometric" not in low
                and "harmonic" not in low
                and "absolute" not in low
                and "column" not in low
                and "matrix" not in low
                and "error" not in low
                and "deviation" not in low
            ),
            (
                (([1, 2, 3, 4],), 2.5),
                (([10],), 10.0),
                (([],), 0.0),
            ),
        ),
        T(
            "sum_evens",
            "def sum_evens(nums):\n"
            '    """Return the sum of even numbers; odds contribute 0."""\n'
            "    return sum(x for x in nums if x % 2 == 0)\n",
            lambda low: (
                "even" in low
                and ("sum" in low or "total" in low)
                and "quer" not in low
                and "after" not in low
                and "divisible" not in low
                and "average" not in low
                and "index" not in low
                and "indices" not in low
            ),
            (
                (([1, 2, 3, 4],), 6),
                (([1, 3, 5],), 0),
                (([],), 0),
            ),
        ),
    ]
