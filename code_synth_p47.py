"""Cycle 309: palindrome number / shift 2D grid / monotonic array / odd cells / rank transform / matrix diagonal sum."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "palindrome_number",
            "def palindrome_number(x):\n"
            '    """True if integer x is a palindrome (LeetCode 9)."""\n'
            "    s = str(int(x))\n"
            "    return s == s[::-1]\n",
            lambda low: bool(
                re.search(
                    r"\bpalindrome[_ ]number\b|"
                    r"\bis[_ ]palindrome[_ ]number\b|"
                    r"\bnumber[_ ]is[_ ](a[_ ])?palindrome\b",
                    low,
                )
            ),
            (
                ((121,), True),
                ((-121,), False),
                ((10,), False),
            ),
        ),
        T(
            "shift_grid",
            "def shift_grid(grid, k):\n"
            '    """Shift grid values k times (LeetCode 1260)."""\n'
            "    m, n = len(grid), len(grid[0]) if grid else 0\n"
            "    flat = [v for row in grid for v in row]\n"
            "    if not flat:\n"
            "        return grid\n"
            "    k %= len(flat)\n"
            "    flat = flat[-k:] + flat[:-k] if k else flat\n"
            "    return [flat[i * n:(i + 1) * n] for i in range(m)]\n",
            lambda low: bool(
                re.search(
                    r"\bshift[_ ](2d[_ ]|two[_ ]dimensional[_ ])?grid\b|"
                    r"\bshift_grid\b",
                    low,
                )
            ),
            (
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1), [[9, 1, 2], [3, 4, 5], [6, 7, 8]]),
                (([[3, 8, 1, 9], [19, 7, 2, 5], [4, 6, 11, 10], [12, 0, 21, 13]], 4), [[12, 0, 21, 13], [3, 8, 1, 9], [19, 7, 2, 5], [4, 6, 11, 10]]),
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9), [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            ),
        ),
        T(
            "monotonic_array",
            "def monotonic_array(nums):\n"
            '    """True if nums is monotone increasing or decreasing (LeetCode 896)."""\n'
            "    inc = dec = True\n"
            "    for i in range(1, len(nums)):\n"
            "        if nums[i] < nums[i - 1]:\n"
            "            inc = False\n"
            "        if nums[i] > nums[i - 1]:\n"
            "            dec = False\n"
            "    return inc or dec\n",
            lambda low: bool(
                re.search(r"\bmonotonic[_ ]array\b|\bmonotone[_ ]array\b", low)
            ) and not re.search(r"\bis[_ ]monotonic\b", low),
            (
                (([1, 2, 2, 3],), True),
                (([6, 5, 4, 4],), True),
                (([1, 3, 2],), False),
            ),
        ),
        T(
            "odd_cells",
            "def odd_cells(m, n, indices):\n"
            '    """Count cells with odd values after increments (LeetCode 1252)."""\n'
            "    rows = [0] * m\n"
            "    cols = [0] * n\n"
            "    for r, c in indices:\n"
            "        rows[r] ^= 1\n"
            "        cols[c] ^= 1\n"
            "    return sum((rows[i] + cols[j]) % 2 for i in range(m) for j in range(n))\n",
            lambda low: bool(
                re.search(
                    r"\bcells[_ ]with[_ ]odd[_ ]values\b|"
                    r"\bodd[_ ]cells\b|"
                    r"\bodd_cells\b",
                    low,
                )
            ),
            (
                ((2, 3, [[0, 1], [1, 1]]), 6),
                ((2, 2, [[1, 1], [0, 0]]), 0),
            ),
        ),
        T(
            "rank_transform",
            "def rank_transform(arr):\n"
            '    """Replace each value with its rank (LeetCode 1331)."""\n'
            "    order = sorted(set(arr))\n"
            "    rank = {v: i + 1 for i, v in enumerate(order)}\n"
            "    return [rank[v] for v in arr]\n",
            lambda low: bool(
                re.search(
                    r"\brank[_ ]transform\b|"
                    r"\brank[_ ]transform[_ ]of[_ ]an[_ ]array\b|"
                    r"\brank_transform\b",
                    low,
                )
            ),
            (
                (([40, 10, 20, 30],), [4, 1, 2, 3]),
                (([100, 100, 100],), [1, 1, 1]),
                (([37, 12, 28, 9, 100, 56, 80, 5, 12],), [5, 3, 4, 2, 8, 6, 7, 1, 3]),
            ),
        ),
        T(
            "k_weakest_rows",
            "def k_weakest_rows(mat, k):\n"
            '    """Indices of the k weakest rows (LeetCode 1337)."""\n'
            "    scored = []\n"
            "    for i, row in enumerate(mat):\n"
            "        s = 0\n"
            "        for v in row:\n"
            "            if int(v) == 1:\n"
            "                s += 1\n"
            "            else:\n"
            "                break\n"
            "        scored.append((s, i))\n"
            "    scored.sort()\n"
            "    return [i for _, i in scored[: int(k)]]\n",
            lambda low: bool(
                re.search(
                    r"\bk[_ ]weakest[_ ]rows\b|"
                    r"\bweakest[_ ]rows[_ ]in[_ ](a[_ ])?matrix\b|"
                    r"\bk_weakest_rows\b",
                    low,
                )
            ),
            (
                (([[1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]], 3), [2, 0, 3]),
                (([[1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0]], 2), [0, 2]),
            ),
        ),
        T(
            "matrix_diagonal_sum",
            "def matrix_diagonal_sum(mat):\n"
            '    """Sum of primary and secondary diagonals (LeetCode 1572)."""\n'
            "    n = len(mat)\n"
            "    total = 0\n"
            "    for i in range(n):\n"
            "        total += int(mat[i][i])\n"
            "        j = n - 1 - i\n"
            "        if j != i:\n"
            "            total += int(mat[i][j])\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bmatrix[_ ]diagonal[_ ]sum\b|"
                    r"\bdiagonal[_ ]sum\b|"
                    r"\bmatrix_diagonal_sum\b",
                    low,
                )
            ),
            (
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), 25),
                (([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],), 8),
                (([[5]],), 5),
            ),
        ),
    ]
