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
    """Load split packs (Cycle 244). Missing packs are skipped so CI still collects."""
    import importlib
    out: list[Template] = []
    for name in ("code_synth_p1", "code_synth_p2", "code_synth_p3"):
        try:
            mod = importlib.import_module(name)
        except Exception:
            continue
        fn = getattr(mod, "templates", None)
        if callable(fn):
            out.extend(fn())
    return out


def get_templates() -> list[Template]:
    global TEMPLATES
    cached = globals().get("_TEMPLATES_CACHE")
    if cached is not None:
        return cached
    loaded = _templates()
    globals()["_TEMPLATES_CACHE"] = loaded
    TEMPLATES = loaded
    return loaded



def __getattr__(name: str):
    if name == "TEMPLATES":
        return get_templates()
    raise AttributeError(name)


def match_template(request: str) -> Template | None:
    low = _low(request)
    for tmpl in get_templates():
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
