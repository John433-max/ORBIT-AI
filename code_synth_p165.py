"""Cycle 447: RGB-to-hex, any-base, int-to-Roman, URL encode, word wrap, weekday.

Matchers are phrase-gated so hex-to-RGB, base-7, and Roman-to-int keep their names.
Pack loads before p164.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "rgb_to_hex",
            "def rgb_to_hex(r, g, b):\n"
            '    """Pack 0-255 channels as a #rrggbb CSS color."""\n'
            "    chans = []\n"
            "    for v in (r, g, b):\n"
            "        n = int(v)\n"
            "        if n < 0 or n > 255:\n"
            "            raise ValueError('channel out of range')\n"
            "        chans.append(f'{n:02x}')\n"
            "    return '#' + ''.join(chans)\n",
            lambda low: "rgb" in low and "hex" in low and "to rgb" not in low and "hex color" not in low and "hex to" not in low,
            (
                ((255, 128, 0), "#ff8000"),
                ((0, 0, 0), "#000000"),
                ((15, 16, 255), "#0f10ff"),
            ),
        ),
        T(
            "int_to_base",
            "def int_to_base(n, base):\n"
            '    """Write a non-negative integer in base 2..36."""\n'
            "    n = int(n)\n"
            "    base = int(base)\n"
            "    if n < 0:\n"
            "        raise ValueError('n must be non-negative')\n"
            "    if base < 2 or base > 36:\n"
            "        raise ValueError('base must be 2..36')\n"
            "    digits = '0123456789abcdefghijklmnopqrstuvwxyz'\n"
            "    if n == 0:\n"
            "        return '0'\n"
            "    out = []\n"
            "    while n:\n"
            "        n, rem = divmod(n, base)\n"
            "        out.append(digits[rem])\n"
            "    return ''.join(reversed(out))\n",
            lambda low: (
                ("to base" in low or "in base" in low or "any base" in low or "integer to base" in low)
                and "base7" not in low
                and "base 7" not in low
                and "base-7" not in low
            ),
            (
                ((255, 16), "ff"),
                ((10, 2), "1010"),
                ((0, 8), "0"),
                ((35, 36), "z"),
            ),
        ),
        T(
            "sample_stdev",
            "def sample_stdev(nums):\n"
            '    """Sample standard deviation (n-1). Needs at least two numbers."""\n'
            "    xs = [float(x) for x in nums]\n"
            "    n = len(xs)\n"
            "    if n < 2:\n"
            "        raise ValueError('need at least two values')\n"
            "    mean = sum(xs) / n\n"
            "    var = sum((x - mean) ** 2 for x in xs) / (n - 1)\n"
            "    return var ** 0.5\n",
            lambda low: (
                ("standard deviation" in low or "stdev" in low or "std dev" in low)
                and "population" not in low
            ),
            (
                (([2, 4, 4, 4, 5, 5, 7, 9],), 2.138089935299395),
                (([1, 2, 3],), 1.0),
            ),
        ),
        T(
            "url_encode",
            "def url_encode(text):\n"
            '    """Percent-encode every byte except RFC 3986 unreserved characters."""\n'
            "    from urllib.parse import quote\n"
            "    return quote(str(text), safe='')\n",
            lambda low: (
                ("url encode" in low or "percent-encode" in low or "percent encode" in low or "percent-encoding" in low)
                and "decode" not in low
            ),
            (
                (("a b",), "a%20b"),
                (("/",), "%2F"),
                (("hello",), "hello"),
            ),
        ),
        T(
            "word_wrap",
            "def word_wrap(text, width):\n"
            '    """Greedy wrap on spaces; words longer than width stay intact."""\n'
            "    width = int(width)\n"
            "    if width < 1:\n"
            "        raise ValueError('width must be positive')\n"
            "    words = str(text).split()\n"
            "    lines = []\n"
            "    cur = ''\n"
            "    for word in words:\n"
            "        if not cur:\n"
            "            cur = word\n"
            "        elif len(cur) + 1 + len(word) <= width:\n"
            "            cur += ' ' + word\n"
            "        else:\n"
            "            lines.append(cur)\n"
            "            cur = word\n"
            "    if cur:\n"
            "        lines.append(cur)\n"
            "    return '\\n'.join(lines)\n",
            lambda low: (
                "word wrap" in low
                or "word-wrap" in low
                or "wrap text" in low
                or "wraps text" in low
                or "wrap words" in low
                or "text to a width" in low
            ),
            (
                (("hello world", 5), "hello\nworld"),
                (("aa bb cc", 5), "aa bb\ncc"),
                (("hi", 10), "hi"),
            ),
        ),
        T(
            "weekday_name",
            "def weekday_name(year, month, day):\n"
            '    """Gregorian weekday name for a civil date."""\n'
            "    import datetime\n"
            "    return datetime.date(int(year), int(month), int(day)).strftime('%A')\n",
            lambda low: "weekday" in low or "day of week" in low or "day-of-week" in low,
            (
                ((2026, 10, 5), "Monday"),
                ((2000, 1, 1), "Saturday"),
                ((2024, 2, 29), "Thursday"),
            ),
        ),
    ]
