"""Deterministic TinyLM-free templates for 'write a python function…' asks."""
from __future__ import annotations

import re


def synthesize_python(request: str) -> str:
    low = (request or "").lower()
    two = r"(two|2|a pair of)"
    if re.search(r"add(s|ing)?\b.{0,24}\b" + two + r"\b.{0,24}\b(number|int|value)", low) or "adds two" in low:
        return (
            "def add(a, b):\n"
            '    """Return the sum of a and b."""\n'
            "    return a + b\n"
        )
    if re.search(r"\b(multipl(?:y|ies|ied|ying)|product of)\b.{0,40}\b" + two + r"\b", low):
        return (
            "def multiply(a, b):\n"
            '    """Return the product of a and b."""\n'
            "    return a * b\n"
        )
    if re.search(r"\b(subtract(?:s|ing)?|difference (of|between)|minus)\b.{0,40}\b" + two, low):
        return (
            "def subtract(a, b):\n"
            '    """Return a minus b."""\n'
            "    return a - b\n"
        )
    if re.search(r"\b(max(?:imum)?|larger|greater)\b.{0,40}\b" + two, low):
        return (
            "def maximum(a, b):\n"
            '    """Return the larger of a and b."""\n'
            "    return a if a >= b else b\n"
        )
    if re.search(r"\b(min(?:imum)?|smaller|lesser)\b.{0,40}\b" + two, low):
        return (
            "def minimum(a, b):\n"
            '    """Return the smaller of a and b."""\n'
            "    return a if a <= b else b\n"
        )
    if re.search(r"\breverse\b.{0,40}\b(string|str|text)\b|\b(string|str|text)\b.{0,20}\breverse", low):
        return (
            "def reverse_string(s):\n"
            '    """Return s reversed."""\n'
            "    return s[::-1]\n"
        )
    if re.search(r"\bfactorial\b", low):
        return (
            "def factorial(n):\n"
            '    """Return n! for n >= 0."""\n'
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    out = 1\n"
            "    for i in range(2, n + 1):\n"
            "        out *= i\n"
            "    return out\n"
        )
    slug = re.sub(r"[^a-z0-9]+", "_", low)[:40].strip("_") or "solve"
    return (
        f"def {slug}(*args, **kwargs):\n"
        f'    """Draft from: {(request or "").strip()[:120]}"""\n'
        "    raise NotImplementedError('Paste a fenced snippet to run it, or specify the function body.')\n"
    )


_synthesize_python = synthesize_python
