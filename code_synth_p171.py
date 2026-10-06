"""Cycle 453: SemVer, Base32, CIDR, NFC, Jaro-Winkler, duration, EAN-13, Pearson, Shannon, word wrap.

Pack loads first so phrase gates beat broader string/decode hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "parse_semver",
            "def parse_semver(text):\n"
            '    """SemVer 2.0.0 core (major, minor, patch); pre-release/build ignored."""\n'
            "    import re\n"
            "    m = re.fullmatch(\n"
            "        r'v?(\\d+)\\.(\\d+)\\.(\\d+)(?:-[0-9A-Za-z.-]+)?(?:\\+[0-9A-Za-z.-]+)?',\n"
            "        str(text).strip(),\n"
            "    )\n"
            "    if not m:\n"
            "        return None\n"
            "    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))\n",
            lambda low: "semver" in low or "semantic version" in low,
            (
                (("1.2.3",), (1, 2, 3)),
                (("v2.0.0-rc.1+build",), (2, 0, 0)),
                (("1.2",), None),
            ),
        ),
        T(
            "base32_encode",
            "def base32_encode(data):\n"
            '    """RFC 4648 Base32 (alphabet A-Z2-7) with padding."""\n'
            "    import base64\n"
            "    raw = data.encode('utf-8') if isinstance(data, str) else bytes(data)\n"
            "    return base64.b32encode(raw).decode('ascii')\n",
            lambda low: "base32" in low and "decode" not in low,
            (
                (("foo",), "MZXW6==="),
                ((b"Hello",), "JBSWY3DP"),
            ),
        ),
        T(
            "ip_in_cidr",
            "def ip_in_cidr(ip, cidr):\n"
            '    """True if ip is inside a CIDR prefix (RFC 4632 / ipaddress)."""\n'
            "    import ipaddress\n"
            "    return ipaddress.ip_address(str(ip)) in ipaddress.ip_network(str(cidr), strict=False)\n",
            lambda low: "cidr" in low,
            (
                (("192.168.1.10", "192.168.1.0/24"), True),
                (("10.0.0.1", "192.168.1.0/24"), False),
                (("2001:db8::1", "2001:db8::/32"), True),
            ),
        ),
        T(
            "unicode_nfc",
            "def unicode_nfc(text):\n"
            '    """Unicode Normalization Form C (canonical composition)."""\n'
            "    import unicodedata\n"
            "    return unicodedata.normalize('NFC', str(text))\n",
            lambda low: (
                "nfc" in low
                or "unicode normal" in low
                or "normalize unicode" in low
            ),
            (
                (("e\u0301",), "\u00e9"),
                (("\u00e9",), "\u00e9"),
            ),
        ),
        T(
            "jaro_winkler",
            "def jaro_winkler(a, b, prefix_scale=0.1):\n"
            '    """Jaro-Winkler similarity in [0, 1] (Winkler 1990; prefix cap 4)."""\n'
            "    s, t = str(a), str(b)\n"
            "    if s == t:\n"
            "        return 1.0\n"
            "    len_s, len_t = len(s), len(t)\n"
            "    if not len_s or not len_t:\n"
            "        return 0.0\n"
            "    match_dist = max(len_s, len_t) // 2 - 1\n"
            "    s_m = [False] * len_s\n"
            "    t_m = [False] * len_t\n"
            "    matches = 0\n"
            "    for i in range(len_s):\n"
            "        start = max(0, i - match_dist)\n"
            "        end = min(i + match_dist + 1, len_t)\n"
            "        for j in range(start, end):\n"
            "            if t_m[j] or s[i] != t[j]:\n"
            "                continue\n"
            "            s_m[i] = t_m[j] = True\n"
            "            matches += 1\n"
            "            break\n"
            "    if not matches:\n"
            "        return 0.0\n"
            "    k = trans = 0\n"
            "    for i in range(len_s):\n"
            "        if not s_m[i]:\n"
            "            continue\n"
            "        while not t_m[k]:\n"
            "            k += 1\n"
            "        if s[i] != t[k]:\n"
            "            trans += 1\n"
            "        k += 1\n"
            "    trans /= 2\n"
            "    jaro = (matches / len_s + matches / len_t + (matches - trans) / matches) / 3\n"
            "    prefix = 0\n"
            "    for ca, cb in zip(s, t):\n"
            "        if ca != cb or prefix == 4:\n"
            "            break\n"
            "        prefix += 1\n"
            "    return round(jaro + prefix * prefix_scale * (1 - jaro), 6)\n",
            lambda low: "jaro" in low or "winkler" in low,
            (
                (("MARTHA", "MARHTA"), 0.961111),
                (("DIXON", "DICKSONX"), 0.813333),
                (("abc", "xyz"), 0.0),
            ),
        ),
        T(
            "humanize_duration",
            "def humanize_duration(seconds):\n"
            '    """Whole seconds as compact d/h/m/s text."""\n'
            "    s = int(seconds)\n"
            "    neg = s < 0\n"
            "    s = abs(s)\n"
            "    parts = []\n"
            "    for name, size in (('d', 86400), ('h', 3600), ('m', 60), ('s', 1)):\n"
            "        n, s = divmod(s, size)\n"
            "        if n:\n"
            "            parts.append(f'{n}{name}')\n"
            "    out = ' '.join(parts) or '0s'\n"
            "    return '-' + out if neg else out\n",
            lambda low: (
                "humanize duration" in low
                or "duration in seconds" in low
                or "seconds as human" in low
                or ("formats a duration" in low)
                or ("humanizes a duration" in low)
            ),
            (
                ((3661,), "1h 1m 1s"),
                ((90,), "1m 30s"),
                ((0,), "0s"),
            ),
        ),
        T(
            "ean13_valid",
            "def ean13_valid(code):\n"
            '    """GS1 EAN-13 mod-10 check digit (weights 1,3 from the left)."""\n'
            "    d = ''.join(ch for ch in str(code) if ch.isdigit())\n"
            "    if len(d) != 13:\n"
            "        return False\n"
            "    total = 0\n"
            "    for i, ch in enumerate(d[:12]):\n"
            "        n = int(ch)\n"
            "        total += n * (1 if i % 2 == 0 else 3)\n"
            "    check = (10 - (total % 10)) % 10\n"
            "    return check == int(d[12])\n",
            lambda low: "ean-13" in low or "ean13" in low or "ean 13" in low,
            (
                (("4006381333931",), True),
                (("4006381333932",), False),
                (("4006 3813 3393 1",), True),
            ),
        ),
        T(
            "pearson",
            "def pearson(xs, ys):\n"
            '    """Pearson product-moment correlation of two equal numeric series."""\n'
            "    xs = [float(x) for x in xs]\n"
            "    ys = [float(y) for y in ys]\n"
            "    n = len(xs)\n"
            "    if n != len(ys) or n < 2:\n"
            "        raise ValueError('need two equal series of length >= 2')\n"
            "    mx = sum(xs) / n\n"
            "    my = sum(ys) / n\n"
            "    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))\n"
            "    dx = sum((x - mx) ** 2 for x in xs) ** 0.5\n"
            "    dy = sum((y - my) ** 2 for y in ys) ** 0.5\n"
            "    if dx == 0.0 or dy == 0.0:\n"
            "        return 0.0\n"
            "    return round(num / (dx * dy), 10)\n",
            lambda low: "pearson" in low,
            (
                (([1, 2, 3], [1, 2, 3]), 1.0),
                (([1, 2, 3], [3, 2, 1]), -1.0),
            ),
        ),
        T(
            "shannon_entropy",
            "def shannon_entropy(text):\n"
            '    """Shannon entropy (bits) of the empirical character distribution."""\n'
            "    import math\n"
            "    from collections import Counter\n"
            "    s = str(text)\n"
            "    if not s:\n"
            "        return 0.0\n"
            "    n = len(s)\n"
            "    h = 0.0\n"
            "    for c in Counter(s).values():\n"
            "        p = c / n\n"
            "        h -= p * math.log2(p)\n"
            "    return h\n",
            lambda low: "shannon" in low or "entropy of a string" in low or "entropy of text" in low,
            (
                (("aaaa",), 0.0),
                (("ab",), 1.0),
                (("",), 0.0),
            ),
        ),
        T(
            "word_wrap",
            "def word_wrap(text, width):\n"
            '    """Wrap text to width on whitespace boundaries."""\n'
            "    import textwrap\n"
            "    return '\\n'.join(textwrap.wrap(str(text), width=int(width)))\n",
            lambda low: (
                ("word wrap" in low or "wraps text" in low or "wrap text" in low or "text wrap" in low)
                and "unwrap" not in low
            ),
            (
                (("hello world", 5), "hello\nworld"),
                (("a b c", 3), "a b\nc"),
            ),
        ),
    ]
