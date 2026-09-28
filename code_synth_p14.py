"""Cycle 271: additional verified Python templates (pack 14)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "defang_ip_addr",
            "def defang_ip_addr(address):\n"
            '    """Replace every \'.\' in an IPv4 address with \'[.]\'."""\n'
            "    return str(address).replace('.', '[.]')\n",
            lambda low: bool(
                re.search(
                    r"\bdefang|"
                    r"\bdefang_ip_addr\b",
                    low,
                )
            ),
            ((("1.1.1.1",), "1[.]1[.]1[.]1"), (("255.100.50.0",), "255[.]100[.]50[.]0")),
        ),
        T(
            "subtract_product_and_sum",
            "def subtract_product_and_sum(n):\n"
            '    """Product of digits minus sum of digits of n."""\n'
            "    n = abs(int(n))\n"
            "    prod, s = 1, 0\n"
            "    if n == 0:\n"
            "        return -0\n"
            "    while n:\n"
            "        d = n % 10\n"
            "        prod *= d\n"
            "        s += d\n"
            "        n //= 10\n"
            "    return prod - s\n",
            lambda low: bool(
                re.search(
                    r"\bsubtract (?:the )?product and sum\b|"
                    r"\bsubtract_product_and_sum\b|"
                    r"\bproduct of digits minus (?:the )?sum\b|"
                    r"\bsubtract product and sum of digits\b",
                    low,
                )
            ),
            (((234,), 15), ((4421,), 21)),
        ),
        T(
            "decompress_rl_elist",
            "def decompress_rl_elist(nums):\n"
            '    """Decompress run-length list [freq, val, freq, val, ...]."""\n'
            "    a = list(nums)\n"
            "    out = []\n"
            "    for i in range(0, len(a), 2):\n"
            "        out.extend([a[i + 1]] * int(a[i]))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdecompress (?:run[- ]length )?(?:encoded )?list\b|"
                    r"\bdecompress_rl_elist\b|"
                    r"\brun[- ]length (?:encoded )?list\b",
                    low,
                )
            ),
            (([[1, 2, 3, 4],], [2, 4, 4, 4]), ([[1, 1, 2, 3],], [1, 3, 3])),
        ),
        T(
            "replace_elements",
            "def replace_elements(arr):\n"
            '    """Replace each element with the greatest element to its right; last becomes -1."""\n'
            "    a = [int(x) for x in arr]\n"
            "    best = -1\n"
            "    for i in range(len(a) - 1, -1, -1):\n"
            "        cur = a[i]\n"
            "        a[i] = best\n"
            "        if cur > best:\n"
            "            best = cur\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\breplace elements? with (?:the )?greatest\b|"
                    r"\breplace_elements\b|"
                    r"\bgreatest element on (?:the )?right\b",
                    low,
                )
            ),
            (([[17, 18, 5, 4, 6, 1],], [18, 6, 6, 6, 1, -1]), ([[400],], [-1])),
        ),
        T(
            "find_numbers",
            "def find_numbers(nums):\n"
            '    """Count how many numbers have an even number of digits."""\n'
            "    return sum(1 for x in nums if len(str(abs(int(x)))) % 2 == 0)\n",
            lambda low: bool(
                re.search(
                    r"\bfind numbers with even number of digits\b|"
                    r"\beven number of digits\b|"
                    r"\bfind_numbers\b",
                    low,
                )
            )
            and "even number is" not in low,
            (([[12, 345, 2, 6, 7896],], 2), ([[555, 901, 482, 1771],], 1)),
        ),
        T(
            "smaller_numbers_than_current",
            "def smaller_numbers_than_current(nums):\n"
            '    """For each value, count how many numbers are strictly smaller."""\n'
            "    a = [int(x) for x in nums]\n"
            "    order = sorted(a)\n"
            "    first = {}\n"
            "    for i, v in enumerate(order):\n"
            "        if v not in first:\n"
            "            first[v] = i\n"
            "    return [first[v] for v in a]\n",
            lambda low: bool(
                re.search(
                    r"\bhow many numbers (?:are )?smaller than (?:the )?current\b|"
                    r"\bsmaller_numbers_than_current\b|"
                    r"\bsmaller than current number\b",
                    low,
                )
            ),
            (([[8, 1, 2, 2, 3],], [4, 0, 1, 1, 3]), ([[6, 5, 4, 8],], [2, 1, 0, 3])),
        ),
    ]
