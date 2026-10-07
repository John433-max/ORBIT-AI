"""Cycle 284: array / Pascal-II / rotate-array templates + tighter siblings."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "merge_sorted_array",
            "def merge_sorted_array(nums1, m, nums2, n):\n"
            '    """Merge nums2 into nums1 in-place (both already sorted)."""\n'
            "    i, j, k = m - 1, n - 1, m + n - 1\n"
            "    while j >= 0:\n"
            "        if i >= 0 and nums1[i] > nums2[j]:\n"
            "            nums1[k] = nums1[i]\n"
            "            i -= 1\n"
            "        else:\n"
            "            nums1[k] = nums2[j]\n"
            "            j -= 1\n"
            "        k -= 1\n"
            "    return nums1\n",
            lambda low: bool(
                re.search(
                    r"\bmerge[_ ]sorted[_ ]array\b|"
                    r"\bmerge two sorted arrays?\b|"
                    r"\bmerge nums2 into nums1\b",
                    low,
                )
                and "interval" not in low
                and "linked" not in low
            ),
            (
                (([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3), [1, 2, 2, 3, 5, 6]),
                (([1], 1, [], 0), [1]),
                (([0], 0, [1], 1), [1]),
            ),
        ),
        T(
            "intersect_two_arrays_ii",
            "def intersect(nums1, nums2):\n"
            '    """Multiset intersection of two arrays (counts preserved)."""\n'
            "    from collections import Counter\n"
            "    c = Counter(nums1)\n"
            "    out = []\n"
            "    for x in nums2:\n"
            "        if c[x] > 0:\n"
            "            out.append(x)\n"
            "            c[x] -= 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bintersect(?:ion)? of two arrays? i{1,2}\b|"
                    r"\bintersect_two_arrays_ii\b|"
                    r"\bmultiset intersection\b|"
                    r"\bintersection.{0,24}\b(with )?(counts|duplicates)\b",
                    low,
                )
            ),
            (
                (([1, 2, 2, 1], [2, 2]), [2, 2]),
                (([4, 9, 5], [9, 4, 9, 8, 4]), [9, 4]),
            ),
        ),
        T(
            "contains_duplicate_ii",
            "def contains_nearby_duplicate(nums, k):\n"
            '    """True if some value repeats at indices at most k apart."""\n'
            "    last = {}\n"
            "    for i, x in enumerate(nums):\n"
            "        if x in last and i - last[x] <= k:\n"
            "            return True\n"
            "        last[x] = i\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bcontains[- ]?duplicates? i{1,2}\b|"
                    r"\bcontains_nearby_duplicate\b|"
                    r"\bnearby duplicates?\b|"
                    r"\bduplicate.{0,20}\bwithin k\b|"
                    r"\bsame value.{0,24}\bat most k\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 1], 3), True),
                (([1, 0, 1, 1], 1), True),
                (([1, 2, 3, 1, 2, 3], 2), False),
            ),
        ),
        T(
            "pascal_triangle_ii",
            "def get_row(row_index):\n"
            '    """Return row `row_index` of Pascal\'s triangle (0-indexed)."""\n'
            "    row = [1]\n"
            "    for i in range(row_index):\n"
            "        nxt = [1]\n"
            "        for j in range(len(row) - 1):\n"
            "            nxt.append(row[j] + row[j + 1])\n"
            "        nxt.append(1)\n"
            "        row = nxt\n"
            "    return row\n",
            lambda low: bool(
                re.search(
                    r"\bpascal(?:'s)? triangle i{1,2}\b|"
                    r"\bpascal_triangle_ii\b|"
                    r"\bget[_ ]row\b.{0,24}\bpascal\b|"
                    r"\bpascal.{0,24}\brow index\b|"
                    r"\bnth row of pascal",
                    low,
                )
            ),
            (
                ((3,), [1, 3, 3, 1]),
                ((0,), [1]),
                ((1,), [1, 1]),
            ),
        ),
        T(
            "remove_element",
            "def remove_element(nums, val):\n"
            '    """In-place compact nums by dropping val; return new length."""\n'
            "    w = 0\n"
            "    for x in nums:\n"
            "        if x != val:\n"
            "            nums[w] = x\n"
            "            w += 1\n"
            "    return w\n",
            lambda low: bool(
                re.search(
                    r"\bremove_element\b|"
                    r"\bremov(?:e|es|ing) element\b|"
                    r"\bin[- ]place.{0,24}\bremove.{0,16}\bval\b",
                    low,
                )
                and "linked" not in low
                and "node" not in low
                and "elements" not in low
            ),
            (
                (([3, 2, 2, 3], 3), 2),
                (([0, 1, 2, 2, 3, 0, 4, 2], 2), 5),
                (([], 1), 0),
            ),
        ),
        T(
            "rotate_array",
            "def rotate_array(nums, k):\n"
            '    """Rotate nums to the right by k steps, in place."""\n'
            "    n = len(nums)\n"
            "    if n == 0:\n"
            "        return nums\n"
            "    k %= n\n"
            "    nums[:] = nums[n - k :] + nums[: n - k]\n"
            "    return nums\n",
            lambda low: bool(
                re.search(
                    r"\brotate[_ ]array\b|"
                    r"\brotate (the )?array\b|"
                    r"\brotate nums to the right\b|"
                    r"\bright rotat(?:e|ion) of (an )?array\b|"
                    r"\brotat(?:e|es|ing) an array to the right\b|"
                    r"\bright rotat(?:e|es) an array\b",
                    low,
                )
                and "matrix" not in low
                and "image" not in low
                and "linked" not in low
            ),
            (
                (([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4]),
                (([-1, -100, 3, 99], 2), [3, 99, -1, -100]),
            ),
        ),
    ]
