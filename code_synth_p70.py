"""Cycle 333: unused Easy — winning players / apple boxes / ant boundary /
intersection values / stable mountains / special chars I."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "winning_player_count",
            "def winning_player_count(n, pick):\n"
            '    """Players who picked one color > i times (LeetCode 3238)."""\n'
            "    from collections import defaultdict\n"
            "    freq = defaultdict(lambda: defaultdict(int))\n"
            "    for player, color in pick:\n"
            "        freq[player][color] += 1\n"
            "    wins = 0\n"
            "    for i in range(n):\n"
            "        if any(c > i for c in freq[i].values()):\n"
            "            wins += 1\n"
            "    return wins\n",
            lambda low: bool(
                re.search(
                    r"\bwinning_player_count\b|"
                    r"\bfind[_ ]the[_ ]number[_ ]of[_ ]winning[_ ]players\b|"
                    r"\bwinning[_ ]players\b|"
                    r"\bleetcode[_ ]3238\b",
                    low,
                )
            ),
            (
                ((4, [[0, 0], [1, 0], [1, 0], [2, 1], [2, 1], [2, 0]]), 2),
                ((5, [[1, 1], [1, 2], [1, 3], [1, 4]]), 0),
                ((2, [[1, 1], [1, 1]]), 1),
            ),
        ),
        T(
            "minimum_boxes",
            "def minimum_boxes(apple, capacity):\n"
            '    """Min boxes (largest first) to hold all apples (LeetCode 3074)."""\n'
            "    need = sum(apple)\n"
            "    boxes = sorted(capacity, reverse=True)\n"
            "    used = 0\n"
            "    for c in boxes:\n"
            "        need -= c\n"
            "        used += 1\n"
            "        if need <= 0:\n"
            "            return used\n"
            "    return used\n",
            lambda low: bool(
                re.search(
                    r"\bminimum_boxes\b|"
                    r"\bapple[_ ]redistribution[_ ]into[_ ]boxes\b|"
                    r"\bminimum[_ ]number[_ ]of[_ ]boxes\b|"
                    r"\bleetcode[_ ]3074\b",
                    low,
                )
            )
            and "climbing" not in low,
            (
                (([1, 3, 2], [4, 3, 1, 5, 2]), 2),
                (([5, 5, 5], [2, 4, 2, 7]), 4),
            ),
        ),
        T(
            "return_to_boundary_count",
            "def return_to_boundary_count(nums):\n"
            '    """Times an ant on the line returns to 0 (LeetCode 3028)."""\n'
            "    pos = 0\n"
            "    hits = 0\n"
            "    for x in nums:\n"
            "        pos += x\n"
            "        if pos == 0:\n"
            "            hits += 1\n"
            "    return hits\n",
            lambda low: bool(
                re.search(
                    r"\breturn_to_boundary_count\b|"
                    r"\bant[_ ]on[_ ]the[_ ]boundary\b|"
                    r"\breturn[_ ]to[_ ]boundary\b|"
                    r"\bleetcode[_ ]3028\b",
                    low,
                )
            ),
            (
                (([2, 3, -5],), 1),
                (([3, 2, -3, -4],), 0),
            ),
        ),
        T(
            "find_intersection_values",
            "def find_intersection_values(nums1, nums2):\n"
            '    """[count nums1 in nums2, count nums2 in nums1] (LeetCode 2956)."""\n'
            "    s1, s2 = set(nums1), set(nums2)\n"
            "    a = sum(1 for x in nums1 if x in s2)\n"
            "    b = sum(1 for x in nums2 if x in s1)\n"
            "    return [a, b]\n",
            lambda low: bool(
                re.search(
                    r"\bfind_intersection_values\b|"
                    r"\bfind[_ ]common[_ ]elements[_ ]between[_ ]two[_ ]arrays\b|"
                    r"\bintersection[_ ]values\b|"
                    r"\bleetcode[_ ]2956\b",
                    low,
                )
            )
            and "difference of two arrays" not in low,
            (
                (([4, 3, 2, 3, 1], [2, 2, 5, 2, 3, 6]), [3, 4]),
                (([3, 4, 2, 3], [1, 5]), [0, 0]),
            ),
        ),
        T(
            "stable_mountains",
            "def stable_mountains(height, threshold):\n"
            '    """Indices i>0 where height[i-1] > threshold (LeetCode 3285)."""\n'
            "    return [i for i in range(1, len(height)) if height[i - 1] > threshold]\n",
            lambda low: bool(
                re.search(
                    r"\bstable_mountains\b|"
                    r"\bstable[_ ]mountains\b|"
                    r"\bfind[_ ]indices[_ ]of[_ ]stable[_ ]mountains\b|"
                    r"\bleetcode[_ ]3285\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 5], 2), [3, 4]),
                (([10, 1, 10, 1, 10], 3), [1, 3]),
                (([10, 1, 10, 1, 10], 10), []),
            ),
        ),
        T(
            "number_of_special_chars",
            "def number_of_special_chars(word):\n"
            '    """Count letters that appear in both cases (LeetCode 3120)."""\n'
            "    lows = set()\n"
            "    ups = set()\n"
            "    for ch in word:\n"
            "        if 'a' <= ch <= 'z':\n"
            "            lows.add(ch)\n"
            "        else:\n"
            "            ups.add(ch.lower())\n"
            "    return len(lows & ups)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber_of_special_chars\b|"
                    r"\bcount[_ ]the[_ ]number[_ ]of[_ ]special[_ ]characters\b|"
                    r"\bnumber[_ ]of[_ ]special[_ ]characters\b|"
                    r"\bleetcode[_ ]3120\b",
                    low,
                )
            )
            and "3121" not in low
            and "special characters ii" not in low,
            (
                (("aaAbcBC",), 3),
                (("abc",), 0),
                (("abBCab",), 1),
            ),
        ),
    ]
