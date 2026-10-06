"""Cycle 459: smootherstep, smoothstep, ISBN-13, Adler-32, map-range, slerp.

Pack loads first so smootherstep beats smoothstep and ISBN-13 beats ISBN-10.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "smootherstep",
            "def smootherstep(edge0, edge1, x):\n"
            '    """Ken Perlin smootherstep (C2 Hermite), clamped to [0, 1]."""\n'
            "    e0, e1 = float(edge0), float(edge1)\n"
            "    if e0 == e1:\n"
            "        return 0.0 if float(x) < e0 else 1.0\n"
            "    t = (float(x) - e0) / (e1 - e0)\n"
            "    t = 0.0 if t < 0.0 else 1.0 if t > 1.0 else t\n"
            "    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)\n",
            lambda low: "smootherstep" in low or "smoother step" in low or "smoother-step" in low,
            (
                ((0, 1, 0.5), 0.5),
                ((0, 1, 0), 0.0),
                ((0, 1, 1), 1.0),
            ),
        ),
        T(
            "smoothstep",
            "def smoothstep(edge0, edge1, x):\n"
            '    """GLSL/Perlin smoothstep (C1 Hermite), clamped to [0, 1]."""\n'
            "    e0, e1 = float(edge0), float(edge1)\n"
            "    if e0 == e1:\n"
            "        return 0.0 if float(x) < e0 else 1.0\n"
            "    t = (float(x) - e0) / (e1 - e0)\n"
            "    t = 0.0 if t < 0.0 else 1.0 if t > 1.0 else t\n"
            "    return t * t * (3.0 - 2.0 * t)\n",
            lambda low: (
                ("smoothstep" in low or "smooth step" in low or "smooth-step" in low)
                and "smoother" not in low
            ),
            (
                ((0, 1, 0.5), 0.5),
                ((0, 1, -1), 0.0),
                ((0, 1, 2), 1.0),
            ),
        ),
        T(
            "isbn13_valid",
            "def isbn13_valid(s):\n"
            '    """True if ISBN-13 check digit matches (weights 1,3)."""\n'
            "    digits = [c for c in str(s) if c.isdigit()]\n"
            "    if len(digits) != 13:\n"
            "        return False\n"
            "    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))\n"
            "    return total % 10 == 0\n",
            lambda low: "isbn" in low and ("13" in low or "isbn-13" in low or "isbn13" in low),
            (
                (("9780306406157",), True),
                (("9780306406158",), False),
                (("978030640615",), False),
            ),
        ),
        T(
            "adler32",
            "def adler32(text):\n"
            '    """Adler-32 checksum (RFC 1950), modulus 65521."""\n'
            "    a, b = 1, 0\n"
            "    for byte in str(text).encode(\"utf-8\"):\n"
            "        a = (a + byte) % 65521\n"
            "        b = (b + a) % 65521\n"
            "    return (b << 16) | a\n",
            lambda low: "adler" in low,
            (
                (("Wikipedia",), 300286872),
                (("",), 1),
            ),
        ),
        T(
            "map_range",
            "def map_range(x, in_min, in_max, out_min, out_max):\n"
            '    """Affine remap of x from [in_min, in_max] to [out_min, out_max]."""\n'
            "    src = float(in_max) - float(in_min)\n"
            "    if src == 0.0:\n"
            "        return float(out_min)\n"
            "    return float(out_min) + (float(x) - float(in_min)) * (float(out_max) - float(out_min)) / src\n",
            lambda low: (
                ("map range" in low or "remap" in low or "map_range" in low)
                and "hashmap" not in low
            ),
            (
                ((5, 0, 10, 0, 100), 50.0),
                ((0, 0, 10, 0, 100), 0.0),
            ),
        ),
        T(
            "slerp_scalar",
            "def slerp_scalar(a, b, t):\n"
            '    """Spherical lerp of two angles in radians, shortest arc."""\n'
            "    import math\n"
            "    aa, bb, tt = float(a), float(b), float(t)\n"
            "    delta = (bb - aa + math.pi) % (2.0 * math.pi) - math.pi\n"
            "    return aa + delta * tt\n",
            lambda low: "slerp" in low and "smooth" not in low,
            (
                ((0.0, 2.0, 0.5), 1.0),
                ((0.0, 0.0, 0.5), 0.0),
            ),
        ),
    ]
