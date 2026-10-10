"""Cycle 451: SHA-1, CRC-32, Dice, thousands, query encode, HMS parse, triangular.

Pack loads before p168 so phrase gates beat broader hash/query/hms hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "sha1_hex",
            "def sha1_hex(text):\n"
            '    """FIPS 180-4 / RFC 3174 SHA-1 digest as lowercase hex."""\n'
            "    import hashlib\n"
            "    raw = text.encode('utf-8') if isinstance(text, str) else bytes(text)\n"
            "    return hashlib.sha1(raw).hexdigest()\n",
            lambda low: (
                ("sha1" in low or "sha-1" in low or "sha 1" in low)
                and "sha256" not in low
                and "sha-256" not in low
                and "md5" not in low
            ),
            (
                (("abc",), "a9993e364706816aba3e25717850c26c9cd0d89d"),
                (("",), "da39a3ee5e6b4b0d3255bfef95601890afd80709"),
            ),
        ),
        T(
            "crc32_hex",
            "def crc32_hex(text):\n"
            '    """ISO 3309 / ITU-T V.42 CRC-32 (zlib polynomial) as 8 hex digits."""\n'
            "    import zlib\n"
            "    raw = text.encode('utf-8') if isinstance(text, str) else bytes(text)\n"
            "    return f'{zlib.crc32(raw) & 0xFFFFFFFF:08x}'\n",
            lambda low: "crc32" in low or "crc-32" in low or "crc 32" in low,
            (
                (("abc",), "352441c2"),
                (("",), "00000000"),
            ),
        ),
        T(
            "dice_coefficient",
            "def dice_coefficient(a, b):\n"
            '    """Sorensen-Dice coefficient 2|A intersect B| / (|A|+|B|)."""\n'
            "    sa, sb = set(a), set(b)\n"
            "    denom = len(sa) + len(sb)\n"
            "    if denom == 0:\n"
            "        return 1.0\n"
            "    return (2 * len(sa & sb)) / denom\n",
            lambda low: (
                ("dice" in low and ("coefficient" in low or "sorensen" in low or "sørensen" in low))
                or "dice coefficient" in low
            ),
            (
                (([1, 2, 3], [2, 3, 4]), 2 / 3),
                (([], []), 1.0),
                (([1], [2]), 0.0),
            ),
        ),
        T(
            "thousands_separators",
            "def thousands_separators(n):\n"
            '    """Insert comma thousands separators. Keeps a leading minus."""\n'
            "    sign = '-' if int(n) < 0 else ''\n"
            "    digits = str(abs(int(n)))\n"
            "    parts = []\n"
            "    while digits:\n"
            "        parts.append(digits[-3:])\n"
            "        digits = digits[:-3]\n"
            "    return sign + ','.join(reversed(parts))\n",
            lambda low: (
                ("thousand" in low and ("separator" in low or "comma" in low or "format" in low))
                or "thousands separator" in low
            ),
            (
                ((1234567,), "1,234,567"),
                ((0,), "0"),
                ((-1000,), "-1,000"),
            ),
        ),
        T(
            "build_query",
            "def build_query(params):\n"
            '    """Encode a mapping as an application/x-www-form-urlencoded query string."""\n'
            "    from urllib.parse import urlencode\n"
            "    return urlencode([(str(k), '' if v is None else str(v)) for k, v in dict(params).items()])\n",
            lambda low: (
                ("query" in low)
                and ("build" in low or "encode" in low or "from a dict" in low or "from dict" in low)
                and "parse" not in low
            ),
            (
                (({"a": 1, "b": "x"},), "a=1&b=x"),
                (({},), ""),
            ),
        ),
        T(
            "hms_to_seconds",
            "def hms_to_seconds(text):\n"
            '    """Parse H:MM:SS or MM:SS into a non-negative second count."""\n'
            "    parts = [int(p) for p in str(text).split(':')]\n"
            "    if len(parts) == 2:\n"
            "        m, s = parts\n"
            "        h = 0\n"
            "    else:\n"
            "        h, m, s = parts[-3:]\n"
            "    return h * 3600 + m * 60 + s\n",
            lambda low: (
                ("hms" in low or "hh:mm:ss" in low or "h:mm:ss" in low)
                and ("to seconds" in low or "into seconds" in low or "parse" in low)
                and "to hms" not in low
            ),
            (
                (("1:01:01",), 3661),
                (("0:00:00",), 0),
                (("2:03",), 123),
            ),
        ),
        T(
            "triangular",
            "def triangular(n):\n"
            '    """nth triangular number n*(n+1)/2. Negative n returns 0."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        return 0\n"
            "    return n * (n + 1) // 2\n"
            "\n"
            "\n"
            "def triangle_number(n):\n"
            '    """Alias so smoke rows can expect either name."""\n'
            "    return triangular(n)\n",
            lambda low: "triangular" in low and "triangular sum" not in low and "triangular_sum" not in low,
            (
                ((0,), 0),
                ((1,), 1),
                ((5,), 15),
            ),
        ),
    ]
