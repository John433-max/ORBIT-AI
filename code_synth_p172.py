"""Cycle 454: ISO week, pluralize, collapse space, deep get, Spearman, accents, n-grams, geometric mean, ordinal.

Pack loads first so phrase gates beat broader string/stats hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "iso_week",
            "def iso_week(year, month, day):\n"
            '    """ISO 8601 week date (year, week, weekday) for a civil date."""\n'
            "    import datetime\n"
            "    return tuple(datetime.date(int(year), int(month), int(day)).isocalendar())\n",
            lambda low: "iso week" in low or "isocalendar" in low or "iso-8601 week" in low,
            (
                ((2024, 1, 1), (2024, 1, 1)),
                ((2021, 1, 1), (2020, 53, 5)),
            ),
        ),
        T(
            "pluralize",
            "def pluralize(word, count=2):\n"
            '    """Simple English plural (irregulars + y->ies). Not a full inflection library."""\n'
            "    w = str(word)\n"
            "    n = int(count)\n"
            "    if n == 1:\n"
            "        return w\n"
            "    irregular = {\n"
            "        'child': 'children', 'person': 'people', 'man': 'men',\n"
            "        'woman': 'women', 'mouse': 'mice', 'tooth': 'teeth', 'foot': 'feet',\n"
            "    }\n"
            "    key = w.lower()\n"
            "    if key in irregular:\n"
            "        out = irregular[key]\n"
            "        return out.capitalize() if w[:1].isupper() else out\n"
            "    if len(w) > 1 and w.endswith('y') and w[-2].lower() not in 'aeiou':\n"
            "        return w[:-1] + 'ies'\n"
            "    if w.endswith(('s', 'x', 'z', 'ch', 'sh')):\n"
            "        return w + 'es'\n"
            "    return w + 's'\n",
            lambda low: "pluralize" in low or "pluralise" in low,
            (
                (("cat", 1), "cat"),
                (("cat", 2), "cats"),
                (("city", 3), "cities"),
                (("child", 2), "children"),
                (("box", 2), "boxes"),
            ),
        ),
        T(
            "collapse_whitespace",
            "def collapse_whitespace(text):\n"
            '    """Collapse runs of whitespace to a single space and strip ends."""\n'
            "    import re\n"
            "    return re.sub(r'\\s+', ' ', str(text)).strip()\n",
            lambda low: (
                ("collapse" in low and "whitespace" in low)
                or "collapse spaces" in low
                or "normalize whitespace" in low
                or "squash whitespace" in low
            ),
            (
                (("a  b\n\tc",), "a b c"),
                (("  hi  ",), "hi"),
            ),
        ),
        T(
            "deep_get",
            "def deep_get(obj, path, default=None):\n"
            '    """Walk a dotted path (dict keys or list indexes). Missing path returns default."""\n'
            "    cur = obj\n"
            "    for part in str(path).split('.'):\n"
            "        if part == '':\n"
            "            continue\n"
            "        if isinstance(cur, dict) and part in cur:\n"
            "            cur = cur[part]\n"
            "        elif isinstance(cur, (list, tuple)) and part.lstrip('-').isdigit():\n"
            "            idx = int(part)\n"
            "            if -len(cur) <= idx < len(cur):\n"
            "                cur = cur[idx]\n"
            "            else:\n"
            "                return default\n"
            "        else:\n"
            "            return default\n"
            "    return cur\n",
            lambda low: "deep get" in low or "dotted path" in low or "nested get" in low,
            (
                (({"a": {"b": 1}}, "a.b"), 1),
                (({"a": {"b": [9, 8]}}, "a.b.1"), 8),
                (({"a": 1}, "a.c", 0), 0),
            ),
        ),
        T(
            "spearman",
            "def spearman(xs, ys):\n"
            '    """Spearman rank correlation (average ranks on ties), rounded to 10 decimals."""\n'
            "    xs, ys = list(xs), list(ys)\n"
            "    if len(xs) != len(ys) or len(xs) < 2:\n"
            "        return None\n"
            "    def ranks(vals):\n"
            "        order = sorted(range(len(vals)), key=lambda i: vals[i])\n"
            "        r = [0.0] * len(vals)\n"
            "        i = 0\n"
            "        while i < len(vals):\n"
            "            j = i\n"
            "            while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:\n"
            "                j += 1\n"
            "            avg = (i + j) / 2 + 1\n"
            "            for k in range(i, j + 1):\n"
            "                r[order[k]] = avg\n"
            "            i = j + 1\n"
            "        return r\n"
            "    rx, ry = ranks(xs), ranks(ys)\n"
            "    n = len(xs)\n"
            "    mx, my = sum(rx) / n, sum(ry) / n\n"
            "    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))\n"
            "    dx = sum((a - mx) ** 2 for a in rx) ** 0.5\n"
            "    dy = sum((b - my) ** 2 for b in ry) ** 0.5\n"
            "    if dx == 0 or dy == 0:\n"
            "        return None\n"
            "    return round(num / (dx * dy), 10)\n",
            lambda low: "spearman" in low,
            (
                (([1, 2, 3], [3, 2, 1]), -1.0),
                (([10, 20, 30], [1, 2, 3]), 1.0),
                (([1, 2, 2], [1, 3, 2]), 0.8660254038),
            ),
        ),
        T(
            "strip_accents",
            "def strip_accents(text):\n"
            '    """Remove combining marks after NFD (Unicode accent folding)."""\n'
            "    import unicodedata\n"
            "    nfd = unicodedata.normalize('NFD', str(text))\n"
            "    return ''.join(ch for ch in nfd if unicodedata.category(ch) != 'Mn')\n",
            lambda low: (
                ("accent" in low and ("strip" in low or "remove" in low or "fold" in low))
                or "without accents" in low
            ),
            (
                (("é",), "e"),
                (("caf\u00e9",), "cafe"),
                (("naïve",), "naive"),
            ),
        ),
        T(
            "char_ngrams",
            "def char_ngrams(text, n):\n"
            '    """Overlapping character n-grams of a string."""\n'
            "    s = str(text)\n"
            "    k = int(n)\n"
            "    if k <= 0 or k > len(s):\n"
            "        return []\n"
            "    return [s[i:i + k] for i in range(len(s) - k + 1)]\n",
            lambda low: "n-gram" in low or "ngram" in low or "character gram" in low,
            (
                (("abc", 2), ["ab", "bc"]),
                (("ab", 3), []),
                (("aaaa", 1), ["a", "a", "a", "a"]),
            ),
        ),
        T(
            "geometric_mean",
            "def geometric_mean(values):\n"
            '    """Geometric mean of positive numbers, rounded to 6 decimals. Non-positive -> None."""\n'
            "    xs = list(values)\n"
            "    if not xs or any(x <= 0 for x in xs):\n"
            "        return None\n"
            "    acc = 1.0\n"
            "    for x in xs:\n"
            "        acc *= float(x)\n"
            "    return round(acc ** (1.0 / len(xs)), 6)\n",
            lambda low: "geometric mean" in low,
            (
                (([1, 3, 9],), 3.0),
                (([4, 9],), 6.0),
                (([1, 0, 2],), None),
            ),
        ),
        T(
            "ordinal",
            "def ordinal(n):\n"
            '    """English ordinal suffix (1st, 2nd, 3rd, 4th; 11th-13th stay th)."""\n'
            "    i = int(n)\n"
            "    if 10 <= (i % 100) <= 20:\n"
            "        suf = 'th'\n"
            "    else:\n"
            "        suf = {1: 'st', 2: 'nd', 3: 'rd'}.get(i % 10, 'th')\n"
            "    return f'{i}{suf}'\n",
            lambda low: "ordinal" in low and "encode" not in low,
            (
                ((1,), "1st"),
                ((2,), "2nd"),
                ((3,), "3rd"),
                ((11,), "11th"),
                ((22,), "22nd"),
            ),
        ),
    ]
