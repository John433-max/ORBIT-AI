"""Cycle 263: additional verified Python templates (pack 6)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "single_number_ii",
            "def single_number_ii(nums):\n"
            '    """Element that appears once; every other value appears three times."""\n'
            "    ones = twos = 0\n"
            "    for x in nums:\n"
            "        x = int(x)\n"
            "        ones = (ones ^ x) & ~twos\n"
            "        twos = (twos ^ x) & ~ones\n"
            "    return ones\n",
            lambda low: bool(
                re.search(
                    r"\bsingle[- ]?number\s*(ii|2)\b|"
                    r"\bsingle_number_ii\b|"
                    r"\bappears once.{0,40}three times\b|"
                    r"\bthree times.{0,40}appears once\b",
                    low,
                )
            ),
            ((([2, 2, 3, 2],), 3), (([0, 1, 0, 1, 0, 1, 99],), 99)),
        ),
        T(
            "hamming_weight",
            "def hamming_weight(n):\n"
            '    """Number of 1-bits in the binary representation of n."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        n &= (1 << 32) - 1\n"
            "    c = 0\n"
            "    while n:\n"
            "        n &= n - 1\n"
            "        c += 1\n"
            "    return c\n",
            lambda low: bool(
                re.search(
                    r"\bhamming[- ]?weight\b|"
                    r"\bnumber of 1[- ]?bits\b|"
                    r"\bnumber of one bits\b|"
                    r"\bcount(?:ing)? (?:set )?bits\b|"
                    r"\bpopcount\b|"
                    r"\bhamming_weight\b",
                    low,
                )
            ),
            (((11,), 3), ((128,), 1), ((0,), 0)),
        ),
        T(
            "reverse_bits",
            "def reverse_bits(n, width=32):\n"
            '    """Reverse the binary bits of n in a fixed width (default 32)."""\n'
            "    n = int(n)\n"
            "    width = int(width)\n"
            "    out = 0\n"
            "    for _ in range(width):\n"
            "        out = (out << 1) | (n & 1)\n"
            "        n >>= 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\breverse bits\b|"
                    r"\breverse the bits\b|"
                    r"\breverse_bits\b|"
                    r"\bbit revers(?:e|al)\b",
                    low,
                )
            ),
            (((1, 8), 128), ((43261596, 32), 964176192)),
        ),
        T(
            "is_power_of_four",
            "def is_power_of_four(n):\n"
            '    """Return True if n is a positive power of four."""\n'
            "    n = int(n)\n"
            "    if n <= 0 or (n & (n - 1)) != 0:\n"
            "        return False\n"
            "    return (n & 0x55555555) != 0\n",
            lambda low: bool(
                re.search(
                    r"\bpower of four\b|"
                    r"\bpower of 4\b|"
                    r"\bpower-of-four\b|"
                    r"\bis_power_of_four\b",
                    low,
                )
            ),
            (((1,), True), ((4,), True), ((16,), True), ((8,), False), ((0,), False)),
        ),
        T(
            "valid_mountain_array",
            "def valid_mountain_array(arr):\n"
            '    """True if arr strictly increases then strictly decreases."""\n'
            "    arr = list(arr)\n"
            "    n = len(arr)\n"
            "    if n < 3:\n"
            "        return False\n"
            "    i = 0\n"
            "    while i + 1 < n and arr[i] < arr[i + 1]:\n"
            "        i += 1\n"
            "    if i == 0 or i == n - 1:\n"
            "        return False\n"
            "    while i + 1 < n and arr[i] > arr[i + 1]:\n"
            "        i += 1\n"
            "    return i == n - 1\n",
            lambda low: (
                bool(
                    re.search(
                        r"\bvalid mountain\b|"
                        r"\bvalid_mountain_array\b|"
                        r"\bchecks? a valid mountain array\b",
                        low,
                    )
                )
                and not re.search(r"\bpeak index\b|\bpeak_index\b", low)
            ),
            ((([2, 1],), False), (([3, 5, 5],), False), (([0, 3, 2, 1],), True)),
        ),
        T(
            "summary_ranges",
            "def summary_ranges(nums):\n"
            '    """Compact sorted unique ints into inclusive range strings."""\n'
            "    nums = list(nums)\n"
            "    if not nums:\n"
            "        return []\n"
            "    out = []\n"
            "    start = prev = int(nums[0])\n"
            "    for x in nums[1:]:\n"
            "        x = int(x)\n"
            "        if x == prev + 1:\n"
            "            prev = x\n"
            "            continue\n"
            "        out.append(str(start) if start == prev else f'{start}->{prev}')\n"
            "        start = prev = x\n"
            "    out.append(str(start) if start == prev else f'{start}->{prev}')\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsummary ranges\b|"
                    r"\bsummary_ranges\b|"
                    r"\brange summar(?:y|ies)\b|"
                    r"\bcompact ranges\b",
                    low,
                )
            ),
            (
                (([0, 1, 2, 4, 5, 7],), ["0->2", "4->5", "7"]),
                (([0, 2, 3, 4, 6, 8, 9],), ["0", "2->4", "6", "8->9"]),
            ),
        ),
    ]
