"""Cycle 522: elementwise product, whitespace strip, char separator, prefix, variance, even-index sum.

Matchers stay narrower than list product, pad, word prefix, and is_even.
CI 37814609674: list_variance must not steal p174 population_variance.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "hadamard_product",
            "def hadamard_product(a, b):\n"
            '    """Multiply corresponding elements; extra tail is dropped."""\n'
            "    n = min(len(a), len(b))\n"
            "    return [a[i] * b[i] for i in range(n)]\n",
            lambda low: (
                "corresponding" in low
                and ("element" in low or "pair" in low)
                and "matrix" not in low
            ),
            (
                (([1, 2, 3], [4, 5, 6]), [4, 10, 18]),
                (([2], [3, 9]), [6]),
                (([], [1]), []),
            ),
        ),
        T(
            "remove_whitespace",
            "def remove_whitespace(s):\n"
            '    """Drop spaces, tabs, and other whitespace."""\n'
            "    return ''.join(str(s).split())\n",
            lambda low: (
                ("whitespace" in low or "all spaces" in low or "every space" in low)
                and ("remove" in low or "strip" in low or "delete" in low)
                and "pad" not in low
                and "word" not in low
            ),
            (
                (("a b\tc",), "abc"),
                (("  x  ",), "x"),
                (("",), ""),
            ),
        ),
        T(
            "intersperse_chars",
            "def intersperse_chars(s, sep):\n"
            '    """Insert sep between characters."""\n'
            "    return str(sep).join(str(s))\n",
            lambda low: (
                "character" in low
                and ("separator" in low or "between" in low)
                and ("insert" in low or "separator" in low)
                and "word" not in low
                and "list" not in low
            ),
            (
                (("ab", "-"), "a-b"),
                (("x", ","), "x"),
                (("", "-"), ""),
            ),
        ),
        T(
            "first_n_chars",
            "def first_n_chars(s, n):\n"
            '    """Return the first n characters; n < 0 yields empty."""\n'
            "    return str(s)[: max(0, int(n))]\n",
            lambda low: (
                "first" in low
                and "character" in low
                and "word" not in low
                and "unique" not in low
                and "non" not in low
            ),
            (
                (("orbit", 3), "orb"),
                (("ab", 0), ""),
                (("ab", 9), "ab"),
            ),
        ),
        T(
            "list_variance",
            "def list_variance(nums):\n"
            '    """Population variance; empty list is 0.0."""\n'
            "    if not nums:\n"
            "        return 0.0\n"
            "    mean = sum(nums) / len(nums)\n"
            "    return sum((x - mean) ** 2 for x in nums) / len(nums)\n",
            lambda low: (
                "variance" in low
                and "list" in low
                and "population" not in low
                and "standard" not in low
                and "sample" not in low
            ),
            (
                (([1, 2, 3],), 2 / 3),
                (([4, 4],), 0.0),
                (([],), 0.0),
            ),
        ),
        T(
            "even_index_sum",
            "def even_index_sum(nums):\n"
            '    """Sum values at even indices (0, 2, 4, ...)."""\n'
            "    return sum(nums[i] for i in range(0, len(nums), 2))\n",
            lambda low: (
                "even" in low
                and ("index" in low or "indices" in low)
                and "sum" in low
                and "odd" not in low
                and "sort" not in low
            ),
            (
                (([1, 2, 3, 4],), 4),
                (([9],), 9),
                (([],), 0),
            ),
        ),
    ]
