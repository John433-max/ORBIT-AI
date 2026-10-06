"""Cycle 466: numeric, sort, and geometry asks that still fell through.

Loaded first so bubble sort does not hit generic sort_list, and Kelvin
does not hit celsius_to_fahrenheit.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "celsius_to_kelvin",
            "def celsius_to_kelvin(c):\n"
            '    """ITS-90 offset: K = C + 273.15, rounded to 6 decimals."""\n'
            "    return round(float(c) + 273.15, 6)\n",
            lambda low: (
                ("celsius" in low or "centigrade" in low)
                and ("to kelvin" in low or "into kelvin" in low)
                and "to celsius" not in low
                and "to centigrade" not in low
                and "fahrenheit" not in low
            ),
            (
                ((0,), 273.15),
                ((-273.15,), 0.0),
                ((100,), 373.15),
            ),
        ),
        T(
            "bubble_sort",
            "def bubble_sort(values):\n"
            '    """Stable comparison sort. Returns a new list."""\n'
            "    arr = list(values)\n"
            "    n = len(arr)\n"
            "    for i in range(n):\n"
            "        for j in range(0, n - 1 - i):\n"
            "            if arr[j] > arr[j + 1]:\n"
            "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
            "    return arr\n",
            lambda low: "bubble" in low and "sort" in low,
            (
                (([3, 1, 2],), [1, 2, 3]),
                (([1],), [1]),
                (([],), []),
            ),
        ),
        T(
            "decimal_to_binary",
            "def decimal_to_binary(n):\n"
            '    """Integer to binary digits without a 0b prefix."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        return '-' + decimal_to_binary(-n)\n"
            "    return bin(n)[2:]\n",
            lambda low: (
                "binary" in low
                and ("decimal" in low or "integer" in low or "int " in low or "binary string" in low)
                and "to int" not in low
                and "to integer" not in low
                and "to decimal" not in low
                and "date" not in low
                and "add " not in low
                and "tree" not in low
                and "linked" not in low
                and "1290" not in low
            ),
            (
                ((0,), "0"),
                ((5,), "101"),
                ((13,), "1101"),
            ),
        ),
        T(
            "binary_to_decimal",
            "def binary_to_decimal(bits):\n"
            '    """Binary digit string to int. Leading minus is honored."""\n'
            "    s = str(bits).strip()\n"
            "    if s.startswith('-'):\n"
            "        return -binary_to_decimal(s[1:])\n"
            "    return int(s, 2)\n",
            lambda low: (
                "binary" in low
                and ("decimal" in low or "to int" in low or "to integer" in low)
                and "date" not in low
                and "add" not in low
                and "tree" not in low
                and "linked" not in low
                and "leetcode 1290" not in low
                and "1290" not in low
            ),
            (
                (("101",), 5),
                (("0",), 0),
                (("1101",), 13),
            ),
        ),
        T(
            "point_in_circle",
            "def point_in_circle(x, y, cx, cy, r):\n"
            '    """Inclusive disk test: (x-cx)^2 + (y-cy)^2 <= r^2."""\n'
            "    return (float(x) - float(cx)) ** 2 + (float(y) - float(cy)) ** 2 <= float(r) ** 2\n",
            lambda low: (
                "point" in low
                and "circle" in low
                and ("inside" in low or "in a circle" in low or "in the circle" in low or "within" in low)
                and "area" not in low
            ),
            (
                ((0, 0, 0, 0, 1), True),
                ((1, 0, 0, 0, 1), True),
                ((2, 0, 0, 0, 1), False),
            ),
        ),
        T(
            "matrix_trace",
            "def matrix_trace(matrix):\n"
            '    """Sum of the main diagonal. Ragged rows contribute when present."""\n'
            "    if not matrix:\n"
            "        return 0\n"
            "    total = 0\n"
            "    for i, row in enumerate(matrix):\n"
            "        if i < len(row):\n"
            "            total += row[i]\n"
            "    return total\n",
            lambda low: (
                "trace" in low
                and "matrix" in low
                and "traceback" not in low
                and "stack" not in low
            ),
            (
                (([[1, 2], [3, 4]],), 5),
                (([[7]],), 7),
                (([],), 0),
            ),
        ),
        T(
            "is_isogram",
            "def is_isogram(word):\n"
            '    """True when no letter repeats, ignoring case and non-letters."""\n'
            "    letters = [c.lower() for c in str(word) if c.isalpha()]\n"
            "    return len(letters) == len(set(letters))\n",
            lambda low: "isogram" in low,
            (
                (("isogram",), True),
                (("hello",), False),
                (("",), True),
            ),
        ),
    ]
