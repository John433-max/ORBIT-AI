"""Cycle 448: prime factors, base64 encode, Celsius, URL decode, percentile, z-scores.

Matchers are phrase-gated so is_prime, decode_string, and sample_stdev keep their names.
Pack loads before p165.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "prime_factors",
            "def prime_factors(n):\n"
            '    """Trial-division prime factors, smallest first, with repeats."""\n'
            "    n = int(n)\n"
            "    if n < 2:\n"
            "        return []\n"
            "    out = []\n"
            "    d = 2\n"
            "    while d * d <= n:\n"
            "        while n % d == 0:\n"
            "            out.append(d)\n"
            "            n //= d\n"
            "        d += 1 if d == 2 else 2\n"
            "    if n > 1:\n"
            "        out.append(n)\n"
            "    return out\n",
            lambda low: (
                "prime factor" in low
                or "prime factorization" in low
                or "factorize" in low
            ),
            (
                ((84,), [2, 2, 3, 7]),
                ((13,), [13]),
                ((1,), []),
                ((360,), [2, 2, 2, 3, 3, 5]),
            ),
        ),
        T(
            "base64_encode",
            "def base64_encode(text):\n"
            '    """RFC 4648 standard base64 of a UTF-8 string."""\n'
            "    import base64\n"
            "    raw = text.encode('utf-8') if isinstance(text, str) else bytes(text)\n"
            "    return base64.b64encode(raw).decode('ascii')\n",
            lambda low: "base64" in low and "decode" not in low,
            (
                (("hi",), "aGk="),
                (("f",), "Zg=="),
                (("Man",), "TWFu"),
            ),
        ),
        T(
            "celsius_to_fahrenheit",
            "def celsius_to_fahrenheit(c):\n"
            '    """Convert Celsius to Fahrenheit: F = C * 9/5 + 32."""\n'
            "    return float(c) * 9.0 / 5.0 + 32.0\n",
            lambda low: "celsius" in low and "fahrenheit" in low and "to celsius" not in low,
            (
                ((0,), 32.0),
                ((100,), 212.0),
                ((-40,), -40.0),
            ),
        ),
        T(
            "url_decode",
            "def url_decode(text):\n"
            '    """Percent-decode a string (urllib.parse.unquote). Does not treat + as space."""\n'
            "    from urllib.parse import unquote\n"
            "    return unquote(str(text))\n",
            lambda low: (
                ("url" in low or "percent" in low)
                and "decode" in low
                and "encode" not in low
            ),
            (
                (("%20hello%21",), " hello!"),
                (("a%2Fb",), "a/b"),
                (("plain",), "plain"),
            ),
        ),
        T(
            "percentile",
            "def percentile(nums, p):\n"
            '    """Nearest-rank percentile. p is 0..100."""\n'
            "    import math\n"
            "    xs = sorted(float(x) for x in nums)\n"
            "    if not xs:\n"
            "        raise ValueError('empty')\n"
            "    p = float(p)\n"
            "    if p <= 0:\n"
            "        return xs[0]\n"
            "    if p >= 100:\n"
            "        return xs[-1]\n"
            "    rank = max(1, math.ceil(p / 100.0 * len(xs)))\n"
            "    return xs[rank - 1]\n",
            lambda low: "percentile" in low and "percent" not in low.replace("percentile", ""),
            (
                (([1, 2, 3, 4, 5], 50), 3.0),
                (([1, 2, 3, 4], 0), 1.0),
                (([1, 2, 3, 4], 100), 4.0),
                (([10, 20, 30], 40), 20.0),
            ),
        ),
        T(
            "z_scores",
            "def z_scores(nums):\n"
            '    """Population z-scores (divide by n, not n-1)."""\n'
            "    xs = [float(x) for x in nums]\n"
            "    n = len(xs)\n"
            "    if n == 0:\n"
            "        return []\n"
            "    mean = sum(xs) / n\n"
            "    var = sum((x - mean) ** 2 for x in xs) / n\n"
            "    if var == 0:\n"
            "        return [0.0 for _ in xs]\n"
            "    sd = var ** 0.5\n"
            "    return [(x - mean) / sd for x in xs]\n",
            lambda low: (
                ("z-score" in low or "z score" in low or "zscore" in low)
                and "sample" not in low
            ),
            (
                (([1, 2, 3],), [-1.224744871391589, 0.0, 1.224744871391589]),
                (([5, 5, 5],), [0.0, 0.0, 0.0]),
            ),
        ),
    ]
