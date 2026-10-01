"""Cycle 352: unmatched Easy — string value, adjacent parity swap,
OR trailing zeros, index/value indices, distinct-count square sum,
longest monotonic subarray."""

from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "maximum_value_string",
            "def maximum_value(strs):\n"
            '    """Max value of strings: int if all digits else length (LeetCode 2496)."""\n'
            "    best = 0\n"
            "    for s in strs:\n"
            "        val = int(s) if s.isdigit() else len(s)\n"
            "        if val > best:\n"
            "            best = val\n"
            "    return best\n",
            lambda low: "value of a string" in low or (
                "maximum value" in low and "string" in low and "array" in low
            ),
            (
                ((["alic3", "bob", "3", "4", "00000"],), 5),
                ((["1", "01", "001", "0001"],), 1),
                ((["abc", "ab"],), 3),
            ),
        ),
        T(
            "smallest_string_after_swap",
            "def get_smallest_string(s):\n"
            '    """One adjacent different-parity digit swap if it decreases (LeetCode 3216)."""\n'
            "    chars = list(s)\n"
            "    for i in range(len(chars) - 1):\n"
            "        a, b = chars[i], chars[i + 1]\n"
            "        if a > b and (ord(a) - ord(b)) % 2 == 0:\n"
            "            chars[i], chars[i + 1] = b, a\n"
            "            break\n"
            "    return ''.join(chars)\n",
            lambda low: "after a swap" in low or (
                "lexicographically smallest" in low and "string" in low
            ),
            (
                (("45320",), "43520"),
                (("001",), "001"),
                (("10",), "10"),
            ),
        ),
        T(
            "has_trailing_zeros",
            "def has_trailing_zeros(nums):\n"
            '    """True if bitwise OR of some pair has a trailing zero (LeetCode 2980)."""\n'
            "    even = 0\n"
            "    for n in nums:\n"
            "        if n % 2 == 0:\n"
            "            even += 1\n"
            "            if even >= 2:\n"
            "                return True\n"
            "    return False\n",
            lambda low: "trailing zeros" in low and ("bitwise" in low or " or " in low),
            (
                (([1, 2, 3, 4],), True),
                (([1, 3, 5],), False),
                (([2, 4, 8],), True),
            ),
        ),
        T(
            "find_indices_diff",
            "def find_indices(nums, index_difference, value_difference):\n"
            '    """Indices with index and value gaps (LeetCode 2903)."""\n'
            "    n = len(nums)\n"
            "    for i in range(n):\n"
            "        j = i + index_difference\n"
            "        while j < n:\n"
            "            if abs(nums[i] - nums[j]) >= value_difference:\n"
            "                return [i, j]\n"
            "            j += 1\n"
            "    return [-1, -1]\n",
            lambda low: "index and value difference" in low or (
                "indexdifference" in low.replace(" ", "")
            ),
            (
                (([5, 1, 4, 1], 2, 4), [0, 3]),
                (([2, 1], 0, 0), [0, 0]),
                (([1, 2, 3], 2, 4), [-1, -1]),
            ),
        ),
        T(
            "sum_counts_distinct_sq",
            "def sum_counts(nums):\n"
            '    """Sum of squared distinct counts over subarrays (LeetCode 2913)."""\n'
            "    n = len(nums)\n"
            "    total = 0\n"
            "    for i in range(n):\n"
            "        seen = set()\n"
            "        for j in range(i, n):\n"
            "            seen.add(nums[j])\n"
            "            d = len(seen)\n"
            "            total += d * d\n"
            "    return total\n",
            lambda low: "distinct element sum of squares" in low or (
                "sum of squares" in low and "distinct" in low and "subarray" in low
            ),
            (
                (([1, 2, 1],), 15),
                (([1, 1],), 3),
                (([2],), 1),
            ),
        ),
        T(
            "longest_monotonic_subarray",
            "def longest_monotonic_subarray(nums):\n"
            '    """Longest strictly increasing or decreasing run (LeetCode 3105)."""\n'
            "    best = 1\n"
            "    inc = 1\n"
            "    dec = 1\n"
            "    for i in range(1, len(nums)):\n"
            "        if nums[i] > nums[i - 1]:\n"
            "            inc += 1\n"
            "            dec = 1\n"
            "        elif nums[i] < nums[i - 1]:\n"
            "            dec += 1\n"
            "            inc = 1\n"
            "        else:\n"
            "            inc = 1\n"
            "            dec = 1\n"
            "        if inc > best:\n"
            "            best = inc\n"
            "        if dec > best:\n"
            "            best = dec\n"
            "    return best\n",
            lambda low: "monotonic" in low or (
                "strictly increasing" in low and "strictly decreasing" in low
            ),
            (
                (([1, 4, 3, 3, 2],), 2),
                (([3, 3, 3, 3],), 1),
                (([3, 2, 1],), 3),
            ),
        ),
    ]
