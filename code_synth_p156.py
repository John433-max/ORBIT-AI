"""Cycle 435: wiggle sort II, malware spread II, stack sequences, tokens, chunks II, monotone digits.

Matchers are id- or phrase-gated. Wiggle sort II does not steal wiggle subsequence.
Malware II does not steal 924 (that matcher already excludes "ii").
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "wiggle_sort_ii",
            "def wiggle_sort(nums):\n"
            '    """Reorder so nums[0] < nums[1] > nums[2] < nums[3] ... (LeetCode 324)."""\n'
            "    arr = sorted(int(x) for x in nums)\n"
            "    n = len(arr)\n"
            "    mid = (n + 1) // 2\n"
            "    small = arr[:mid][::-1]\n"
            "    large = arr[mid:][::-1]\n"
            "    out = []\n"
            "    for i in range(n):\n"
            "        out.append(small[i // 2] if i % 2 == 0 else large[i // 2])\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode 324\b", low)
                or "wiggle sort ii" in low
                or "wiggle sort 2" in low
            )
            and "subsequence" not in low,
            (
                (([1, 5, 1, 1, 6, 4],), [1, 6, 1, 5, 1, 4]),
                (([1, 3, 2, 2, 3, 1],), [2, 3, 1, 3, 1, 2]),
            ),
        ),
        T(
            "min_malware_spread_ii",
            "def min_malware_spread(graph, initial):\n"
            '    """Remove one initial node and its edges to minimize spread (LeetCode 928)."""\n'
            "    n = len(graph)\n"
            "    seeds = sorted(set(int(x) for x in initial))\n"
            "    def infected_count(removed):\n"
            "        infected = {s for s in seeds if s != removed}\n"
            "        changed = True\n"
            "        while changed:\n"
            "            changed = False\n"
            "            for i in range(n):\n"
            "                if i == removed or i in infected:\n"
            "                    continue\n"
            "                if any(graph[i][j] and j in infected for j in range(n)):\n"
            "                    infected.add(i)\n"
            "                    changed = True\n"
            "        return len(infected)\n"
            "    best = seeds[0]\n"
            "    best_count = infected_count(best)\n"
            "    for node in seeds[1:]:\n"
            "        count = infected_count(node)\n"
            "        if count < best_count:\n"
            "            best_count = count\n"
            "            best = node\n"
            "    return best\n",
            lambda low: bool(
                re.search(r"\bleetcode 928\b", low)
                or "minimize malware spread ii" in low
                or "malware spread ii" in low
            ),
            (
                (([[1, 1, 0], [1, 1, 0], [0, 0, 1]], [0, 1]), 0),
                (([[1, 1, 0], [1, 1, 1], [0, 1, 1]], [0, 1]), 1),
                (([[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]], [0, 1]), 1),
            ),
        ),
        T(
            "validate_stack_sequences",
            "def validate_stack_sequences(pushed, popped):\n"
            '    """Whether popped is a valid stack order of pushed (LeetCode 946)."""\n'
            "    stack = []\n"
            "    j = 0\n"
            "    popped = [int(x) for x in popped]\n"
            "    for x in pushed:\n"
            "        stack.append(int(x))\n"
            "        while stack and j < len(popped) and stack[-1] == popped[j]:\n"
            "            stack.pop()\n"
            "            j += 1\n"
            "    return j == len(popped)\n",
            lambda low: bool(
                re.search(r"\bleetcode 946\b", low)
                or "validate stack sequences" in low
                or "validate stack sequence" in low
            ),
            (
                (([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]), True),
                (([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]), False),
            ),
        ),
        T(
            "bag_of_tokens",
            "def bag_of_tokens_score(tokens, power):\n"
            '    """Max score from face-up / face-down token plays (LeetCode 948)."""\n'
            "    tokens = sorted(int(x) for x in tokens)\n"
            "    power = int(power)\n"
            "    lo, hi = 0, len(tokens) - 1\n"
            "    score = best = 0\n"
            "    while lo <= hi:\n"
            "        if power >= tokens[lo]:\n"
            "            power -= tokens[lo]\n"
            "            lo += 1\n"
            "            score += 1\n"
            "            best = max(best, score)\n"
            "        elif score > 0 and lo < hi:\n"
            "            power += tokens[hi]\n"
            "            hi -= 1\n"
            "            score -= 1\n"
            "        else:\n"
            "            break\n"
            "    return best\n",
            lambda low: bool(
                re.search(r"\bleetcode 948\b", low)
                or "bag of tokens" in low
            ),
            (
                (([100], 50), 0),
                (([200, 100], 150), 1),
                (([100, 200, 300, 400], 200), 2),
            ),
        ),
        T(
            "partition_disjoint",
            "def partition_disjoint(nums):\n"
            '    """Shortest left chunk whose max is <= every right value (LeetCode 915)."""\n'
            "    nums = [int(x) for x in nums]\n"
            "    n = len(nums)\n"
            "    left_max = nums[0]\n"
            "    cur_max = nums[0]\n"
            "    split = 0\n"
            "    for i in range(1, n):\n"
            "        cur_max = max(cur_max, nums[i])\n"
            "        if nums[i] < left_max:\n"
            "            split = i\n"
            "            left_max = cur_max\n"
            "    return split + 1\n",
            lambda low: bool(
                re.search(r"\bleetcode 915\b", low)
                or "partition array into disjoint" in low
                or "disjoint intervals" in low
            ),
            (
                (([5, 0, 3, 8, 6],), 3),
                (([1, 1, 1, 0, 6, 12],), 4),
            ),
        ),
        T(
            "monotone_increasing_digits",
            "def monotone_increasing_digits(n):\n"
            '    """Largest integer <= n with non-decreasing digits (LeetCode 738)."""\n'
            "    digits = list(str(int(n)))\n"
            "    mark = len(digits)\n"
            "    for i in range(len(digits) - 1):\n"
            "        if digits[i] > digits[i + 1]:\n"
            "            while i > 0 and digits[i] == digits[i - 1]:\n"
            "                i -= 1\n"
            "            digits[i] = str(int(digits[i]) - 1)\n"
            "            mark = i + 1\n"
            "            break\n"
            "    for j in range(mark, len(digits)):\n"
            "        digits[j] = '9'\n"
            "    return int(''.join(digits))\n",
            lambda low: bool(
                re.search(r"\bleetcode 738\b", low)
                or "monotone increasing digits" in low
            ),
            (
                ((10,), 9),
                ((1234,), 1234),
                ((332,), 299),
            ),
        ),
    ]
