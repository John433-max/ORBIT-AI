"""
Calculus / geometry / physics helpers (Cycle 59).

Uses sympy when available for derivatives/integrals/algebra.
Geometry + intro physics are closed-form. Open science → caller may search.
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, Optional

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr,
        standard_transformations,
        implicit_multiplication_application,
        convert_xor,
    )
    _SYMPY = True
    _TRANSFORMS = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )
except ImportError:
    _SYMPY = False
    sp = None  # type: ignore


def _num(x) -> float:
    if hasattr(x, "evalf"):
        x = x.evalf()
    return float(x)


def _sym(expr: str):
    if not _SYMPY:
        raise RuntimeError("sympy not installed")
    return parse_expr(expr, transformations=_TRANSFORMS)
