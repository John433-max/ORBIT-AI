"""Cycle 364: unmatched Easy string/array templates.

Official problem statements (algorithms only, not copied text):
LeetCode 3561, 3591, 3612, 3622, 3637, 3668.
"""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "resulting_string_after_adjacent_removals",
            "def resulting_string_after_adjacent_removals(s):\n"
            '    """Drop leftmost adjacent alphabet-consecutive pairs, a/z circular (LeetCode 3561)."""\n'
            "    stack = []\n"
            "    for ch in s:\n"
            "        if stack and abs(ord(stack[-1]) - ord(ch)) in (1, 25):\n"
            "            stack.pop()\n"
            "        else:\n"
            "            stack.append(ch)\n"
            "    return ''.join(stack)\n"
            "\n"
            "def resulting_string(s):\n"
            "    return resulting_string_after_adjacent_removals(s)\n",
            lambda low: bool(
                re.search(
                    r"\badjacent removals\b|"
                    r"\bleetcode 3561\b",
                    low,
                )
            ),
            (
                (("abc",), "c"),
                (("adcb",), ""),
                (("zadb",), "db"),
            ),
        ),
        T(
            "has_prime_frequency",
            "def has_prime_frequency(nums):\n"
            '    """True if any value occurs a prime number of times (LeetCode 3591)."""\n'
            "    counts = {}\n"
            "    for x in nums:\n"
            "        counts[x] = counts.get(x, 0) + 1\n"
            "\n"
            "    def _prime(n):\n"
            "        if n < 2:\n"
            "            return False\n"
            "        d = 2\n"
            "        while d * d <= n:\n"
            "            if n % d == 0:\n"
            "                return False\n"
            "            d += 1\n"
            "        return True\n"
            "\n"
            "    return any(_prime(c) for c in counts.values())\n"
            "\n"
            "def check_prime_frequency(nums):\n"
            "    return has_prime_frequency(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bprime frequency\b|"
                    r"\bleetcode 3591\b",
                    low,
                )
            ),
            (
                (((1, 2, 3, 4, 5, 4),), True),
                (((1, 2, 3, 4, 5),), False),
                (((2, 2, 2, 4, 4),), True),
            ),
        ),
        T(
            "process_string_special_operations",
            "def process_string_special_operations(s):\n"
            '    """Append letters; * pops, # duplicates, % reverses (LeetCode 3612)."""\n'
            "    out = []\n"
            "    for ch in s:\n"
            "        if ch == '*':\n"
            "            if out:\n"
            "                out.pop()\n"
            "        elif ch == '#':\n"
            "            out.extend(out)\n"
            "        elif ch == '%':\n"
            "            out.reverse()\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n"
            "\n"
            "def process_str(s):\n"
            "    return process_string_special_operations(s)\n",
            lambda low: bool(
                re.search(
                    r"\bspecial operations\b|"
                    r"\bleetcode 3612\b",
                    low,
                )
                and not re.search(r"\bii\b|\bleetcode 3613\b", low)
            ),
            (
                (("a#b%*",), "ba"),
                (("z*#",), ""),
                (("abc",), "abc"),
            ),
        ),
        T(
            "check_divisibility_digit_sum_product",
            "def check_divisibility_digit_sum_product(n):\n"
            '    """n divisible by digit-sum plus digit-product (LeetCode 3622)."""\n'
            "    s = 0\n"
            "    p = 1\n"
            "    x = n\n"
            "    while x:\n"
            "        x, v = divmod(x, 10)\n"
            "        s += v\n"
            "        p *= v\n"
            "    total = s + p\n"
            "    return total != 0 and n % total == 0\n"
            "\n"
            "def check_divisibility(n):\n"
            "    return check_divisibility_digit_sum_product(n)\n",
            lambda low: bool(
                re.search(
                    r"\bdigit sum and product\b|"
                    r"\bleetcode 3622\b",
                    low,
                )
            ),
            (
                ((99,), True),
                ((23,), False),
                ((1,), False),
            ),
        ),
        T(
            "is_trionic",
            "def is_trionic(nums):\n"
            '    """Strict increase, then decrease, then increase (LeetCode 3637)."""\n'
            "    n = len(nums)\n"
            "    p = 0\n"
            "    while p < n - 2 and nums[p] < nums[p + 1]:\n"
            "        p += 1\n"
            "    if p == 0:\n"
            "        return False\n"
            "    q = p\n"
            "    while q < n - 1 and nums[q] > nums[q + 1]:\n"
            "        q += 1\n"
            "    if q == p or q == n - 1:\n"
            "        return False\n"
            "    while q < n - 1 and nums[q] < nums[q + 1]:\n"
            "        q += 1\n"
            "    return q == n - 1\n"
            "\n"
            "def trionic_array(nums):\n"
            "    return is_trionic(nums)\n",
            lambda low: bool(
                re.search(
                    r"\btrionic\b|"
                    r"\bleetcode 3637\b",
                    low,
                )
            ),
            (
                (((1, 3, 5, 4, 2, 6),), True),
                (((2, 1, 3),), False),
                (((1, 2, 3, 2, 1, 2),), True),
            ),
        ),
        T(
            "restore_finishing_order",
            "def restore_finishing_order(order, friends):\n"
            '    """Friends in race finishing order (LeetCode 3668)."""\n'
            "    wanted = set(friends)\n"
            "    return [x for x in order if x in wanted]\n"
            "\n"
            "def recover_order(order, friends):\n"
            "    return restore_finishing_order(order, friends)\n",
            lambda low: bool(
                re.search(
                    r"\bfinishing order\b|"
                    r"\bleetcode 3668\b",
                    low,
                )
            ),
            (
                (((3, 1, 2, 5, 4), (1, 3, 4)), [3, 1, 4]),
                (((1, 4, 5, 3, 2), (2, 5)), [5, 2]),
                (((1, 2, 3), (2,)), [2]),
            ),
        ),
    ]
