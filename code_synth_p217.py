"""Cycle 501: unmatched write-a-function asks.

LeetCode 1437 / 1461 / 93 / 1657 / 1492 / 1909. Matchers stay off
decimal conversion, unique-occurrence, and generic factor lists.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "k_length_apart",
            "def k_length_apart(nums, k):\n"
            '    """True when every pair of 1s has more than k indices between them."""\n'
            "    last = None\n"
            "    for i, value in enumerate(nums):\n"
            "        if int(value) != 1:\n"
            "            continue\n"
            "        if last is not None and i - last - 1 < int(k):\n"
            "            return False\n"
            "        last = i\n"
            "    return True\n",
            lambda low: (
                ("1" in low or "ones" in low or "one" in low)
                and "apart" in low
                and ("binary" in low or "array" in low or "distance" in low)
                and "hamming" not in low
            ),
            (
                (([1, 0, 0, 0, 1, 0, 0, 1], 2), True),
                (([1, 0, 0, 1, 0, 1], 2), False),
                (([1, 0, 0, 1], 1), True),
            ),
        ),
        T(
            "has_all_codes",
            "def has_all_codes(s, k):\n"
            '    """True when s contains every binary code of length k as a substring."""\n'
            "    s = str(s)\n"
            "    k = int(k)\n"
            "    if k <= 0 or len(s) < k:\n"
            "        return False\n"
            "    need = 1 << k\n"
            "    seen = set()\n"
            "    for i in range(len(s) - k + 1):\n"
            "        seen.add(s[i:i + k])\n"
            "        if len(seen) == need:\n"
            "            return True\n"
            "    return False\n",
            lambda low: (
                "binary" in low
                and ("all codes" in low or "binary codes" in low or "every binary" in low)
                and "decimal" not in low
                and "convert" not in low
            ),
            (
                (("00110110", 2), True),
                (("0110", 2), False),
                (("0110", 1), True),
            ),
        ),
        T(
            "restore_ip_addresses",
            "def restore_ip_addresses(s):\n"
            '    """All valid IPv4 restorations of a digit string (LeetCode 93)."""\n'
            "    s = str(s)\n"
            "    out = []\n"
            "\n"
            "    def ok(part):\n"
            "        if not part or len(part) > 3:\n"
            "            return False\n"
            "        if len(part) > 1 and part[0] == '0':\n"
            "            return False\n"
            "        return int(part) <= 255\n"
            "\n"
            "    n = len(s)\n"
            "    for a in range(1, 4):\n"
            "        for b in range(1, 4):\n"
            "            for c in range(1, 4):\n"
            "                d = n - a - b - c\n"
            "                if d < 1 or d > 3:\n"
            "                    continue\n"
            "                parts = [s[0:a], s[a:a + b], s[a + b:a + b + c], s[a + b + c:]]\n"
            "                if all(ok(part) for part in parts):\n"
            "                    out.append('.'.join(parts))\n"
            "    return out\n",
            lambda low: (
                ("restore" in low or "ip addresses" in low or "ipv4 addresses" in low)
                and "flip" not in low
                and "valid ipv4" not in low
                and "is a valid" not in low
            ),
            (
                (("25525511135",), ["255.255.11.135", "255.255.111.35"]),
                (("0000",), ["0.0.0.0"]),
                (("101023",), ["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"]),
            ),
        ),
        T(
            "close_strings",
            "def close_strings(word1, word2):\n"
            '    """True when two strings can be made equal by the close-string operations."""\n'
            "    if len(word1) != len(word2):\n"
            "        return False\n"
            "    from collections import Counter\n"
            "    c1, c2 = Counter(word1), Counter(word2)\n"
            "    if set(c1) != set(c2):\n"
            "        return False\n"
            "    return sorted(c1.values()) == sorted(c2.values())\n",
            lambda low: (
                "close" in low
                and "string" in low
                and "closest" not in low
                and "closed" not in low
            ),
            (
                (("abc", "bca"), True),
                (("a", "aa"), False),
                (("cabbba", "abbccc"), True),
            ),
        ),
        T(
            "kth_factor",
            "def kth_factor(n, k):\n"
            '    """The k-th factor of n, or -1 if fewer than k factors exist."""\n'
            "    n, k = int(n), int(k)\n"
            "    if k <= 0:\n"
            "        return -1\n"
            "    small = []\n"
            "    large = []\n"
            "    i = 1\n"
            "    while i * i <= n:\n"
            "        if n % i == 0:\n"
            "            small.append(i)\n"
            "            if i != n // i:\n"
            "                large.append(n // i)\n"
            "        i += 1\n"
            "    factors = small + large[::-1]\n"
            "    if k > len(factors):\n"
            "        return -1\n"
            "    return factors[k - 1]\n",
            lambda low: (
                "kth" in low
                and "factor" in low
                and "factorial" not in low
                and "prime" not in low
            ),
            (
                ((12, 3), 3),
                ((7, 2), 7),
                ((4, 4), -1),
            ),
        ),
        T(
            "can_be_increasing",
            "def can_be_increasing(nums):\n"
            '    """True if removing at most one element makes nums strictly increasing."""\n'
            "    def ok(arr):\n"
            "        return all(arr[i] < arr[i + 1] for i in range(len(arr) - 1))\n"
            "\n"
            "    if ok(nums):\n"
            "        return True\n"
            "    for i in range(len(nums)):\n"
            "        if ok(nums[:i] + nums[i + 1:]):\n"
            "            return True\n"
            "    return False\n",
            lambda low: (
                "increasing" in low
                and ("remov" in low or "delet" in low)
                and ("one" in low or "single" in low or "at most" in low)
                and "subsequence" not in low
                and "continuous" not in low
            ),
            (
                (([1, 2, 10, 5, 7],), True),
                (([2, 3, 1, 2],), False),
                (([1, 1, 1],), False),
            ),
        ),
    ]
