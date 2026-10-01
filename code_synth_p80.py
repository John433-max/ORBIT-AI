"""Cycle 349: unused Easy — ant boundary / candy split / longest diagonal /
circular adjacent gap / good numbers / ship containers."""

from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "return_to_boundary_count",
            "def return_to_boundary_count(nums):\n"
            '    """Times the ant is back on the boundary after a step (LeetCode 3028)."""\n'
            "    pos = 0\n"
            "    hits = 0\n"
            "    for step in nums:\n"
            "        pos += step\n"
            "        if pos == 0:\n"
            "            hits += 1\n"
            "    return hits\n",
            lambda low: "ant on the boundary" in low or "returns to the boundary" in low,
            (
                (([2, 3, -5],), 1),
                (([3, 2, -3, -4],), 0),
                (([1, -1, 2, -2],), 2),
            ),
        ),
        T(
            "distribute_candies",
            "def distribute_candies(n, limit):\n"
            '    """Ways to give n candies to 3 children, each at most limit (LeetCode 2928)."""\n'
            "    ways = 0\n"
            "    for a in range(limit + 1):\n"
            "        for b in range(limit + 1):\n"
            "            c = n - a - b\n"
            "            if 0 <= c <= limit:\n"
            "                ways += 1\n"
            "    return ways\n",
            lambda low: "distribute candies among children" in low
            or ("candies" in low and "limit" in low and "children" in low),
            (
                ((5, 2), 3),
                ((3, 3), 10),
                ((1, 1), 3),
            ),
        ),
        T(
            "area_of_max_diagonal",
            "def area_of_max_diagonal(dimensions):\n"
            '    """Area of the rectangle with the longest diagonal (LeetCode 3000)."""\n'
            "    best_diag = -1\n"
            "    best_area = 0\n"
            "    for length, width in dimensions:\n"
            "        diag = length * length + width * width\n"
            "        area = length * width\n"
            "        if diag > best_diag or (diag == best_diag and area > best_area):\n"
            "            best_diag = diag\n"
            "            best_area = area\n"
            "    return best_area\n",
            lambda low: "longest diagonal" in low and "rectangle" in low,
            (
                (([[9, 3], [8, 6]],), 48),
                (([[3, 4], [4, 3]],), 12),
                (([[2, 2]],), 4),
            ),
        ),
        T(
            "max_adjacent_distance",
            "def max_adjacent_distance(nums):\n"
            '    """Max absolute gap between circular neighbors (LeetCode 3423)."""\n'
            "    best = 0\n"
            "    for i, value in enumerate(nums):\n"
            "        nxt = nums[(i + 1) % len(nums)]\n"
            "        best = max(best, abs(value - nxt))\n"
            "    return best\n",
            lambda low: "adjacent elements in a circular" in low
            or ("circular array" in low and "adjacent" in low),
            (
                (([1, 2, 4],), 3),
                (([-5, -10, -5],), 5),
                (([7],), 0),
            ),
        ),
        T(
            "sum_of_good_numbers",
            "def sum_of_good_numbers(nums, k):\n"
            '    """Sum of values strictly greater than both k-step neighbors (LeetCode 3452)."""\n'
            "    total = 0\n"
            "    n = len(nums)\n"
            "    for i, value in enumerate(nums):\n"
            "        left = i - k < 0 or value > nums[i - k]\n"
            "        right = i + k >= n or value > nums[i + k]\n"
            "        if left and right:\n"
            "            total += value\n"
            "    return total\n",
            lambda low: "sum of good numbers" in low or (
                "good numbers" in low and "leetcode 3452" in low
            ),
            (
                (([1, 3, 2, 1, 5, 4], 2), 12),
                (([2, 1], 1), 2),
                (([4, 1, 2], 1), 6),
            ),
        ),
        T(
            "max_containers",
            "def max_containers(n, w, max_weight):\n"
            '    """Containers on an n x n deck under a weight cap (LeetCode 3492)."""\n'
            "    cells = n * n\n"
            "    by_weight = max_weight // w\n"
            "    return cells if cells < by_weight else by_weight\n",
            lambda low: "containers on a ship" in low or (
                "maximum containers" in low and "ship" in low
            ),
            (
                ((2, 3, 15), 4),
                ((3, 5, 20), 4),
                ((1, 2, 3), 1),
            ),
        ),
    ]
