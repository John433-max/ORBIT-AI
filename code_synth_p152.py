"""Cycle 406: product of three, tree cameras, numeric string, fixed point, index pairs, powers of three.

Unmatched fallbacks on the local coding path (LeetCode 628 / 968 / 1663 / 1064 / 1065 / 1780).
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "maximum_product",
            "def maximum_product(nums):\n"
            '    """Max product of three numbers (LeetCode 628)."""\n'
            "    s = sorted(nums)\n"
            "    return max(s[-1] * s[-2] * s[-3], s[0] * s[1] * s[-1])\n"
            "\n"
            "def maximumProduct(nums):\n"
            "    return maximum_product(nums)\n",
            lambda low: bool(
                re.search(r"\bleetcode 628\b", low)
                or (
                    "maximum product of three" in low
                    and "difference" not in low
                    and "two elements" not in low
                    and "subarray" not in low
                )
            ),
            (
                (([1, 2, 3],), 6),
                (([1, 2, 3, 4],), 24),
                (([-1, -2, -3],), -6),
                (([-100, -98, 1, 2, 3],), 29400),
            ),
        ),
        T(
            "min_camera_cover",
            "def min_camera_cover(root):\n"
            '    """Minimum cameras so every node is watched (LeetCode 968).\n'
            "\n"
            "    Nodes are [val, left, right]; missing children may be omitted or None.\n"
            '    """\n'
            "    ans = 0\n"
            "\n"
            "    def kids(node):\n"
            "        if not node:\n"
            "            return None, None\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        return left, right\n"
            "\n"
            "    def dfs(node):\n"
            "        nonlocal ans\n"
            "        if not node:\n"
            "            return 1\n"
            "        left, right = kids(node)\n"
            "        ls, rs = dfs(left), dfs(right)\n"
            "        if ls == 0 or rs == 0:\n"
            "            ans += 1\n"
            "            return 2\n"
            "        if ls == 2 or rs == 2:\n"
            "            return 1\n"
            "        return 0\n"
            "\n"
            "    if dfs(root) == 0:\n"
            "        ans += 1\n"
            "    return ans\n"
            "\n"
            "def minCameraCover(root):\n"
            "    return min_camera_cover(root)\n",
            lambda low: bool(
                re.search(r"\bbinary tree cameras\b|\bleetcode 968\b", low)
            ),
            (
                (([0],), 1),
                (([0, [0, [0], [0]], None],), 1),
                (([0, [0, [0, None, [0]], None], None],), 2),
            ),
        ),
        T(
            "get_smallest_string",
            "def get_smallest_string(n, k):\n"
            '    """Lexicographically smallest length-n string with numeric value k (LeetCode 1663)."""\n'
            "    chars = [\"a\"] * n\n"
            "    remain = k - n\n"
            "    i = n - 1\n"
            "    while remain > 0 and i >= 0:\n"
            "        add = 25 if remain > 25 else remain\n"
            "        chars[i] = chr(ord(\"a\") + add)\n"
            "        remain -= add\n"
            "        i -= 1\n"
            "    return \"\".join(chars)\n"
            "\n"
            "def getSmallestString(n, k):\n"
            "    return get_smallest_string(n, k)\n",
            lambda low: bool(
                re.search(r"\bleetcode 1663\b", low)
                or (
                    "smallest string with a given numeric value" in low
                    and "swap" not in low
                )
            ),
            (
                ((3, 27), "aay"),
                ((5, 73), "aaszz"),
                ((1, 1), "a"),
            ),
        ),
        T(
            "fixed_point",
            "def fixed_point(arr):\n"
            '    """Smallest index i with arr[i] == i, or -1 (LeetCode 1064)."""\n'
            "    lo, hi, ans = 0, len(arr) - 1, -1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] == mid:\n"
            "            ans = mid\n"
            "            hi = mid - 1\n"
            "        elif arr[mid] < mid:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return ans\n"
            "\n"
            "def fixedPoint(arr):\n"
            "    return fixed_point(arr)\n",
            lambda low: bool(
                re.search(r"\bleetcode 1064\b", low)
                or "fixed point in a sorted array" in low
                or ("fixed point" in low and "floating" not in low and "sorted" in low)
            ),
            (
                (([-10, -5, 0, 3, 7],), 3),
                (([0, 2, 5, 8, 17],), 0),
                (([-10, -5, 3, 4, 7, 9],), -1),
            ),
        ),
        T(
            "index_pairs",
            "def index_pairs(text, words):\n"
            '    """Start/end index pairs of words inside text (LeetCode 1065)."""\n'
            "    ans = []\n"
            "    for word in words:\n"
            "        start = 0\n"
            "        while word:\n"
            "            i = text.find(word, start)\n"
            "            if i < 0:\n"
            "                break\n"
            "            ans.append([i, i + len(word) - 1])\n"
            "            start = i + 1\n"
            "    ans.sort()\n"
            "    return ans\n"
            "\n"
            "def indexPairs(text, words):\n"
            "    return index_pairs(text, words)\n",
            lambda low: bool(
                re.search(r"\bleetcode 1065\b|\bindex pairs of a string\b", low)
            ),
            (
                (("thestoryofleetcodeandme", ["story", "fleet", "leetcode"]), [[3, 7], [9, 13], [10, 17]]),
                (("ababa", ["aba", "ab"]), [[0, 1], [0, 2], [2, 3], [2, 4]]),
            ),
        ),
        T(
            "check_powers_of_three",
            "def check_powers_of_three(n):\n"
            '    """True if n is a sum of distinct powers of three (LeetCode 1780)."""\n'
            "    while n > 0:\n"
            "        if n % 3 == 2:\n"
            "            return False\n"
            "        n //= 3\n"
            "    return True\n"
            "\n"
            "def checkPowersOfThree(n):\n"
            "    return check_powers_of_three(n)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1780\b|\bsum of powers of three\b",
                    low,
                )
            ),
            (
                ((12,), True),
                ((91,), True),
                ((21,), False),
            ),
        ),
    ]
