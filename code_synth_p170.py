"""Cycle 452: HMAC-SHA256, IBAN, percent-encode, UUID, digital root, ellipsize, Gray code.

Pack loads before p169 so phrase gates beat broader hash/string hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "hmac_sha256_hex",
            "def hmac_sha256_hex(key, message):\n"
            '    """RFC 2104 / FIPS 198-1 HMAC-SHA-256 as lowercase hex."""\n'
            "    import hashlib\n"
            "    import hmac\n"
            "    def _b(v):\n"
            "        return v.encode('utf-8') if isinstance(v, str) else bytes(v)\n"
            "    return hmac.new(_b(key), _b(message), hashlib.sha256).hexdigest()\n",
            lambda low: (
                "hmac" in low
                and ("sha256" in low or "sha-256" in low or "sha 256" in low)
            ),
            (
                (("key", "The quick brown fox jumps over the lazy dog"),
                 "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"),
                ((bytes.fromhex("0b" * 20), b"Hi There"),
                 "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"),
            ),
        ),
        T(
            "iban_valid",
            "def iban_valid(iban):\n"
            '    """ISO 13616 IBAN check: rearrange, expand letters, mod 97 == 1."""\n'
            "    t = ''.join(ch for ch in str(iban).upper() if ch.isalnum())\n"
            "    if len(t) < 5:\n"
            "        return False\n"
            "    t = t[4:] + t[:4]\n"
            "    n = ''\n"
            "    for ch in t:\n"
            "        if ch.isalpha():\n"
            "            n += str(ord(ch) - 55)\n"
            "        elif ch.isdigit():\n"
            "            n += ch\n"
            "        else:\n"
            "            return False\n"
            "    return int(n) % 97 == 1\n",
            lambda low: "iban" in low,
            (
                (("GB82WEST12345698765432",), True),
                (("GB82 WEST 1234 5698 7654 32",), True),
                (("GB82WEST12345698765433",), False),
            ),
        ),
        T(
            "percent_encode",
            "def percent_encode(text, safe='/'):\n"
            '    """RFC 3986 percent-encoding via urllib.parse.quote."""\n'
            "    from urllib.parse import quote\n"
            "    return quote(str(text), safe=safe)\n",
            lambda low: (
                ("percent-encode" in low or "percent encode" in low or "percent_encode" in low)
                or ("url quote" in low)
            ),
            (
                (("a b/c",), "a%20b/c"),
                (("a b/c", ""), "a%20b%2Fc"),
            ),
        ),
        T(
            "is_uuid",
            "def is_uuid(text):\n"
            '    """RFC 4122 UUID textual form (8-4-4-4-12 hex)."""\n'
            "    import re\n"
            "    return bool(re.fullmatch(\n"
            "        r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',\n"
            "        str(text).strip(),\n"
            "    ))\n",
            lambda low: "uuid" in low and "valid" in low,
            (
                (("550e8400-e29b-41d4-a716-446655440000",), True),
                (("not-a-uuid",), False),
                (("550e8400e29b41d4a716446655440000",), False),
            ),
        ),
        T(
            "digital_root",
            "def digital_root(n):\n"
            '    """Repeated digit sum. For n>=0 equals 0 if n==0 else 1+(n-1)%9."""\n'
            "    n = abs(int(n))\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    return 1 + (n - 1) % 9\n",
            lambda low: ("digital root" in low or "digital_root" in low)
            and "add digits" not in low
            and "add_digits" not in low,
            (
                ((942,), 6),
                ((0,), 0),
                ((9,), 9),
            ),
        ),
        T(
            "ellipsize",
            "def ellipsize(text, limit):\n"
            '    """Truncate to limit characters, using an ellipsis when shortened."""\n'
            "    s = str(text)\n"
            "    limit = int(limit)\n"
            "    if limit < 0:\n"
            "        limit = 0\n"
            "    if len(s) <= limit:\n"
            "        return s\n"
            "    if limit <= 3:\n"
            "        return s[:limit]\n"
            "    return s[:limit - 3] + '...'\n",
            lambda low: "ellipsize" in low or "ellipsis" in low,
            (
                (("hello world", 8), "hello..."),
                (("hi", 8), "hi"),
                (("abcdef", 2), "ab"),
            ),
        ),
        T(
            "gray_code",
            "def gray_code(n):\n"
            '    """Binary-reflected Gray code: n XOR (n >> 1)."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        raise ValueError('n must be non-negative')\n"
            "    return n ^ (n >> 1)\n",
            lambda low: "gray code" in low or "gray_code" in low or "grey code" in low,
            (
                ((0,), 0),
                ((1,), 1),
                ((4,), 6),
                ((7,), 4),
            ),
        ),
    ]
