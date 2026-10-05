"""Cycle 449: base64 decode, Fahrenheit to Celsius, RLE decode, SHA-256, binomial, miles to km.

Pack loads before p166 so phrase-gated matchers beat decode_string and min_cost_paint_house.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "base64_decode",
            "def base64_decode(text):\n"
            '    """RFC 4648 standard base64 decode to a UTF-8 string."""\n'
            "    import base64\n"
            "    raw = text.encode('ascii') if isinstance(text, str) else bytes(text)\n"
            "    return base64.b64decode(raw).decode('utf-8')\n",
            lambda low: "base64" in low and "decode" in low and "encode" not in low,
            (
                (("aGk=",), "hi"),
                (("Zg==",), "f"),
                (("TWFu",), "Man"),
            ),
        ),
        T(
            "fahrenheit_to_celsius",
            "def fahrenheit_to_celsius(f):\n"
            '    """Convert Fahrenheit to Celsius: C = (F - 32) * 5/9."""\n'
            "    return (float(f) - 32.0) * 5.0 / 9.0\n",
            lambda low: (
                "fahrenheit" in low
                and "celsius" in low
                and "to fahrenheit" not in low
                and ("to celsius" in low or "from fahrenheit" in low)
            ),
            (
                ((32,), 0.0),
                ((212,), 100.0),
                ((-40,), -40.0),
            ),
        ),
        T(
            "run_length_decode",
            "def run_length_decode(pairs):\n"
            '    """Expand (char, count) runs produced by run_length_encode."""\n'
            "    out = []\n"
            "    for item in pairs:\n"
            "        ch, count = item\n"
            "        out.append(str(ch) * int(count))\n"
            "    return ''.join(out)\n",
            lambda low: (
                ("run-length" in low or "run length" in low or "rle" in low)
                and "decode" in low
                and "encode" not in low
            ),
            (
                (([("a", 3), ("b", 2)],), "aaabb"),
                (([],), ""),
                (([("x", 1)],), "x"),
            ),
        ),
        T(
            "sha256_hex",
            "def sha256_hex(text):\n"
            '    """SHA-256 digest of a UTF-8 string as lowercase hex (FIPS 180-4)."""\n'
            "    import hashlib\n"
            "    raw = text.encode('utf-8') if isinstance(text, str) else bytes(text)\n"
            "    return hashlib.sha256(raw).hexdigest()\n",
            lambda low: "sha256" in low or "sha-256" in low,
            (
                (
                    ("abc",),
                    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                ),
                (
                    ("",),
                    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                ),
            ),
        ),
        T(
            "binomial",
            "def binomial(n, k):\n"
            '    """Binomial coefficient C(n, k) via the multiplicative formula."""\n'
            "    n = int(n)\n"
            "    k = int(k)\n"
            "    if k < 0 or n < 0 or k > n:\n"
            "        return 0\n"
            "    k = min(k, n - k)\n"
            "    result = 1\n"
            "    for i in range(1, k + 1):\n"
            "        result = result * (n - k + i) // i\n"
            "    return result\n",
            lambda low: (
                "binomial" in low
                or "n choose k" in low
                or "choose k" in low
                or "combination coefficient" in low
            ),
            (
                ((5, 2), 10),
                ((6, 0), 1),
                ((10, 3), 120),
                ((5, 5), 1),
                ((4, 5), 0),
            ),
        ),
        T(
            "miles_to_km",
            "def miles_to_km(miles):\n"
            '    """International mile to kilometres (1 mi = 1.609344 km)."""\n'
            "    return float(miles) * 1.609344\n",
            lambda low: (
                ("mile" in low)
                and ("kilometer" in low or "kilometre" in low or "km" in low)
                and "to mile" not in low
                and "from km" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 1.609344),
                ((2,), 3.218688),
            ),
        ),
    ]
