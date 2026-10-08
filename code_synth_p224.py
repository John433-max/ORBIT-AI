"""Cycle 508: unmatched write-a-function asks.

Narrow matchers so sum_list, count_words, fizzbuzz, and collatz_steps
keep their existing prompts.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "nth_odd",
            "def nth_odd(n):\n"
            '    """Return the n-th odd positive integer (1-based)."""\n'
            "    n = int(n)\n"
            "    if n < 1:\n"
            "        raise ValueError('n must be >= 1')\n"
            "    return 2 * n - 1\n",
            lambda low: (
                "odd" in low
                and ("nth" in low or "n-th" in low or "n'th" in low)
                and "even" not in low
            ),
            (
                ((1,), 1),
                ((4,), 7),
                ((10,), 19),
            ),
        ),
        T(
            "collatz_next",
            "def collatz_next(n):\n"
            '    """One Collatz step: n/2 if even, else 3n+1."""\n'
            "    n = int(n)\n"
            "    if n % 2 == 0:\n"
            "        return n // 2\n"
            "    return 3 * n + 1\n",
            lambda low: "collatz" in low and ("next" in low or "step" in low) and "steps" not in low and "count" not in low,
            (
                ((6,), 3),
                ((7,), 22),
                ((1,), 4),
            ),
        ),
        T(
            "diagonal_sums",
            "def diagonal_sums(matrix):\n"
            '    """Return (main diagonal sum, anti-diagonal sum)."""\n'
            "    n = len(matrix)\n"
            "    main = 0\n"
            "    anti = 0\n"
            "    for i in range(n):\n"
            "        main += matrix[i][i]\n"
            "        anti += matrix[i][n - 1 - i]\n"
            "    return main, anti\n",
            lambda low: "diagonal" in low and "sum" in low and "difference" not in low,
            (
                (([[1, 2], [3, 4]],), (5, 5)),
                (([[1]],), (1, 1)),
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), (15, 15)),
            ),
        ),
        T(
            "index_of_all",
            "def index_of_all(items, value):\n"
            '    """Return every index where items[i] == value."""\n'
            "    return [i for i, x in enumerate(items) if x == value]\n",
            lambda low: (
                "index" in low
                and ("all" in low or "every" in low or "each" in low)
                and "of" in low
            ),
            (
                (([1, 2, 1, 3], 1), [0, 2]),
                ((["a", "b"], "z"), []),
                (([4, 4, 4], 4), [0, 1, 2]),
            ),
        ),
        T(
            "letter_grade",
            "def letter_grade(score):\n"
            '    """Map a 0-100 score to a letter grade."""\n'
            "    score = float(score)\n"
            "    if score >= 90:\n"
            "        return 'A'\n"
            "    if score >= 80:\n"
            "        return 'B'\n"
            "    if score >= 70:\n"
            "        return 'C'\n"
            "    if score >= 60:\n"
            "        return 'D'\n"
            "    return 'F'\n",
            lambda low: "letter" in low and "grade" in low and "point" not in low,
            (
                ((95,), "A"),
                ((80,), "B"),
                ((70,), "C"),
                ((60,), "D"),
                ((59,), "F"),
            ),
        ),
        T(
            "window_sums",
            "def window_sums(nums, k):\n"
            '    """Sums of every contiguous window of length k."""\n'
            "    k = int(k)\n"
            "    if k <= 0 or k > len(nums):\n"
            "        return []\n"
            "    out = []\n"
            "    total = sum(nums[:k])\n"
            "    out.append(total)\n"
            "    for i in range(k, len(nums)):\n"
            "        total += nums[i] - nums[i - k]\n"
            "        out.append(total)\n"
            "    return out\n",
            lambda low: (
                "window" in low
                and "sum" in low
                and "maximum" not in low
                and "max" not in low
                and "minimum" not in low
            ),
            (
                (([1, 2, 3, 4], 2), [3, 5, 7]),
                (([5], 1), [5]),
                (([1, 2], 3), []),
            ),
        ),
    ]
