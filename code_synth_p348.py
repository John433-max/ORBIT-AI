"""Cycle 641 (p348): stooge_sort for CI unit tests."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "stooge_sort",
            '''def stooge_sort(arr):
    """Recursive stooge sort (educational). Returns a new sorted list."""
    a = list(arr)
    def _stooge(i, j):
        if a[i] > a[j]:
            a[i], a[j] = a[j], a[i]
        if j - i + 1 > 2:
            t = (j - i + 1) // 3
            _stooge(i, j - t)
            _stooge(i + t, j)
            _stooge(i, j - t)
    if a:
        _stooge(0, len(a) - 1)
    return a
''',
            lambda low: bool(re.search(r"\bstooge[- ]?sort\b", low)),
            (
                (([3, 1, 2],), [1, 2, 3]),
            ),
        ),
    ]
