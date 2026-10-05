"""Cycle 450: MD5 hex, Jaccard, humanize bytes, kebab-case, strip HTML, cosine.

Pack loads before p167 so phrase-gated matchers beat broader decode/string hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "md5_hex",
            "def md5_hex(text):\n"
            '    """RFC 1321 MD5 digest as a lowercase hex string."""\n'
            "    import hashlib\n"
            "    raw = text.encode('utf-8') if isinstance(text, str) else bytes(text)\n"
            "    return hashlib.md5(raw).hexdigest()\n",
            lambda low: "md5" in low and "sha" not in low,
            (
                (("abc",), "900150983cd24fb0d6963f7d28e17f72"),
                (("",), "d41d8cd98f00b204e9800998ecf8427e"),
            ),
        ),
        T(
            "jaccard_similarity",
            "def jaccard_similarity(a, b):\n"
            '    """Jaccard index |A intersect B| / |A union B| (Jaccard 1901)."""\n'
            "    sa, sb = set(a), set(b)\n"
            "    union = sa | sb\n"
            "    if not union:\n"
            "        return 1.0\n"
            "    return len(sa & sb) / len(union)\n",
            lambda low: "jaccard" in low,
            (
                (([1, 2, 3], [2, 3, 4]), 0.5),
                (([], []), 1.0),
                (([1], [2]), 0.0),
            ),
        ),
        T(
            "humanize_bytes",
            "def humanize_bytes(n):\n"
            '    """IEC 80000-13 binary prefixes (1024)."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        return '-' + humanize_bytes(-n)\n"
            "    units = ('B', 'KiB', 'MiB', 'GiB', 'TiB')\n"
            "    value = float(n)\n"
            "    for unit in units:\n"
            "        if value < 1024.0 or unit == units[-1]:\n"
            "            if unit == 'B':\n"
            "                return f'{int(value)} B'\n"
            "            return f'{value:.1f} {unit}'\n"
            "        value /= 1024.0\n"
            "    return f'{int(n)} B'\n",
            lambda low: (
                ("byte" in low or "bytes" in low)
                and ("human" in low or "readable" in low or "humanize" in low)
            ),
            (
                ((0,), "0 B"),
                ((1024,), "1.0 KiB"),
                ((1536,), "1.5 KiB"),
            ),
        ),
        T(
            "kebab_case",
            "def kebab_case(text):\n"
            '    """Convert camelCase, snake_case, or words to kebab-case."""\n'
            "    chars = []\n"
            "    for i, ch in enumerate(str(text)):\n"
            "        if ch.isupper() and i:\n"
            "            chars.append('-')\n"
            "        chars.append(ch.lower() if ch not in (' ', '_') else '-')\n"
            "    out = ''.join(chars)\n"
            "    while '--' in out:\n"
            "        out = out.replace('--', '-')\n"
            "    return out.strip('-')\n",
            lambda low: "kebab" in low and "snake" not in low,
            (
                (("hello world",), "hello-world"),
                (("helloWorld",), "hello-world"),
                (("a_b",), "a-b"),
            ),
        ),
        T(
            "strip_html",
            "def strip_html(text):\n"
            '    """Remove HTML/XML tags; leave text nodes concatenated."""\n'
            "    import re\n"
            "    return re.sub(r'<[^>]*>', '', str(text))\n",
            lambda low: (
                ("html" in low or "xml" in low)
                and ("strip" in low or "remove" in low or "tag" in low)
                and "encode" not in low
            ),
            (
                (("<b>hi</b>",), "hi"),
                (("a<br>b",), "ab"),
                (("",), ""),
            ),
        ),
        T(
            "cosine_similarity",
            "def cosine_similarity(a, b):\n"
            '    """Cosine similarity of two equal-length vectors. Zero vector -> 0.0."""\n'
            "    dot = 0.0\n"
            "    na = 0.0\n"
            "    nb = 0.0\n"
            "    for x, y in zip(a, b):\n"
            "        x = float(x)\n"
            "        y = float(y)\n"
            "        dot += x * y\n"
            "        na += x * x\n"
            "        nb += y * y\n"
            "    if na == 0.0 or nb == 0.0:\n"
            "        return 0.0\n"
            "    return dot / ((na ** 0.5) * (nb ** 0.5))\n",
            lambda low: "cosine" in low and "similarity" in low,
            (
                (([1.0, 0.0], [1.0, 0.0]), 1.0),
                (([1.0, 0.0], [0.0, 1.0]), 0.0),
                (([0.0, 0.0], [1.0, 0.0]), 0.0),
            ),
        ),
    ]
