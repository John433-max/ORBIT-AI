"""Cycle 515: odd-sum stolen by sum_list; odd product, list min, digit strip missed.

Elementwise abs/square were claimed by scalar absolute and sum_of_squares.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "sum_odds",
            "def sum_odds(nums):\n"
            '    """Return the sum of odd numbers; evens contribute 0."""\n'
            "    return sum(x for x in nums if x % 2 != 0)\n",
            lambda low: (
                "odd" in low
                and ("sum" in low or "total" in low)
                and "even" not in low
                and "product" not in low
                and "double" not in low
                and "count" not in low
                and "index" not in low
                and "indices" not in low
                and "average" not in low
                and "divisible" not in low
                and "quer" not in low
            ),
            (
                (([1, 2, 3, 4],), 4),
                (([2, 4, 6],), 0),
                (([],), 0),
            ),
        ),
        T(
            "product_of_odds",
            "def product_of_odds(nums):\n"
            '    """Return the product of odd numbers; 1 if none are odd."""\n'
            "    prod = 1\n"
            "    for x in nums:\n"
            "        if x % 2 != 0:\n"
            "            prod *= x\n"
            "    return prod\n",
            lambda low: (
                "product" in low
                and "odd" in low
                and "even" not in low
                and "difference" not in low
                and "except" not in low
                and "matrix" not in low
            ),
            (
                (([1, 2, 3, 4],), 3),
                (([2, 4],), 1),
                (([],), 1),
            ),
        ),
        T(
            "absolute_values",
            "def absolute_values(nums):\n"
            '    """Return the absolute value of each number."""\n'
            "    return [abs(x) for x in nums]\n",
            lambda low: (
                "absolute" in low
                and ("each" in low or "every" in low or "list" in low or "elements" in low)
                and "error" not in low
                and "deviation" not in low
                and "difference" not in low
                and "mean" not in low
            ),
            (
                (([-2, 0, 3],), [2, 0, 3]),
                (([],), []),
                (([-1],), [1]),
            ),
        ),
        T(
            "square_elements",
            "def square_elements(nums):\n"
            '    """Return each element squared."""\n'
            "    return [x * x for x in nums]\n",
            lambda low: (
                "square" in low
                and ("each" in low or "every" in low or "element" in low)
                and "sum" not in low
                and "perfect" not in low
                and "magic" not in low
                and "matrix" not in low
            ),
            (
                (([1, -2, 3],), [1, 4, 9]),
                (([],), []),
                (([0],), [0]),
            ),
        ),
        T(
            "min_of_list",
            "def min_of_list(nums):\n"
            '    """Return the minimum of a list, or None if empty."""\n'
            "    vals = list(nums)\n"
            "    if not vals:\n"
            "        return None\n"
            "    return min(vals)\n",
            lambda low: (
                ("minimum" in low or "smallest" in low or "min " in low or low.endswith(" min"))
                and ("list" in low or "array" in low)
                and "two" not in low
                and "subarray" not in low
                and "window" not in low
                and "stack" not in low
                and "depth" not in low
                and "path" not in low
                and "cost" not in low
                and "rotated" not in low
                and "difference" not in low
                and "index" not in low
                and "running" not in low
                and "cumulative" not in low
                and "prefix" not in low
                and "span" not in low
                and "minus" not in low
                and "max" not in low
                and "rolling" not in low
                and "moving" not in low
            ),
            (
                (([3, 1, 2],), 1),
                (([-5, -1],), -5),
                (([],), None),
            ),
        ),
        T(
            "remove_digits",
            "def remove_digits(s):\n"
            '    """Drop digit characters from a string."""\n'
            "    return ''.join(ch for ch in str(s) if not ch.isdigit())\n",
            lambda low: (
                "digit" in low
                and ("remove" in low or "strip" in low or "drop" in low)
                and "count" not in low
                and "sum" not in low
                and "add" not in low
                and "extract" not in low
                and "leading" not in low
            ),
            (
                (("a1b2",), "ab"),
                (("123",), ""),
                (("",), ""),
            ),
        ),
    ]
