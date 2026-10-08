"""Cycle 516: interleave, pairwise, digit sum, title-case, order-stable unique, swap case.

String interleave (DP) and digital-root add_digits must not claim these asks.
CI 37814609674: do not steal p160 title_case ('capitalizes each word') or
p161 interleave ('interleaves two lists').
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "interleave_lists",
            "def interleave_lists(a, b):\n"
            '    """Alternate items from two lists; leftover tail is appended."""\n'
            "    out = []\n"
            "    n = min(len(a), len(b))\n"
            "    for i in range(n):\n"
            "        out.append(a[i])\n"
            "        out.append(b[i])\n"
            "    out.extend(a[n:])\n"
            "    out.extend(b[n:])\n"
            "    return out\n",
            lambda low: (
                (
                    "interleave_lists" in low
                    or "interleave lists" in low
                    or "interleaves lists" in low
                )
                and "two lists" not in low
                and "string" not in low
                and "substring" not in low
            ),
            (
                (([1, 2], [3, 4]), [1, 3, 2, 4]),
                (([1], [2, 3]), [1, 2, 3]),
                (([], []), []),
            ),
        ),
        T(
            "pairwise",
            "def pairwise(nums):\n"
            '    """Return consecutive overlapping pairs."""\n'
            "    return [(nums[i], nums[i + 1]) for i in range(len(nums) - 1)]\n",
            lambda low: (
                "pairwise" in low
                or ("consecutive" in low and "pair" in low and "group" not in low)
            )
            and "sum" not in low
            and "difference" not in low
            and "duplicate" not in low,
            (
                (([1, 2, 3, 4],), [(1, 2), (2, 3), (3, 4)]),
                (([1],), []),
                (([],), []),
            ),
        ),
        T(
            "digit_sum",
            "def digit_sum(n):\n"
            '    """Return the sum of decimal digits (absolute value)."""\n'
            "    n = abs(int(n))\n"
            "    total = 0\n"
            "    while n:\n"
            "        total += n % 10\n"
            "        n //= 10\n"
            "    return total\n",
            lambda low: (
                (
                    "sum of digits" in low
                    or "sums the digits" in low
                    or "sum the digits" in low
                    or "digit sum" in low
                )
                and "product" not in low
                and "root" not in low
                and "string" not in low
                and "alternat" not in low
                and "leetcode" not in low
                and "base" not in low
                and "even" not in low
                and "count" not in low
                and "convert" not in low
                and "element" not in low
                and "index" not in low
                and "divisib" not in low
                and "four digit" not in low
                and "minimum" not in low
                and "replace" not in low
            ),
            (
                ((38,), 11),
                ((0,), 0),
                ((-19,), 10),
            ),
        ),
        T(
            "capitalize_words",
            "def capitalize_words(text):\n"
            '    """Title-case each whitespace-separated word."""\n'
            "    return \" \".join(w[:1].upper() + w[1:].lower() if w else w for w in text.split(\" \"))\n",
            lambda low: (
                (
                    "capitalize_words" in low
                    or "capitalize words" in low
                    or "capitalizes words" in low
                )
                and "each word" not in low
                and "every word" not in low
                and "detect" not in low
            ),
            (
                (("hello world",), "Hello World"),
                (("a",), "A"),
                (("  ",), "  "),
            ),
        ),
        T(
            "triangle_number",
            "def triangle_number(n):\n"
            '    """Return the nth triangular number n*(n+1)//2."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        raise ValueError(\"n must be non-negative\")\n"
            "    return n * (n + 1) // 2\n",
            lambda low: (
                "triangle_number" in low
                or "triangle number" in low
            )
            and "pascal" not in low
            and "area" not in low
            and "largest" not in low
            and "triangular sum" not in low,
            (
                ((5,), 15),
                ((1,), 1),
                ((0,), 0),
            ),
        ),
        T(
            "parse_csv_line",
            "def parse_csv_line(line):\n"
            '    """Split a simple comma-separated line; no quoted commas."""\n'
            "    if line == \"\":\n"
            "        return []\n"
            "    return line.split(\",\")\n",
            lambda low: (
                "csv" in low
                and ("line" in low or "split" in low or "parse" in low)
                and "quote" not in low
            ),
            (
                (("a,b,c",), ["a", "b", "c"]),
                (("",), []),
                (("only",), ["only"]),
            ),
        ),
    ]
