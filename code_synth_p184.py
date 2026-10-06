"""Cycle 467: sort variants, quadratic roots, and temperature direction.

Loaded first so selection/insertion sort do not hit sort_list, and
Kelvin→Celsius does not hit celsius_to_kelvin.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "kelvin_to_celsius",
            "def kelvin_to_celsius(k):\n"
            '    """ITS-90 offset: C = K - 273.15, rounded to 6 decimals."""\n'
            "    return round(float(k) - 273.15, 6)\n",
            lambda low: (
                "kelvin" in low
                and ("to celsius" in low or "to centigrade" in low)
                and "to kelvin" not in low
                and "fahrenheit" not in low
            ),
            (
                ((273.15,), 0.0),
                ((0,), -273.15),
                ((373.15,), 100.0),
            ),
        ),
        T(
            "fahrenheit_to_kelvin",
            "def fahrenheit_to_kelvin(f):\n"
            '    """F to K via C: (F-32)*5/9 + 273.15, rounded to 6 decimals."""\n'
            "    return round((float(f) - 32.0) * 5.0 / 9.0 + 273.15, 6)\n",
            lambda low: (
                "fahrenheit" in low
                and "kelvin" in low
                and "to kelvin" in low
                and "to fahrenheit" not in low
                and "celsius" not in low
                and "centigrade" not in low
            ),
            (
                ((32,), 273.15),
                ((212,), 373.15),
                ((-40,), 233.15),
            ),
        ),
        T(
            "selection_sort",
            "def selection_sort(values):\n"
            '    """In-place-style selection sort. Returns a new list."""\n'
            "    arr = list(values)\n"
            "    n = len(arr)\n"
            "    for i in range(n):\n"
            "        min_i = i\n"
            "        for j in range(i + 1, n):\n"
            "            if arr[j] < arr[min_i]:\n"
            "                min_i = j\n"
            "        arr[i], arr[min_i] = arr[min_i], arr[i]\n"
            "    return arr\n",
            lambda low: "selection" in low and "sort" in low,
            (
                (([3, 1, 2],), [1, 2, 3]),
                (([1],), [1]),
                (([],), []),
            ),
        ),
        T(
            "insertion_sort",
            "def insertion_sort(values):\n"
            '    """Stable insertion sort. Returns a new list."""\n'
            "    arr = list(values)\n"
            "    for i in range(1, len(arr)):\n"
            "        key = arr[i]\n"
            "        j = i - 1\n"
            "        while j >= 0 and arr[j] > key:\n"
            "            arr[j + 1] = arr[j]\n"
            "            j -= 1\n"
            "        arr[j + 1] = key\n"
            "    return arr\n",
            lambda low: "insertion" in low and "sort" in low,
            (
                (([3, 1, 2],), [1, 2, 3]),
                (([5, 5, 1],), [1, 5, 5]),
                (([],), []),
            ),
        ),
        T(
            "quadratic_roots",
            "def quadratic_roots(a, b, c):\n"
            '    """Real roots of ax^2+bx+c via the quadratic formula. None if no real roots."""\n'
            "    a = float(a)\n"
            "    b = float(b)\n"
            "    c = float(c)\n"
            "    if a == 0:\n"
            "        return None\n"
            "    disc = b * b - 4.0 * a * c\n"
            "    if disc < 0:\n"
            "        return None\n"
            "    root = disc ** 0.5\n"
            "    return ((-b + root) / (2.0 * a), (-b - root) / (2.0 * a))\n",
            lambda low: (
                "quadratic" in low
                and ("root" in low or "equation" in low or "formula" in low)
            ),
            (
                ((1, -3, 2), (2.0, 1.0)),
                ((1, 0, -4), (2.0, -2.0)),
                ((1, 0, 1), None),
            ),
        ),
        T(
            "euclidean_distance",
            "def euclidean_distance(x1, y1, x2, y2):\n"
            '    """L2 distance between two 2D points."""\n'
            "    return ((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2) ** 0.5\n",
            lambda low: "euclidean" in low and "distance" in low,
            (
                ((0, 0, 3, 4), 5.0),
                ((1, 1, 1, 1), 0.0),
                ((0, 0, 1, 0), 1.0),
            ),
        ),
        T(
            "det2",
            "def det2(matrix):\n"
            '    """Determinant of a 2x2 matrix: ad - bc."""\n'
            "    a, b = matrix[0]\n"
            "    c, d = matrix[1]\n"
            "    return a * d - b * c\n",
            lambda low: (
                "determinant" in low
                and ("2x2" in low or "2 by 2" in low or "two by two" in low or "2×2" in low)
            ),
            (
                (([[1, 2], [3, 4]],), -2),
                (([[2, 0], [0, 3]],), 6),
                (([[1, 0], [0, 1]],), 1),
            ),
        ),
        T(
            "is_symmetric_matrix",
            "def is_symmetric_matrix(matrix):\n"
            '    """True when matrix equals its transpose. Empty is symmetric."""\n'
            "    if not matrix:\n"
            "        return True\n"
            "    rows = len(matrix)\n"
            "    if any(len(row) != rows for row in matrix):\n"
            "        return False\n"
            "    for i in range(rows):\n"
            "        for j in range(rows):\n"
            "            if matrix[i][j] != matrix[j][i]:\n"
            "                return False\n"
            "    return True\n",
            lambda low: "symmetric" in low and "matrix" in low,
            (
                (([[1, 2], [2, 3]],), True),
                (([[1, 2], [0, 3]],), False),
                (([],), True),
            ),
        ),
    ]
