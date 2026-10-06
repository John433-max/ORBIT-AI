"""Cycle 477: rectangle diagonal, rhombus, prism, pyramid.

Loaded before older geometry packs so diagonal is not claimed by rectangle
area/perimeter, rhombus is not claimed by parallelogram, and prism/pyramid
are not claimed by cube or cone volume.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "rectangle_diagonal",
            "def rectangle_diagonal(width, height):\n"
            '    """Diagonal of a rectangle, sqrt(width^2 + height^2)."""\n'
            "    return (float(width) ** 2 + float(height) ** 2) ** 0.5\n",
            lambda low: (
                "rectangle" in low
                and "diagonal" in low
                and "area" not in low
                and "perimeter" not in low
            ),
            (
                ((3, 4), 5.0),
                ((0, 0), 0.0),
                ((6, 8), 10.0),
            ),
        ),
        T(
            "rhombus_area",
            "def rhombus_area(d1, d2):\n"
            '    """Rhombus area from diagonals: d1 * d2 / 2."""\n'
            "    return float(d1) * float(d2) / 2.0\n",
            lambda low: (
                "rhombus" in low
                and "area" in low
                and "perimeter" not in low
                and "parallelogram" not in low
            ),
            (
                ((4, 6), 12.0),
                ((0, 5), 0.0),
                ((3, 3), 4.5),
            ),
        ),
        T(
            "rhombus_perimeter",
            "def rhombus_perimeter(side):\n"
            '    """Rhombus perimeter is 4 * side."""\n'
            "    return 4.0 * float(side)\n",
            lambda low: (
                "rhombus" in low
                and "perimeter" in low
                and "area" not in low
            ),
            (
                ((5,), 20.0),
                ((0,), 0.0),
                ((1.5,), 6.0),
            ),
        ),
        T(
            "rectangular_prism_volume",
            "def rectangular_prism_volume(length, width, height):\n"
            '    """Rectangular prism volume length * width * height."""\n'
            "    return float(length) * float(width) * float(height)\n",
            lambda low: (
                "rectangular" in low
                and "prism" in low
                and "volume" in low
                and "surface" not in low
                and "cube" not in low
            ),
            (
                ((2, 3, 4), 24.0),
                ((0, 5, 5), 0.0),
                ((1.5, 2, 2), 6.0),
            ),
        ),
        T(
            "rectangular_prism_surface_area",
            "def rectangular_prism_surface_area(length, width, height):\n"
            '    """Rectangular prism surface 2 * (lw + lh + wh)."""\n'
            "    l, w, h = float(length), float(width), float(height)\n"
            "    return 2.0 * (l * w + l * h + w * h)\n",
            lambda low: (
                "rectangular" in low
                and "prism" in low
                and "surface" in low
                and "volume" not in low
            ),
            (
                ((2, 3, 4), 52.0),
                ((1, 1, 1), 6.0),
                ((0, 2, 3), 12.0),
            ),
        ),
        T(
            "pyramid_volume",
            "def pyramid_volume(length, width, height):\n"
            '    """Right rectangular pyramid volume (l * w * h) / 3."""\n'
            "    return float(length) * float(width) * float(height) / 3.0\n",
            lambda low: (
                "pyramid" in low
                and "volume" in low
                and "cone" not in low
                and "surface" not in low
            ),
            (
                ((3, 3, 3), 9.0),
                ((2, 3, 6), 12.0),
                ((0, 4, 5), 0.0),
            ),
        ),
    ]
