"""Cycle 446: haversine, Levenshtein, Morse, hex-to-RGB, email, leap year.

Everyday asks with no template. Matchers are phrase-gated so unique Morse
and unique-email asks keep their names. Pack loads before p163.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "haversine_km",
            "def haversine_km(lat1, lon1, lat2, lon2):\n"
            '    """Great-circle distance in km, rounded to the nearest integer."""\n'
            "    import math\n"
            "    r = 6371.0\n"
            "    p1 = math.radians(float(lat1))\n"
            "    p2 = math.radians(float(lat2))\n"
            "    dphi = math.radians(float(lat2) - float(lat1))\n"
            "    dl = math.radians(float(lon2) - float(lon1))\n"
            "    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2\n"
            "    return int(round(2 * r * math.asin(math.sqrt(a))))\n",
            lambda low: "haversine" in low or "great circle" in low,
            (
                ((0, 0, 0, 0), 0),
                ((0, 0, 0, 1), 111),
                ((48.8566, 2.3522, 51.5074, -0.1278), 344),
            ),
        ),
        T(
            "hamming_distance",
            "def hamming_distance(a, b):\n"
            '    """Count differing positions; lengths must match."""\n'
            "    a, b = str(a), str(b)\n"
            "    if len(a) != len(b):\n"
            "        raise ValueError('hamming distance requires equal lengths')\n"
            "    return sum(x != y for x, y in zip(a, b))\n",
            lambda low: "hamming" in low and "distance" in low and "weight" not in low,
            ((("karolin", "kathrin"), 3), (("1010", "1110"), 1), (("same", "same"), 0)),
        ),
        T(
            "morse_encode",
            "def morse_encode(s):\n"
            '    """Encode letters and digits to ITU Morse; words separated by /."""\n'
            "    table = {\n"
            "        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',\n"
            "        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',\n"
            "        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',\n"
            "        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',\n"
            "        'Y': '-.--', 'Z': '--..',\n"
            "        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',\n"
            "        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',\n"
            "    }\n"
            "    words = []\n"
            "    for word in str(s).upper().split():\n"
            "        codes = [table[ch] for ch in word if ch in table]\n"
            "        if codes:\n"
            "            words.append(' '.join(codes))\n"
            "    return ' / '.join(words)\n",
            lambda low: (
                "morse" in low
                and "unique" not in low
                and "representation" not in low
            ),
            ((("SOS",), "... --- ..."), (("hi",), ".... .."), (("a b",), ".- / -...")),
        ),
        T(
            "hex_to_rgb",
            "def hex_to_rgb(s):\n"
            '    """Parse #RGB or #RRGGBB into an (r, g, b) tuple of ints."""\n'
            "    h = str(s).strip().lstrip('#')\n"
            "    if len(h) == 3:\n"
            "        h = ''.join(ch * 2 for ch in h)\n"
            "    if len(h) != 6:\n"
            "        raise ValueError('expected #RGB or #RRGGBB')\n"
            "    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))\n",
            lambda low: "hex" in low and "rgb" in low and "hsl" not in low,
            ((("#ff00aa",), (255, 0, 170)), (("abc",), (170, 187, 204)), (("#000000",), (0, 0, 0))),
        ),
        T(
            "is_email",
            "def is_email(s):\n"
            '    """True for a single local@domain form with a dot in the domain."""\n'
            "    text = str(s).strip()\n"
            "    if text.count('@') != 1 or ' ' in text:\n"
            "        return False\n"
            "    local, domain = text.split('@')\n"
            "    if not local or not domain or '.' not in domain:\n"
            "        return False\n"
            "    if domain.startswith('.') or domain.endswith('.'):\n"
            "        return False\n"
            "    return True\n",
            lambda low: (
                "email" in low
                and "unique" not in low
                and "morse" not in low
                and "defang" not in low
            ),
            ((("a@b.co",), True), (("not-an-email",), False), (("a@b",), False)),
        ),
        T(
            "is_leap_year",
            "def is_leap_year(year):\n"
            '    """Gregorian leap year: divisible by 4, but not by 100 unless by 400."""\n'
            "    y = int(year)\n"
            "    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)\n",
            lambda low: "leap" in low and "year" in low,
            (((2000,), True), ((1900,), False), ((2024,), True), ((2023,), False)),
        ),
    ]
