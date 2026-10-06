"""Cycle 468: named sorts and circle/stats that fell through to sort_list or fallback.

Loaded first so shell/counting/heap sort do not hit sort_list, and circle
area does not miss entirely.
"""
from __future__ import annotations

from code_synth import Template

_PI = 3.141592653589793


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "shell_sort",
            "def shell_sort(items):\n"
            '    """Shell sort (Shell 1959) with gap n//2. Returns a new list."""\n'
            "    a = list(items)\n"
            "    n = len(a)\n"
            "    gap = n // 2\n"
            "    while gap:\n"
            "        for i in range(gap, n):\n"
            "            tmp = a[i]\n"
            "            j = i\n"
            "            while j >= gap and a[j - gap] > tmp:\n"
            "                a[j] = a[j - gap]\n"
            "                j -= gap\n"
            "            a[j] = tmp\n"
            "        gap //= 2\n"
            "    return a\n",
            lambda low: "shell sort" in low or "shellsort" in low,
            (
                (([3, 1, 2],), [1, 2, 3]),
                (([],), []),
                (([5, 5, 1],), [1, 5, 5]),
            ),
        ),
        T(
            "counting_sort",
            "def counting_sort(nums):\n"
            '    """Counting sort for non-negative ints. Stable by value, new list."""\n'
            "    xs = [int(x) for x in nums]\n"
            "    if not xs:\n"
            "        return []\n"
            "    if any(x < 0 for x in xs):\n"
            "        raise ValueError('counting sort expects non-negative ints')\n"
            "    counts = [0] * (max(xs) + 1)\n"
            "    for x in xs:\n"
            "        counts[x] += 1\n"
            "    out = []\n"
            "    for value, count in enumerate(counts):\n"
            "        out.extend([value] * count)\n"
            "    return out\n",
            lambda low: "counting sort" in low or "countingsort" in low,
            (
                (([3, 1, 2, 1],), [1, 1, 2, 3]),
                (([],), []),
                (([0, 4, 0],), [0, 0, 4]),
            ),
        ),
        T(
            "heap_sort",
            "def heap_sort(items):\n"
            '    """In-place-style binary heap sort (Williams 1964). Returns a new list."""\n'
            "    a = list(items)\n"
            "    n = len(a)\n"
            "\n"
            "    def _heapify(size, i):\n"
            "        while True:\n"
            "            largest = i\n"
            "            left = 2 * i + 1\n"
            "            right = 2 * i + 2\n"
            "            if left < size and a[left] > a[largest]:\n"
            "                largest = left\n"
            "            if right < size and a[right] > a[largest]:\n"
            "                largest = right\n"
            "            if largest == i:\n"
            "                return\n"
            "            a[i], a[largest] = a[largest], a[i]\n"
            "            i = largest\n"
            "\n"
            "    for i in range(n // 2 - 1, -1, -1):\n"
            "        _heapify(n, i)\n"
            "    for end in range(n - 1, 0, -1):\n"
            "        a[0], a[end] = a[end], a[0]\n"
            "        _heapify(end, 0)\n"
            "    return a\n",
            lambda low: "heap sort" in low or "heapsort" in low,
            (
                (([4, 1, 3, 2],), [1, 2, 3, 4]),
                (([],), []),
                (([2, 2, 1],), [1, 2, 2]),
            ),
        ),
        T(
            "circle_area",
            "def circle_area(r):\n"
            '    """Disk area pi*r^2, rounded to 6 decimals."""\n'
            f"    return round({_PI} * float(r) * float(r), 6)\n",
            lambda low: (
                "circle" in low
                and "area" in low
                and "circumference" not in low
                and "point" not in low
                and "inside" not in low
                and "surface" not in low
                and "perimeter" not in low
            ),
            (
                ((1,), 3.141593),
                ((0,), 0.0),
                ((2,), 12.566371),
            ),
        ),
        T(
            "circle_circumference",
            "def circle_circumference(r):\n"
            '    """Circle circumference 2*pi*r, rounded to 6 decimals."""\n'
            f"    return round(2.0 * {_PI} * float(r), 6)\n",
            lambda low: "circumference" in low and "circle" in low,
            (
                ((1,), 6.283185),
                ((0,), 0.0),
                ((2,), 12.566371),
            ),
        ),
        T(
            "sample_variance",
            "def sample_variance(nums):\n"
            '    """Unbiased sample variance (Bessel, divide by n-1)."""\n'
            "    xs = [float(x) for x in nums]\n"
            "    n = len(xs)\n"
            "    if n < 2:\n"
            "        raise ValueError('need at least two numbers')\n"
            "    mean = sum(xs) / n\n"
            "    return round(sum((x - mean) ** 2 for x in xs) / (n - 1), 6)\n",
            lambda low: (
                "sample" in low
                and "variance" in low
                and "population" not in low
                and "stdev" not in low
                and "standard deviation" not in low
            ),
            (
                (([1, 2, 3],), 1.0),
                (([2, 2, 2, 2],), 0.0),
                (([1, 3],), 2.0),
            ),
        ),
        T(
            "sphere_volume",
            "def sphere_volume(r):\n"
            '    """Sphere volume 4/3*pi*r^3, rounded to 6 decimals."""\n'
            f"    return round(4.0 / 3.0 * {_PI} * float(r) ** 3, 6)\n",
            lambda low: (
                "sphere" in low
                and "volume" in low
                and "surface" not in low
            ),
            (
                ((1,), 4.18879),
                ((0,), 0.0),
                ((3,), 113.097336),
            ),
        ),
        T(
            "hypotenuse",
            "def hypotenuse(a, b):\n"
            '    """Right-triangle hypotenuse sqrt(a^2+b^2), rounded to 6 decimals."""\n'
            "    return round((float(a) ** 2 + float(b) ** 2) ** 0.5, 6)\n",
            lambda low: "hypotenuse" in low,
            (
                ((3, 4), 5.0),
                ((0, 0), 0.0),
                ((5, 12), 13.0),
            ),
        ),
    ]
