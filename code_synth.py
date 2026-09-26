"""Deterministic TinyLM-free templates for 'write a python function…' asks.

Cycle 207: each template carries tiny examples so CodeAgent can self-check
the generated body (HumanEval-style pass/fail) without calling the LLM.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable, Sequence


@dataclass(frozen=True)
class Template:
    name: str
    source: str
    match: Callable[[str], bool]
    examples: Sequence[tuple]  # (args_tuple, expected)


def _low(request: str) -> str:
    return (request or "").lower()


_TWO = r"(two|2|a pair of)"


def _templates() -> list[Template]:
    return [
        Template(
            "add",
            "def add(a, b):\n"
            '    """Return the sum of a and b."""\n'
            "    return a + b\n",
            lambda low: bool(
                re.search(r"add(s|ing)?\b.{0,24}\b" + _TWO + r"\b.{0,24}\b(number|int|value)", low)
                or "adds two" in low
            ),
            (((1, 2), 3), ((-4, 10), 6)),
        ),
        Template(
            "multiply",
            "def multiply(a, b):\n"
            '    """Return the product of a and b."""\n'
            "    return a * b\n",
            lambda low: bool(re.search(r"\b(multipl(?:y|ies|ied|ying)|product of)\b.{0,40}\b" + _TWO + r"\b", low)),
            (((3, 4), 12), ((-2, 5), -10)),
        ),
        Template(
            "subtract",
            "def subtract(a, b):\n"
            '    """Return a minus b."""\n'
            "    return a - b\n",
            lambda low: bool(re.search(r"\b(subtract(?:s|ing)?|difference (of|between)|minus)\b.{0,40}\b" + _TWO, low)),
            (((9, 4), 5), ((0, 3), -3)),
        ),
        Template(
            "maximum",
            "def maximum(a, b):\n"
            '    """Return the larger of a and b."""\n'
            "    return a if a >= b else b\n",
            lambda low: bool(re.search(r"\b(max(?:imum)?|larger|greater)\b.{0,40}\b" + _TWO, low)),
            (((2, 9), 9), ((-1, -8), -1)),
        ),
        Template(
            "minimum",
            "def minimum(a, b):\n"
            '    """Return the smaller of a and b."""\n'
            "    return a if a <= b else b\n",
            lambda low: bool(re.search(r"\b(min(?:imum)?|smaller|lesser)\b.{0,40}\b" + _TWO, low)),
            (((2, 9), 2), ((-1, -8), -8)),
        ),
        Template(
            "reverse_string",
            "def reverse_string(s):\n"
            '    """Return s reversed."""\n'
            "    return s[::-1]\n",
            lambda low: bool(re.search(r"\breverse\b.{0,40}\b(string|str|text)\b|\b(string|str|text)\b.{0,20}\breverse", low)),
            ((("ab",), "ba"), (("Orbit",), "tibrO")),
        ),
        Template(
            "factorial",
            "def factorial(n):\n"
            '    """Return n! for n >= 0."""\n'
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    out = 1\n"
            "    for i in range(2, n + 1):\n"
            "        out *= i\n"
            "    return out\n",
            lambda low: "factorial" in low,
            (((0,), 1), ((5,), 120)),
        ),
        Template(
            "divide",
            "def divide(a, b):\n"
            '    """Return a / b. Raises ZeroDivisionError if b is 0."""\n'
            "    return a / b\n",
            lambda low: bool(re.search(r"\b(divid(?:e|es|ing)|quotient of)\b.{0,40}\b" + _TWO, low)),
            (((10, 4), 2.5), ((9, 3), 3.0)),
        ),
        Template(
            "average",
            "def average(a, b):\n"
            '    """Return the arithmetic mean of a and b."""\n'
            "    return (a + b) / 2\n",
            lambda low: bool(re.search(r"\b(averag(?:e|es|ing)|mean)\b.{0,40}\b(two|2|list|numbers)\b", low)),
            (((2, 4), 3.0), ((0, 5), 2.5)),
        ),
        Template(
            "absolute",
            "def absolute(n):\n"
            '    """Return the absolute value of n."""\n'
            "    return n if n >= 0 else -n\n",
            lambda low: bool(re.search(r"absolute value|\babs\b", low)),
            (((-3,), 3), ((4,), 4)),
        ),
        Template(
            "power",
            "def power(base, exp):\n"
            '    """Return base raised to exp."""\n'
            "    return base ** exp\n",
            lambda low: bool(re.search(r"\b(power|exponent|raise .+ to)\b", low)),
            (((2, 10), 1024), ((3, 0), 1)),
        ),
        Template(
            "sort_list",
            "def sort_list(items):\n"
            '    """Return a new list with items in ascending order."""\n'
            "    return sorted(items)\n",
            lambda low: bool(re.search(r"\b(sort(?:s|ing)?|sorted)\b.{0,40}\b(list|array|numbers|items)\b", low)),
            ((([3, 1, 2],), [1, 2, 3]),),
        ),
        Template(
            "is_palindrome",
            "def is_palindrome(s):\n"
            '    """Return True if s reads the same forwards and backwards."""\n'
            "    t = ''.join(ch.lower() for ch in str(s) if ch.isalnum())\n"
            "    return t == t[::-1]\n",
            lambda low: "palindrome" in low,
            ((("Racecar",), True), (("orbit",), False)),
        ),
        Template(
            "is_even",
            "def is_even(n):\n"
            '    """Return True if n is even."""\n'
            "    return n % 2 == 0\n",
            lambda low: bool(re.search(r"\b(even|is_even|even number)\b", low)),
            (((4,), True), ((7,), False)),
        ),
        Template(
            "gcd",
            "def gcd(a, b):\n"
            '    """Return the greatest common divisor of a and b."""\n'
            "    a, b = abs(int(a)), abs(int(b))\n"
            "    while b:\n"
            "        a, b = b, a % b\n"
            "    return a\n",
            lambda low: bool(re.search(r"\b(gcd|greatest common divisor|hcf)\b", low)),
            (((48, 18), 6), ((7, 13), 1)),
        ),
        Template(
            "fibonacci",
            "def fibonacci(n):\n"
            '    """Return the n-th Fibonacci number (F(0)=0, F(1)=1)."""\n'
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    a, b = 0, 1\n"
            "    for _ in range(n):\n"
            "        a, b = b, a + b\n"
            "    return a\n",
            lambda low: bool(re.search(r"\bfibonacci\b|\bfib\b", low)),
            (((0,), 0), ((10,), 55)),
        ),
        Template(
            "count_vowels",
            "def count_vowels(s):\n"
            '    """Return the number of English vowels in s."""\n'
            "    return sum(1 for ch in str(s).lower() if ch in 'aeiou')\n",
            lambda low: bool(re.search(r"\bcount(?:s|ing)?\b.{0,32}\bvowels?\b|\bvowels?\b.{0,24}\bcount|\bnumber of vowels\b", low)),
            ((("Orbit AI",), 4), (("xyz",), 0)),
        ),
        Template(
            "unique",
            "def unique(items):\n"
            '    """Return items with duplicates removed, first-seen order kept."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for x in items:\n"
            "        if x not in seen:\n"
            "            seen.add(x)\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(re.search(r"\b(unique|dedup|duplicates?)\b.{0,24}\b(list|array|items)\b", low)),
            ((([1, 2, 1, 3],), [1, 2, 3]),),
        ),
        Template(
            "is_odd",
            "def is_odd(n):\n"
            '    """Return True if n is odd."""\n'
            "    return n % 2 != 0\n",
            lambda low: bool(re.search(r"\b(odd|is_odd|odd number)\b", low)),
            (((3,), True), ((8,), False)),
        ),
        Template(
            "sum_list",
            "def sum_list(items):\n"
            '    """Return the sum of items."""\n'
            "    total = 0\n"
            "    for x in items:\n"
            "        total += x\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\b(sum(?:s|ming)?|total)\b.{0,32}\b(list|array|items|numbers)\b|"
                    r"\b(list|array|items|numbers)\b.{0,24}\bsum\b",
                    low,
                )
            ),
            ((([1, 2, 3],), 6), (([],), 0)),
        ),
    ]


TEMPLATES = _templates()


def match_template(request: str) -> Template | None:
    low = _low(request)
    for tmpl in TEMPLATES:
        try:
            if tmpl.match(low):
                return tmpl
        except Exception:
            continue
    return None


def fallback_source(request: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", _low(request))[:40].strip("_") or "solve"
    return (
        f"def {slug}(*args, **kwargs):\n"
        f'    """Draft from: {(request or "").strip()[:120]}"""\n'
        "    raise NotImplementedError('Paste a fenced snippet to run it, or specify the function body.')\n"
    )


def synthesize_python(request: str) -> str:
    tmpl = match_template(request)
    if tmpl is None:
        return fallback_source(request)
    return tmpl.source


def verify_source(source: str, examples: Sequence[tuple] | None = None) -> dict[str, Any]:
    """Exec a trusted template and check (args, expected) pairs.

    Used only on code_synth templates, never on raw user code.
    """
    ns: dict[str, Any] = {}
    try:
        exec(source, ns, ns)  # noqa: S102 — static templates only
    except Exception as exc:
        return {"ok": False, "error": str(exc), "checked": 0}
    fn = None
    for name, val in ns.items():
        if name.startswith("_"):
            continue
        if callable(val):
            fn = val
            break
    if fn is None:
        return {"ok": False, "error": "no function defined", "checked": 0}
    if not examples:
        return {"ok": True, "checked": 0, "name": getattr(fn, "__name__", "?")}
    checked = 0
    try:
        for args, expected in examples:
            got = fn(*args)
            if got != expected:
                return {
                    "ok": False,
                    "error": f"{fn.__name__}{args} -> {got!r} != {expected!r}",
                    "checked": checked,
                    "name": fn.__name__,
                }
            checked += 1
    except Exception as exc:
        return {"ok": False, "error": str(exc), "checked": checked, "name": getattr(fn, "__name__", "?")}
    return {"ok": True, "checked": checked, "name": fn.__name__}


def synthesize_and_verify(request: str) -> dict[str, Any]:
    tmpl = match_template(request)
    if tmpl is None:
        src = fallback_source(request)
        return {"source": src, "verified": False, "name": None, "checked": 0, "fallback": True}
    check = verify_source(tmpl.source, tmpl.examples)
    return {
        "source": tmpl.source,
        "verified": bool(check.get("ok")),
        "name": tmpl.name,
        "checked": int(check.get("checked") or 0),
        "fallback": False,
        "error": check.get("error"),
    }


# alias used by agents.py
_synthesize_python = synthesize_python
