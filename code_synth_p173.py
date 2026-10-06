"""Cycle 455: Manhattan, Chebyshev, softmax, IQR, Vigenere, HTML escape, lerp, mod inverse.

Pack loads first so phrase gates beat broader distance/html/math hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "manhattan_distance",
            "def manhattan_distance(a, b):\n"
            '    """L1 distance between equal-length numeric vectors."""\n'
            "    if len(a) != len(b):\n"
            '        raise ValueError("dimension mismatch")\n'
            "    return sum(abs(x - y) for x, y in zip(a, b))\n",
            lambda low: "manhattan" in low,
            (
                (([0, 0], [3, 4]), 7),
                (([1, 2, 3], [1, 2, 3]), 0),
            ),
        ),
        T(
            "chebyshev_distance",
            "def chebyshev_distance(a, b):\n"
            '    """L-inf distance between equal-length numeric vectors."""\n'
            "    if len(a) != len(b):\n"
            '        raise ValueError("dimension mismatch")\n'
            "    return max(abs(x - y) for x, y in zip(a, b))\n",
            lambda low: "chebyshev" in low,
            (
                (([0, 0], [3, 4]), 4),
                (([1, -2], [1, 5]), 7),
            ),
        ),
        T(
            "softmax",
            "def softmax(xs):\n"
            '    """Numerically stable softmax. Empty input returns []."""\n'
            "    import math\n"
            "    if not xs:\n"
            "        return []\n"
            "    m = max(xs)\n"
            "    exps = [math.exp(x - m) for x in xs]\n"
            "    total = sum(exps)\n"
            "    return [e / total for e in exps]\n",
            lambda low: "softmax" in low,
            (
                (([0, 0],), [0.5, 0.5]),
                (([1],), [1.0]),
                (([],), []),
            ),
        ),
        T(
            "interquartile_range",
            "def interquartile_range(xs):\n"
            '    """IQR via linear percentile on a sorted copy (needs >= 4 values)."""\n'
            "    vals = sorted(xs)\n"
            "    n = len(vals)\n"
            "    if n < 4:\n"
            '        raise ValueError("need at least 4 values")\n'
            "    def _q(p):\n"
            "        idx = (n - 1) * p\n"
            "        lo = int(idx)\n"
            "        hi = min(lo + 1, n - 1)\n"
            "        frac = idx - lo\n"
            "        return vals[lo] * (1 - frac) + vals[hi] * frac\n"
            "    return _q(0.75) - _q(0.25)\n",
            lambda low: "interquartile" in low or "iqr" in low,
            (
                (([1, 2, 3, 4],), 1.5),
                (([1, 2, 3, 4, 5, 6, 7, 8],), 3.5),
            ),
        ),
        T(
            "vigenere_encrypt",
            "def vigenere_encrypt(text, key):\n"
            '    """Vigenere encrypt; non-letters kept; key letters only."""\n'
            "    key = ''.join(c for c in str(key) if c.isalpha()).lower()\n"
            "    if not key:\n"
            "        return str(text)\n"
            "    out = []\n"
            "    j = 0\n"
            "    for ch in str(text):\n"
            "        if ch.isalpha():\n"
            "            base = ord('A') if ch.isupper() else ord('a')\n"
            "            shift = ord(key[j % len(key)]) - ord('a')\n"
            "            out.append(chr(base + (ord(ch) - base + shift) % 26))\n"
            "            j += 1\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: "vigenere" in low or "vigenère" in low,
            (
                (("attackatdawn", "lemon"), "lxfopvefrnhr"),
                (("Hello!", "ab"), "Hflmo!"),
            ),
        ),
        T(
            "escape_html",
            'def escape_html(text):\n    """Escape ampersand, lt, gt, and double quotes for HTML text."""\n    return (\n        str(text)\n        .replace(chr(38), chr(38) + \'amp;\')\n        .replace(chr(60), chr(38) + \'lt;\')\n        .replace(chr(62), chr(38) + \'gt;\')\n        .replace(chr(34), chr(38) + \'quot;\')\n    )\n',
            lambda low: ("escape" in low and "html" in low) or "html escape" in low,
            (
                (('<a & b>',), '&lt;a &amp; b&gt;'),
                (("say \"hi\"",), 'say &quot;hi&quot;'),
            ),
        ),
        T(
            "lerp",
            "def lerp(a, b, t):\n"
            '    """Linear interpolation: a + (b - a) * t."""\n'
            "    return a + (b - a) * t\n",
            lambda low: "lerp" in low or "linearly interpolat" in low or "linear interpolation" in low,
            (
                ((0, 10, 0.5), 5.0),
                ((2, 4, 0), 2),
            ),
        ),
        T(
            "mod_inverse",
            "def mod_inverse(a, m):\n"
            '    """Modular inverse of a modulo m, or ValueError if none exists."""\n'
            "    def egcd(x, y):\n"
            "        if y == 0:\n"
            "            return x, 1, 0\n"
            "        g, s, t = egcd(y, x % y)\n"
            "        return g, t, s - (x // y) * t\n"
            "    g, x, _ = egcd(int(a) % int(m), int(m))\n"
            "    if g != 1:\n"
            '        raise ValueError("no inverse")\n'
            "    return x % int(m)\n",
            lambda low: "modular inverse" in low or "mod inverse" in low or "multiplicative inverse" in low,
            (
                ((3, 11), 4),
                ((10, 17), 12),
            ),
        ),
    ]
