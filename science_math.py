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


def try_calculus(text: str) -> Optional[Dict[str, Any]]:
    """Derivative / integral / simplify / solve simple equations."""
    if not _SYMPY:
        return None
    t = text.strip()
    low = t.lower()

    # second derivative
    m = re.search(r"second derivative of\s+(.+?)(?:\s+with respect to\s+(\w+))?$", t, re.I)
    if m:
        expr_s = m.group(1).strip().rstrip(".")
        var_s = (m.group(2) or "x")
        var = sp.Symbol(var_s)
        expr = _sym(expr_s)
        d2 = sp.diff(expr, var, 2)
        return {
            "ok": True,
            "kind": "derivative",
            "expression": expr_s,
            "result": str(d2),
            "pretty": f"d²/d{var_s}²({expr_s}) = {d2}",
        }


    # d/dx f  or  derivative of f
    m = re.search(
        r"(?:derivative of|differentiate|d/dx|d/d([a-z]))\s+(.+?)(?:\s+with respect to\s+(\w+))?$",
        t,
        re.I,
    )
    if m or re.search(r"\bderivative\b|\bdifferentiate\b", low):
        m2 = re.search(
            r"(?:derivative of|differentiate)\s+(.+?)(?:\s+with respect to\s+(\w+))?$",
            t,
            re.I,
        )
        m3 = re.search(r"d/d([a-z])\s*\(?\s*(.+?)\s*\)?\s*$", t, re.I)
        expr_s, var_s = None, "x"
        if m2:
            expr_s, var_s = m2.group(1).strip(), (m2.group(2) or "x")
        elif m3:
            var_s, expr_s = m3.group(1), m3.group(2).strip()
        if expr_s:
            expr_s = expr_s.rstrip(".")
            var = sp.Symbol(var_s)
            expr = _sym(expr_s)
            deriv = sp.diff(expr, var)
            return {
                "ok": True,
                "kind": "derivative",
                "expression": expr_s,
                "result": str(deriv),
                "pretty": f"d/d{var_s}({expr_s}) = {deriv}",
            }

    # integral of f dx
    m = re.search(
        r"(?:integral of|integrate)\s+(.+?)(?:\s*(?:d|with respect to)\s*(\w+))?$",
        t,
        re.I,
    )
    if m:
        expr_s = m.group(1).strip().rstrip(".")
        # strip trailing dx if glued
        expr_s = re.sub(r"\s*d([a-z])\s*$", "", expr_s, flags=re.I)
        var_s = (m.group(2) or "x").strip()
        var = sp.Symbol(var_s)
        expr = _sym(expr_s)
        integ = sp.integrate(expr, var)
        return {
            "ok": True,
            "kind": "integral",
            "expression": expr_s,
            "result": str(integ),
            "pretty": f"∫ {expr_s} d{var_s} = {integ} + C",
        }
    # limit as x -> a of f
    m = re.search(
        r"limit as\s+(\w+)\s*(?:approaches|->|→)\s*([\w.]+)\s+of\s+(.+)$",
        t,
        re.I,
    )
    if m:
        var_s, at, expr_s = m.group(1), m.group(2), m.group(3).strip().rstrip(".")
        var = sp.Symbol(var_s)
        at_val = sp.oo if at.lower() in ("inf", "infinity", "oo") else _sym(at)
        expr = _sym(expr_s)
        lim = sp.limit(expr, var, at_val)
        return {
            "ok": True,
            "kind": "limit",
            "expression": expr_s,
            "result": str(lim),
            "pretty": f"lim_{{{var_s}→{at}}} {expr_s} = {lim}",
        }

    # solve equation
    m = re.search(r"solve\s+(.+)", t, re.I)
    if m:
        eq = m.group(1).strip()
        if "=" in eq:
            left, right = eq.split("=", 1)
            x = sp.Symbol("x")
            sols = sp.solve(sp.Eq(_sym(left), _sym(right)), x)
            return {
                "ok": True,
                "kind": "solve",
                "expression": eq,
                "result": str(sols),
                "pretty": f"Solutions: {sols}",
            }

    return None


def try_geometry(text: str) -> Optional[Dict[str, Any]]:
    t = text.lower()
    # circle area
    m = re.search(r"area of (?:a )?circle.*?(?:radius|r)\s*[:=]?\s*([\d.]+)", t)
    if not m:
        m = re.search(r"circle.*?radius\s*([\d.]+).*area", t)
    if m:
        r = float(m.group(1))
        a = math.pi * r * r
        return {"ok": True, "kind": "geometry", "pretty": f"Area of circle (r={r}) = {a:.6g} (πr²)", "result": a}

    m = re.search(r"circumference (?:of )?(?:a )?circle.*?(?:radius|r)\s*[:=]?\s*([\d.]+)", t)
    if m:
        r = float(m.group(1))
        c = 2 * math.pi * r
        return {"ok": True, "kind": "geometry", "pretty": f"Circumference (r={r}) = {c:.6g} (2πr)", "result": c}

    m = re.search(r"area of (?:a )?triangle.*?base\s*[:=]?\s*([\d.]+).*height\s*[:=]?\s*([\d.]+)", t)
    if m:
        b, h = float(m.group(1)), float(m.group(2))
        a = 0.5 * b * h
        return {"ok": True, "kind": "geometry", "pretty": f"Area of triangle = {a:.6g} (½·{b}·{h})", "result": a}

    m = re.search(r"area of (?:a )?rectangle.*?length\s*[:=]?\s*([\d.]+).*width\s*[:=]?\s*([\d.]+)", t)
    if m:
        L, W = float(m.group(1)), float(m.group(2))
        a = L * W
        return {"ok": True, "kind": "geometry", "pretty": f"Area of rectangle = {a:.6g} ({L}×{W})", "result": a}

    m = re.search(r"pythagorean|hypotenuse.*?([\d.]+).*?([\d.]+)", t)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        c = math.hypot(a, b)
        return {"ok": True, "kind": "geometry", "pretty": f"Hypotenuse = {c:.6g} (√({a}²+{b}²))", "result": c}

    m = re.search(r"volume of (?:a )?sphere.*?radius\s*[:=]?\s*([\d.]+)", t)
    if m:
        r = float(m.group(1))
        v = (4 / 3) * math.pi * r**3
        return {"ok": True, "kind": "geometry", "pretty": f"Volume of sphere (r={r}) = {v:.6g} (⁴⁄₃πr³)", "result": v}

    m = re.search(r"surface area of (?:a )?sphere.*?radius\s*[:=]?\s*([\d.]+)", t)
    if m:
        r = float(m.group(1))
        a = 4 * math.pi * r * r
        return {"ok": True, "kind": "geometry", "pretty": f"Surface area of sphere (r={r}) = {a:.6g} (4πr²)", "result": a}

    m = re.search(r"volume of (?:a )?(?:box|rectangular prism|cuboid).*?l(?:ength)?\s*[:=]?\s*([\d.]+).*?w(?:idth)?\s*[:=]?\s*([\d.]+).*?h(?:eight)?\s*[:=]?\s*([\d.]+)", t)
    if m:
        L, W, H = float(m.group(1)), float(m.group(2)), float(m.group(3))
        v = L * W * H
        return {"ok": True, "kind": "geometry", "pretty": f"Volume of box = {v:g} ({L}×{W}×{H})", "result": v}

    m = re.search(r"volume of (?:a )?cylinder.*?radius\s*[:=]?\s*([\d.]+).*?height\s*[:=]?\s*([\d.]+)", t)
    if m:
        r, h = float(m.group(1)), float(m.group(2))
        v = math.pi * r * r * h
        return {"ok": True, "kind": "geometry", "pretty": f"Volume of cylinder (r={r}, h={h}) = {v:.6g} (πr²h)", "result": v}

    m = re.search(r"distance between.*?\(?\s*([\d.-]+)\s*,\s*([\d.-]+)\s*\)?.*?\(?\s*([\d.-]+)\s*,\s*([\d.-]+)\s*\)?", t)
    if m:
        x1, y1, x2, y2 = map(float, m.groups())
        d = math.hypot(x2 - x1, y2 - y1)
        return {"ok": True, "kind": "geometry", "pretty": f"Distance = {d:.6g}", "result": d}


    return None


def try_physics(text: str) -> Optional[Dict[str, Any]]:
    t = text.lower()
    # F = m a  (numbers may have units between them)
    m = re.search(
        r"(?:force|f\s*=).*?mass\s*[:=]?\s*([\d.]+).*?accel(?:eration)?\s*[:=]?\s*([\d.]+)",
        t,
    )
    if not m:
        m = re.search(
            r"mass\s*[:=]?\s*([\d.]+).*?accel(?:eration)?\s*[:=]?\s*([\d.]+)",
            t,
        )
    if m and ("force" in t or "newton" in t or "f=" in t.replace(" ", "")):
        mass, acc = float(m.group(1)), float(m.group(2))
        f = mass * acc
        return {"ok": True, "kind": "physics", "pretty": f"Force F = m·a = {mass}×{acc} = {f:g} N", "result": f}
    if m and re.search(r"\bforce\b", t):
        mass, acc = float(m.group(1)), float(m.group(2))
        f = mass * acc
        return {"ok": True, "kind": "physics", "pretty": f"Force F = m·a = {mass}×{acc} = {f:g} N", "result": f}

    # KE = 1/2 m v^2
    m = re.search(
        r"kinetic energy.*?(?:mass|m)\s*[:=]?\s*([\d.]+).*?(?:velocity|speed|v)\s*[:=]?\s*([\d.]+)",
        t,
    )
    if m:
        mass, v = float(m.group(1)), float(m.group(2))
        ke = 0.5 * mass * v * v
        return {"ok": True, "kind": "physics", "pretty": f"KE = ½mv² = {ke:g} J", "result": ke}

    # PE = m g h
    m = re.search(
        r"(?:potential energy|pe).*?(?:mass|m)\s*[:=]?\s*([\d.]+).*?(?:height|h)\s*[:=]?\s*([\d.]+)",
        t,
    )
    if m:
        mass, h = float(m.group(1)), float(m.group(2))
        pe = mass * 9.81 * h
        return {"ok": True, "kind": "physics", "pretty": f"PE = mgh = {mass}×9.81×{h} = {pe:g} J", "result": pe}

    # v = d/t
    m = re.search(
        r"speed|velocity.*?(?:distance|d)\s*[:=]?\s*([\d.]+).*?(?:time|t)\s*[:=]?\s*([\d.]+)",
        t,
    )
    if m:
        d, tm = float(m.group(1)), float(m.group(2))
        if tm != 0:
            v = d / tm
            return {"ok": True, "kind": "physics", "pretty": f"v = d/t = {d}/{tm} = {v:g}", "result": v}

    # Ohm V = IR
    m = re.search(
        r"(?:voltage|ohm).*?(?:current|i)\s*[:=]?\s*([\d.]+).*?(?:resistance|r)\s*[:=]?\s*([\d.]+)",
        t,
    )
    if m:
        i, r = float(m.group(1)), float(m.group(2))
        v = i * r
        return {"ok": True, "kind": "physics", "pretty": f"V = IR = {i}×{r} = {v:g} V", "result": v}

    # density = m/V
    m = re.search(r"density.*?mass\s*[:=]?\s*([\d.]+).*?volume\s*[:=]?\s*([\d.]+)", t)
    if m:
        mass, vol = float(m.group(1)), float(m.group(2))
        if vol != 0:
            dens = mass / vol
            return {"ok": True, "kind": "physics", "pretty": f"Density ρ = m/V = {mass}/{vol} = {dens:g}", "result": dens}

    # momentum p = mv
    m = re.search(r"momentum.*?mass\s*[:=]?\s*([\d.]+).*?(?:velocity|speed)\s*[:=]?\s*([\d.]+)", t)
    if m:
        mass, v = float(m.group(1)), float(m.group(2))
        p = mass * v
        return {"ok": True, "kind": "physics", "pretty": f"Momentum p = mv = {mass}×{v} = {p:g}", "result": p}

    # work W = F d
    m = re.search(r"work.*?(?:force|f)\s*[:=]?\s*([\d.]+).*?(?:distance|d)\s*[:=]?\s*([\d.]+)", t)
    if m:
        f, d = float(m.group(1)), float(m.group(2))
        w = f * d
        return {"ok": True, "kind": "physics", "pretty": f"Work W = F·d = {f}×{d} = {w:g} J", "result": w}

    # simple interest I = P r t
    m = re.search(r"simple interest.*?principal\s*[:=]?\s*([\d.]+).*?rate\s*[:=]?\s*([\d.]+).*?time\s*[:=]?\s*([\d.]+)", t)
    if m:
        P, r, tm = float(m.group(1)), float(m.group(2)), float(m.group(3))
        # rate may be percent
        if r > 1:
            r = r / 100.0
        I = P * r * tm
        return {"ok": True, "kind": "physics", "pretty": f"Simple interest I = Prt = {I:g}", "result": I}


    return None




def try_units_convert(text: str) -> Optional[Dict[str, Any]]:
    """Simple unit conversions (Cycle 70)."""
    t = text.lower()
    m = re.search(r"([\d.]+)\s*(km|kilometers?)\s+(?:to|in)\s+(m|meters?)\b", t)
    if m:
        v = float(m.group(1)) * 1000
        return {"ok": True, "kind": "units", "pretty": f"{m.group(1)} km = {v:g} m", "result": v}
    m = re.search(r"([\d.]+)\s*(m|meters?)\s+(?:to|in)\s+(km|kilometers?)\b", t)
    if m:
        v = float(m.group(1)) / 1000
        return {"ok": True, "kind": "units", "pretty": f"{m.group(1)} m = {v:g} km", "result": v}
    m = re.search(r"([\d.]+)\s*(c|celsius|°c)\s+(?:to|in)\s+(f|fahrenheit|°f)\b", t)
    if m:
        c = float(m.group(1))
        f = c * 9 / 5 + 32
        return {"ok": True, "kind": "units", "pretty": f"{c:g} °C = {f:g} °F", "result": f}
    m = re.search(r"([\d.]+)\s*(f|fahrenheit|°f)\s+(?:to|in)\s+(c|celsius|°c)\b", t)
    if m:
        f = float(m.group(1))
        c = (f - 32) * 5 / 9
        return {"ok": True, "kind": "units", "pretty": f"{f:g} °F = {c:g} °C", "result": c}
    m = re.search(r"([\d.]+)\s*(kg|kilograms?)\s+(?:to|in)\s+(g|grams?)\b", t)
    if m:
        v = float(m.group(1)) * 1000
        return {"ok": True, "kind": "units", "pretty": f"{m.group(1)} kg = {v:g} g", "result": v}
    return None


def solve_science_math(text: str) -> Dict[str, Any]:
    """
    Try calculus → geometry → physics.
    Returns {ok, pretty/result, kind} or {ok: False, error}.
    """
    for fn in (try_calculus, try_geometry, try_physics, try_units_convert):
        try:
            out = fn(text)
        except Exception as e:
            return {"ok": False, "error": str(e), "kind": fn.__name__}
        if out and out.get("ok"):
            return out
    return {"ok": False, "error": "no closed-form science/math match", "kind": None}


def looks_like_science_math(text: str) -> bool:
    low = (text or "").lower()
    keys = (
        "derivative", "differentiate", "integral", "integrate", "d/dx", "limit", "second derivative",
        "area of", "circumference", "volume of", "triangle", "circle",
        "rectangle", "sphere", "hypotenuse", "pythagorean",
        "force", "mass", "acceleration", "kinetic energy", "potential energy",
        "velocity", "newton", "ohm", "voltage", "density", "momentum", "work",
        "surface area", "cylinder", "cuboid", "interest", "celsius", "fahrenheit", "kilometers",
        "calculus", "geometry", "physics",
    )
    return any(k in low for k in keys)
