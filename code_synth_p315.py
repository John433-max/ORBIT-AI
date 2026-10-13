"""Cycle 611 (p315): Educational search algorithms and speculative decoding sketches.

Highest pack so specific matchers win over broader neighbors.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "exponential_search",
            "def exponential_search(arr, target):\n"
            '    """Exponential search on a sorted ascending array.\n'
            "    Doubles the bound until arr[bound] >= target, then binary-searches\n"
            "    the range [bound//2, min(bound, n-1)]. Returns index or -1.\n"
            "    O(log i) where i is the index of the target.\n"
            '    """\n'
            "    n = len(arr)\n"
            "    if n == 0:\n"
            "        return -1\n"
            "    if arr[0] == target:\n"
            "        return 0\n"
            "    bound = 1\n"
            "    while bound < n and arr[bound] < target:\n"
            "        bound *= 2\n"
            "    lo, hi = bound // 2, min(bound, n - 1)\n"
            "    while lo <= hi:\n"
            "        mid = lo + (hi - lo) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        if arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\bexponential(?:[- ]search)?\b", low)
            )
            and "tree" not in low,
            (
                (([2, 3, 4, 10, 40, 50, 60], 10), 3),
                (([1, 2, 3, 4, 5], 1), 0),
                (([1, 2, 3, 4, 5], 6), -1),
                (([], 1), -1),
            ),
        ),
        T(
            "jump_search",
            "def jump_search(arr, target):\n"
            '    """Jump search on a sorted ascending array.\n'
            "    Block size is floor(sqrt(n)). Jumps by blocks until the block\n"
            "    that may contain target, then linear-scans inside it.\n"
            "    Returns index or -1.\n"
            '    """\n'
            "    import math\n"
            "    n = len(arr)\n"
            "    if n == 0:\n"
            "        return -1\n"
            "    step = int(math.sqrt(n)) or 1\n"
            "    prev = 0\n"
            "    while arr[min(step, n) - 1] < target:\n"
            "        prev = step\n"
            "        step += int(math.sqrt(n)) or 1\n"
            "        if prev >= n:\n"
            "            return -1\n"
            "    while prev < min(step, n):\n"
            "        if arr[prev] == target:\n"
            "            return prev\n"
            "        prev += 1\n"
            "    return -1\n",
            lambda low: bool(re.search(r"\bjump[- ]search\b|\bjumpsearch\b", low))
            and "game" not in low
            and "pointer" not in low
            and "lca" not in low
            and "lifting" not in low,
            (
                (([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6), 6),
                (([1, 3, 5, 7, 9], 5), 2),
                (([1, 3, 5], 2), -1),
            ),
        ),
        T(
            "ternary_search",
            "def ternary_search(f, lo, hi, iters=64):\n"
            '    """Ternary search for the maximum of a unimodal function f on [lo, hi].\n'
            "    Evaluates two interior points and discards the third that cannot\n"
            "    contain the max. Returns the approximate argmax (float).\n"
            "    iters controls precision. f should be unimodal (increase then decrease).\n"
            '    """\n'
            "    for _ in range(iters):\n"
            "        m1 = lo + (hi - lo) / 3.0\n"
            "        m2 = hi - (hi - lo) / 3.0\n"
            "        if f(m1) < f(m2):\n"
            "            lo = m1\n"
            "        else:\n"
            "            hi = m2\n"
            "    return round((lo + hi) / 2.0, 6)\n",
            lambda low: bool(
                re.search(r"\bternary(?:[- ]search)?\b", low)
            )
            and "tree" not in low,
            (
                ((lambda x: -(x - 3) ** 2, 0.0, 10.0, 50), 3.0),
                ((lambda x: -abs(x - 1.5), -5.0, 5.0, 40), 1.5),
            ),
        ),
        T(
            "interpolation_search",
            "def interpolation_search(arr, target):\n"
            '    """Interpolation search on a sorted ascending array of numbers.\n'
            "    Estimates the position by linear interpolation between lo/hi.\n"
            "    Better than binary search on uniformly distributed data.\n"
            "    Returns index or -1.\n"
            '    """\n'
            "    lo, hi = 0, len(arr) - 1\n"
            "    while lo <= hi and arr[lo] <= target <= arr[hi]:\n"
            "        if arr[hi] == arr[lo]:\n"
            "            return lo if arr[lo] == target else -1\n"
            "        pos = lo + (target - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])\n"
            "        if arr[pos] == target:\n"
            "            return pos\n"
            "        if arr[pos] < target:\n"
            "            lo = pos + 1\n"
            "        else:\n"
            "            hi = pos - 1\n"
            "    return -1\n",
            lambda low: bool(re.search(r"\binterpolation[- ]search\b|\binterpolationsearch\b", low))
            and "lagrange" not in low
            and "polynomial" not in low
            and "basis" not in low,
            (
                (([10, 20, 30, 40, 50, 60, 70], 40), 3),
                (([1, 2, 3, 4, 5], 5), 4),
                (([1, 2, 3], 4), -1),
            ),
        ),
        T(
            "speculative_decode_greedy",
            "def speculative_decode_greedy(draft_next, target_next, prefix, gamma=4):\n"
            '    """Educational greedy speculative decoding (Leviathan / Chen style).\n'
            "    draft_next(ids) and target_next(ids) return the greedy next token id.\n"
            "    Draft proposes up to gamma tokens; target verifies left-to-right.\n"
            "    Accepts a prefix of matching tokens, then commits the target token\n"
            "    at the first mismatch (or one bonus token if all match).\n"
            "    Returns the new tokens appended to a copy of prefix.\n"
            '    """\n'
            "    ids = list(prefix)\n"
            "    if gamma <= 0:\n"
            "        return ids + [target_next(ids)]\n"
            "    draft = []\n"
            "    for _ in range(gamma):\n"
            "        draft.append(draft_next(ids + draft))\n"
            "    accepted = 0\n"
            "    for i, tok in enumerate(draft):\n"
            "        if target_next(ids + draft[:i]) == tok:\n"
            "            accepted += 1\n"
            "        else:\n"
            "            break\n"
            "    if accepted == len(draft):\n"
            "        return ids + draft + [target_next(ids + draft)]\n"
            "    return ids + draft[:accepted] + [target_next(ids + draft[:accepted])]\n",
            lambda low: bool(
                re.search(r"\bspeculative[- ]decode\b|\bleviathan\b", low)
            ),
            (),
        ),
    ]
