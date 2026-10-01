"""Cycle 353: unmatched Easy — same-color chessboards, increasing
difference, collect-1..k ops, categorize box, digit-count value,
k-distant indices."""

from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "check_two_chessboards",
            "def check_two_chessboards(coordinate1, coordinate2):\n"
            '    """True if two chessboard squares share a color (LeetCode 3274)."""\n'
            "    def color(c):\n"
            "        return (ord(c[0]) - ord('a') + int(c[1:])) % 2\n"
            "    return color(coordinate1) == color(coordinate2)\n",
            lambda low: "chessboards" in low and "same color" in low,
            (
                (("a1", "c3"), True),
                (("a1", "h3"), False),
                (("h8", "a1"), True),
            ),
        ),
        T(
            "maximum_increasing_difference",
            "def maximum_difference(nums):\n"
            '    """Max nums[j]-nums[i] for i<j and nums[i]<nums[j], else -1 (LeetCode 2016)."""\n'
            "    best = -1\n"
            "    mn = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        if x > mn:\n"
            "            best = max(best, x - mn)\n"
            "        elif x < mn:\n"
            "            mn = x\n"
            "    return best\n",
            lambda low: "increasing elements" in low and "difference" in low,
            (
                (([7, 1, 5, 4],), 4),
                (([9, 4, 3, 2],), -1),
                (([1, 5, 2, 10],), 9),
            ),
        ),
        T(
            "min_operations_collect_elements",
            "def min_operations(nums, k):\n"
            '    """Ops removing from the end until 1..k are collected (LeetCode 2869)."""\n'
            "    need = set(range(1, k + 1))\n"
            "    seen = set()\n"
            "    for i in range(len(nums) - 1, -1, -1):\n"
            "        if nums[i] in need:\n"
            "            seen.add(nums[i])\n"
            "            if len(seen) == len(need):\n"
            "                return len(nums) - i\n"
            "    return len(nums)\n",
            lambda low: "collect elements" in low,
            (
                (([3, 1, 5, 4, 2], 2), 4),
                (([3, 1, 5, 4, 2], 5), 5),
                (([1, 2, 3], 2), 3),
            ),
        ),
        T(
            "categorize_box",
            "def categorize_box(length, width, height, mass):\n"
            '    """Bulky/Heavy/Both/Neither by size and mass (LeetCode 2525)."""\n'
            "    bulky = (\n"
            "        length >= 10000 or width >= 10000 or height >= 10000\n"
            "        or length * width * height >= 10 ** 9\n"
            "    )\n"
            "    heavy = mass >= 100\n"
            "    if bulky and heavy:\n"
            "        return 'Both'\n"
            "    if bulky:\n"
            "        return 'Bulky'\n"
            "    if heavy:\n"
            "        return 'Heavy'\n"
            "    return 'Neither'\n",
            lambda low: "categorize box" in low or ("box" in low and "criteria" in low),
            (
                ((1000, 35, 700, 300), "Heavy"),
                ((200, 50, 800, 50), "Neither"),
                ((10000, 1, 1, 100), "Both"),
            ),
        ),
        T(
            "digit_count_value",
            "def digit_count(num):\n"
            '    """True if num[i] equals the count of digit i (LeetCode 2283)."""\n'
            "    for i, ch in enumerate(num):\n"
            "        if num.count(str(i)) != int(ch):\n"
            "            return False\n"
            "    return True\n",
            lambda low: "equal digit count" in low or (
                "digit count" in low and "digit value" in low
            ),
            (
                (("1210",), True),
                (("030",), False),
                (("1",), False),
            ),
        ),
        T(
            "find_k_distant_indices",
            "def find_k_distant_indices(nums, key, k):\n"
            '    """Indices within k of some index holding key (LeetCode 2200)."""\n'
            "    n = len(nums)\n"
            "    out = []\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            if nums[j] == key and abs(i - j) <= k:\n"
            "                out.append(i)\n"
            "                break\n"
            "    return out\n",
            lambda low: "k-distant" in low or "k distant" in low,
            (
                (([3, 4, 9, 1, 3, 9, 5], 9, 1), [1, 2, 3, 4, 5, 6]),
                (([2, 2, 2, 2, 2], 2, 2), [0, 1, 2, 3, 4]),
                (([1, 2, 3], 2, 0), [1]),
            ),
        ),
    ]
