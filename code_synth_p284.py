"""Cycle 586: Newton interpolation, linear algebra, SAM, geometry, lazy segtree.

newton_interpolation, matrix_determinant, solve_linear_system,
count_distinct_substrings (suffix automaton), min_area_bounding_rectangle,
lazy_segment_tree.
"""
from __future__ import annotations

import math
import re
from typing import Sequence

from code_synth import Template


def templates() -> list[Template]:
    return [
        Template(
            "newton_interpolation",
            '''def newton_interpolation(xs, ys, x):
    """Newton divided-difference interpolation. Returns p(x).

    Builds divided-difference coefficients then evaluates the Newton form.
    Educational pure-Python implementation.
    """
    n = len(xs)
    if n == 0 or n != len(ys):
        raise ValueError('xs and ys must be non-empty and same length')
    coef = list(ys)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            denom = xs[i] - xs[i - j]
            if denom == 0:
                raise ValueError('duplicate x')
            coef[i] = (coef[i] - coef[i - 1]) / denom
    result = coef[-1]
    for i in range(n - 2, -1, -1):
        result = result * (x - xs[i]) + coef[i]
    return result
''',
            lambda low: bool(
                re.search(r"newton.*divided|divided.?difference|newton.?interpolat", low)
            ),
            (
                (([0, 1, 2], [1, 2, 4], 1), 2),
                (([0, 1, 2], [1, 3, 7], 1.5), 4.75),
                (([1, 2], [3, 5], 1.5), 4.0),
            ),
        ),
    ]
