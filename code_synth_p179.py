"""Cycle 461: phrase-gated weather, phonetic, and direction helpers.

Loaded first so integer-to-Roman beats the broader roman-numeral matcher,
and METAR / dew-point / bearing asks do not fall through to a stub.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "integer_to_roman",
            "def integer_to_roman(num):\n"
            '    """Convert a positive integer to a Roman numeral (standard subtractive)."""\n'
            "    num = int(num)\n"
            "    vals = [\n"
            "        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),\n"
            "        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),\n"
            "        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'),\n"
            "    ]\n"
            "    out = []\n"
            "    for v, s in vals:\n"
            "        if num <= 0:\n"
            "            break\n"
            "        k, num = divmod(num, v)\n"
            "        out.append(s * k)\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"integer to roman|int to roman|to a roman numeral|"
                    r"roman numerals? from|returns roman numeral",
                    low,
                )
                and "roman to int" not in low
                and "from roman" not in low
                and "roman numeral to" not in low
            ),
            (((3,), "III"), ((58,), "LVIII"), ((1994,), "MCMXCIV")),
        ),
        T(
            "parse_metar",
            "def parse_metar(report):\n"
            '    """Parse station, wind, temp/dewpoint, and altimeter from a METAR body."""\n'
            "    import re\n"
            "    text = str(report).upper()\n"
            "    out = {}\n"
            "    for tok in text.split():\n"
            "        if len(tok) == 4 and tok.isalpha() and tok not in {'METAR', 'SPECI', 'AUTO'}:\n"
            "            out['station'] = tok\n"
            "            break\n"
            "    wind = re.search(r'\\b(\\d{3})(\\d{2,3})(G(\\d{2,3}))?KT\\b', text)\n"
            "    if wind:\n"
            "        out['wind_dir'] = int(wind.group(1))\n"
            "        out['wind_kt'] = int(wind.group(2))\n"
            "        if wind.group(4):\n"
            "            out['gust_kt'] = int(wind.group(4))\n"
            "    td = re.search(r'\\b(M?\\d{2})/(M?\\d{2})\\b', text)\n"
            "    if td:\n"
            "        def _t(s):\n"
            "            return -int(s[1:]) if s.startswith('M') else int(s)\n"
            "        out['temp_c'] = _t(td.group(1))\n"
            "        out['dewpoint_c'] = _t(td.group(2))\n"
            "    alt = re.search(r'\\bA(\\d{4})\\b', text)\n"
            "    if alt:\n"
            "        out['altimeter_inhg'] = int(alt.group(1)) / 100.0\n"
            "    return out\n",
            lambda low: "metar" in low and "taf" not in low,
            (
                (
                    ("METAR KJFK 121251Z 18015G20KT 10SM FEW030 22/M01 A2992",),
                    {
                        "station": "KJFK",
                        "wind_dir": 180,
                        "wind_kt": 15,
                        "gust_kt": 20,
                        "temp_c": 22,
                        "dewpoint_c": -1,
                        "altimeter_inhg": 29.92,
                    },
                ),
                (("KJFK 090751Z 24006KT 10SM FEW250 24/22 A2995",), {
                    "station": "KJFK",
                    "wind_dir": 240,
                    "wind_kt": 6,
                    "temp_c": 24,
                    "dewpoint_c": 22,
                    "altimeter_inhg": 29.95,
                }),
            ),
        ),
        T(
            "dew_point_c",
            "def dew_point_c(temp_c, rh):\n"
            '    """Magnus dew point (a=17.27, b=237.7) from Celsius and percent RH."""\n'
            "    import math\n"
            "    t = float(temp_c)\n"
            "    humidity = min(100.0, max(0.1, float(rh)))\n"
            "    gamma = math.log(humidity / 100.0) + (17.27 * t) / (237.7 + t)\n"
            "    return round((237.7 * gamma) / (17.27 - gamma), 2)\n",
            lambda low: "dew" in low and ("point" in low or "dewpoint" in low) and "metar" not in low,
            (((20, 50), 9.25), ((25, 100), 25.0)),
        ),
        T(
            "initial_bearing",
            "def initial_bearing(lat1, lon1, lat2, lon2):\n"
            '    """Initial great-circle bearing in degrees, 0..360."""\n'
            "    import math\n"
            "    p1, p2 = math.radians(float(lat1)), math.radians(float(lat2))\n"
            "    dl = math.radians(float(lon2) - float(lon1))\n"
            "    y = math.sin(dl) * math.cos(p2)\n"
            "    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)\n"
            "    return round((math.degrees(math.atan2(y, x)) + 360.0) % 360.0, 2)\n",
            lambda low: ("bearing" in low or "azimuth" in low) and "metar" not in low,
            (((0, 0, 0, 1), 90.0), ((40.7128, -74.006, 51.5074, -0.1278), 51.21)),
        ),
        T(
            "next_prime",
            "def next_prime(n):\n"
            '    """Smallest prime strictly greater than n."""\n'
            "    n = int(n)\n"
            "    cand = 2 if n < 2 else n + 1\n"
            "    if cand > 2 and cand % 2 == 0:\n"
            "        cand += 1\n"
            "    def _prime(x):\n"
            "        if x < 2:\n"
            "            return False\n"
            "        if x % 2 == 0:\n"
            "            return x == 2\n"
            "        i = 3\n"
            "        while i * i <= x:\n"
            "            if x % i == 0:\n"
            "                return False\n"
            "            i += 2\n"
            "        return True\n"
            "    while not _prime(cand):\n"
            "        cand += 1 if cand == 2 else 2\n"
            "    return cand\n",
            lambda low: "next prime" in low or "next_prime" in low,
            (((1,), 2), ((10,), 11), ((11,), 13)),
        ),
        T(
            "metaphone_primary",
            "def metaphone_primary(word):\n"
            '    """Reduced primary metaphone (Philips 1990 style, not Metaphone 3)."""\n'
            "    raw = ''.join(ch for ch in str(word).upper() if ch.isalpha())\n"
            "    if not raw:\n"
            "        return ''\n"
            "    if raw.startswith('KN') or raw.startswith('GN') or raw.startswith('PN') or raw.startswith('WR'):\n"
            "        raw = raw[1:]\n"
            "    raw = raw.replace('PH', 'F')\n"
            "    out = []\n"
            "    i = 0\n"
            "    while i < len(raw) and len(out) < 4:\n"
            "        ch = raw[i]\n"
            "        nxt = raw[i + 1] if i + 1 < len(raw) else ''\n"
            "        if ch in 'AEIOU':\n"
            "            if i == 0:\n"
            "                out.append(ch)\n"
            "            i += 1\n"
            "            continue\n"
            "        if ch == 'B':\n"
            "            if i + 1 != len(raw) or raw[i - 1:i] != 'M':\n"
            "                out.append('B')\n"
            "        elif ch == 'C':\n"
            "            out.append('S' if nxt in 'EIY' else 'K')\n"
            "        elif ch == 'D':\n"
            "            out.append('J' if nxt == 'G' and raw[i + 2:i + 3] in 'EIY' else 'T')\n"
            "        elif ch == 'G':\n"
            "            if nxt not in 'EIY':\n"
            "                out.append('K')\n"
            "            else:\n"
            "                out.append('J')\n"
            "        elif ch in 'H':\n"
            "            if nxt in 'AEIOU' and (i == 0 or raw[i - 1] not in 'CSPTG'):\n"
            "                out.append('H')\n"
            "        elif ch == 'K':\n"
            "            if i == 0 or raw[i - 1] != 'C':\n"
            "                out.append('K')\n"
            "        elif ch == 'P':\n"
            "            out.append('F' if nxt == 'H' else 'P')\n"
            "            if nxt == 'H':\n"
            "                i += 1\n"
            "        elif ch == 'Q':\n"
            "            out.append('K')\n"
            "        elif ch == 'S':\n"
            "            out.append('X' if nxt == 'H' else 'S')\n"
            "        elif ch == 'T':\n"
            "            if raw[i:i + 2] == 'TH':\n"
            "                out.append('0')\n"
            "                i += 1\n"
            "            else:\n"
            "                out.append('T')\n"
            "        elif ch in 'VW':\n"
            "            out.append('F' if ch == 'V' else 'W')\n"
            "        elif ch == 'X':\n"
            "            out.append('KS')\n"
            "        elif ch == 'Y':\n"
            "            if nxt in 'AEIOU':\n"
            "                out.append('Y')\n"
            "        elif ch == 'Z':\n"
            "            out.append('S')\n"
            "        elif ch in 'FJLMNR':\n"
            "            out.append(ch)\n"
            "        i += 1\n"
            "    return ''.join(out)[:4]\n",
            lambda low: "metaphone" in low and "double metaphone" not in low,
            ((("Smith",), "SM0"), (("Robert",), "RBRT"), (("phone",), "FN")),
        ),
    ]
