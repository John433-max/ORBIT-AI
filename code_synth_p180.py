"""Cycle 462: geometry, calendar, and text helpers that still fell through.

Loaded first so catalan / days-in-month / hashtag asks do not hit factorial,
leap-year, or generic string stubs.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "rotate_point",
            "def rotate_point(x, y, degrees):\n"
            '    """Rotate (x, y) around the origin by degrees, counterclockwise."""\n'
            "    import math\n"
            "    rad = math.radians(float(degrees))\n"
            "    c, s = math.cos(rad), math.sin(rad)\n"
            "    xr = float(x) * c - float(y) * s\n"
            "    yr = float(x) * s + float(y) * c\n"
            "    return (round(xr, 6), round(yr, 6))\n",
            lambda low: bool(
                re.search(r"rotat\w*\s+(a\s+)?point", low)
                and "origin" in low
            ),
            (
                ((1, 0, 90), (0.0, 1.0)),
                ((1, 0, 180), (-1.0, 0.0)),
                ((0, 1, -90), (1.0, 0.0)),
            ),
        ),
        T(
            "cartesian_to_polar",
            "def cartesian_to_polar(x, y):\n"
            '    """Return (radius, degrees) for a cartesian point."""\n'
            "    import math\n"
            "    r = math.hypot(float(x), float(y))\n"
            "    deg = math.degrees(math.atan2(float(y), float(x)))\n"
            "    return (round(r, 6), round(deg, 6))\n",
            lambda low: "cartesian" in low and "polar" in low,
            (
                ((3, 4), (5.0, 53.130102)),
                ((1, 0), (1.0, 0.0)),
                ((0, -2), (2.0, -90.0)),
            ),
        ),
        T(
            "extract_hashtags",
            "def extract_hashtags(text):\n"
            '    """Return hashtag bodies in order, without the leading #."""\n'
            "    import re\n"
            "    return re.findall(r'(?<!\\w)#([A-Za-z0-9_]+)', str(text))\n",
            lambda low: "hashtag" in low,
            (
                (("love #Orbit and #AI",), ["Orbit", "AI"]),
                (("#a #a #b",), ["a", "a", "b"]),
                (("no tags",), []),
            ),
        ),
        T(
            "mask_last4",
            "def mask_last4(value):\n"
            '    """Mask all but the last four characters."""\n'
            "    s = str(value)\n"
            "    if len(s) <= 4:\n"
            "        return s\n"
            "    return ('*' * (len(s) - 4)) + s[-4:]\n",
            lambda low: "mask" in low and "last four" in low,
            (
                (("4111111111111111",), "************1111"),
                (("abcd",), "abcd"),
                (("secret99",), "****et99"),
            ),
        ),
        T(
            "days_in_month",
            "def days_in_month(year, month):\n"
            '    """Return the number of days in month (1-12), leap-aware."""\n'
            "    year, month = int(year), int(month)\n"
            "    if month == 2:\n"
            "        leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n"
            "        return 29 if leap else 28\n"
            "    if month in (4, 6, 9, 11):\n"
            "        return 30\n"
            "    return 31\n",
            lambda low: "days in a month" in low or "days in month" in low,
            (
                ((2024, 2), 29),
                ((2023, 2), 28),
                ((2023, 4), 30),
            ),
        ),
        T(
            "catalan_number",
            "def catalan_number(n):\n"
            '    """Return the nth Catalan number C_n = (2n choose n) / (n+1)."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    c = 1\n"
            "    for k in range(n):\n"
            "        c = c * (2 * n - k) // (k + 1)\n"
            "    return c // (n + 1)\n",
            lambda low: "catalan" in low,
            (
                ((0,), 1),
                ((3,), 5),
                ((5,), 42),
            ),
        ),
    ]
