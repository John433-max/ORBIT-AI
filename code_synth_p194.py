"""Cycle 477: point geometry and angle conversion misses.

Loaded before p180 so polar→cartesian is not claimed by cartesian_to_polar
(that matcher only requires both words). Slope, distance, and midpoint were
NotImplemented drafts. Degrees/radians require an explicit direction.
Ellipse area is pi*a*b and does not match circle asks.
"""
from __future__ import annotations

from code_synth import Template

_PI = 3.141592653589793


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "slope",
            "def slope(x1, y1, x2, y2):\n"
            '    """Slope (y2-y1)/(x2-x1). Vertical lines raise ZeroDivisionError."""\n'
            "    dx = float(x2) - float(x1)\n"
            "    if dx == 0.0:\n"
            "        raise ZeroDivisionError('vertical line')\n"
            "    return (float(y2) - float(y1)) / dx\n",
            lambda low: (
                "slope" in low
                and "point" in low
                and "intercept" not in low
            ),
            (
                ((0, 0, 2, 2), 1.0),
                ((1, 1, 3, 5), 2.0),
                ((0, 4, 4, 0), -1.0),
            ),
        ),
        T(
            "point_distance",
            "def point_distance(x1, y1, x2, y2):\n"
            '    """Euclidean distance between two points, rounded to 6 decimals."""\n'
            "    import math\n"
            "    return round(math.hypot(float(x2) - float(x1), float(y2) - float(y1)), 6)\n",
            lambda low: (
                "distance" in low
                and "point" in low
                and "edit" not in low
                and "hamming" not in low
                and "levenshtein" not in low
                and "manhattan" not in low
                and "chebyshev" not in low
                and "euclidean" not in low
            ),
            (
                ((0, 0, 3, 4), 5.0),
                ((1, 1, 1, 1), 0.0),
                ((0, 0, 1, 0), 1.0),
            ),
        ),
        T(
            "midpoint",
            "def midpoint(x1, y1, x2, y2):\n"
            '    """Midpoint of two points as (x, y)."""\n'
            "    return ((float(x1) + float(x2)) / 2.0, (float(y1) + float(y2)) / 2.0)\n",
            lambda low: "midpoint" in low and "point" in low,
            (
                ((0, 0, 2, 4), (1.0, 2.0)),
                ((1, 1, 1, 1), (1.0, 1.0)),
                ((-2, 4, 2, 0), (0.0, 2.0)),
            ),
        ),
        T(
            "degrees_to_radians",
            "def degrees_to_radians(degrees):\n"
            '    """Degrees to radians, rounded to 6 decimals."""\n'
            "    import math\n"
            "    return round(math.radians(float(degrees)), 6)\n",
            lambda low: (
                "degree" in low
                and "radian" in low
                and "to radian" in low
            ),
            (
                ((0,), 0.0),
                ((180,), 3.141593),
                ((90,), 1.570796),
            ),
        ),
        T(
            "radians_to_degrees",
            "def radians_to_degrees(radians):\n"
            '    """Radians to degrees, rounded to 6 decimals."""\n'
            "    import math\n"
            "    return round(math.degrees(float(radians)), 6)\n",
            lambda low: (
                "radian" in low
                and "degree" in low
                and "to degree" in low
            ),
            (
                ((0,), 0.0),
                ((3.141592653589793,), 180.0),
                ((1.5707963267948966,), 90.0),
            ),
        ),
        T(
            "ellipse_area",
            "def ellipse_area(a, b):\n"
            '    """Ellipse area pi*a*b, rounded to 6 decimals."""\n'
            f"    return round({_PI} * float(a) * float(b), 6)\n",
            lambda low: "ellipse" in low and "area" in low and "circle" not in low,
            (
                ((1, 1), 3.141593),
                ((2, 3), 18.849556),
                ((0, 5), 0.0),
            ),
        ),
        T(
            "polar_to_cartesian",
            "def polar_to_cartesian(r, degrees):\n"
            '    """Polar (radius, degrees) to cartesian (x, y), rounded to 6 decimals."""\n'
            "    import math\n"
            "    rad = math.radians(float(degrees))\n"
            "    return (round(float(r) * math.cos(rad), 6), round(float(r) * math.sin(rad), 6))\n",
            lambda low: (
                "polar" in low
                and "cartesian" in low
                and "to cartesian" in low
                and "to polar" not in low
            ),
            (
                ((1, 0), (1.0, 0.0)),
                ((1, 90), (0.0, 1.0)),
                ((2, 180), (-2.0, 0.0)),
            ),
        ),
    ]
