"""Deterministic TinyLM-free templates for 'write a python function…' asks.

Cycle 207: each template carries tiny examples so CodeAgent can self-check
the generated body (HumanEval-style pass/fail) without calling the LLM.
"""
from __future__ import annotations

import copy
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


def _widen_loaded(tmpl: Template) -> Template:
    """Phrase gaps found by CI 37575101631 (p202–p205 asks).

    Pack files stay the source of the body. Only the loaded matcher is
    relaxed so 'swaps the case', 'splits a list into chunks', and
    'rotates a string left' hit the existing templates.
    """
    name = getattr(tmpl, "name", None)
    if name == "swap_case":
        return Template(
            name,
            tmpl.source,
            lambda low: bool(re.search(r"swaps?(?: the)?[- ]case", low))
            and "node" not in low
            and "value" not in low,
            tmpl.examples,
        )
    if name == "chunk_list":
        return Template(
            name,
            tmpl.source,
            lambda low: bool(
                re.search(
                    r"\bchunk(?:s|ed|ing)?\b.{0,24}\b(list|array|items)\b|"
                    r"\bsplits?\b.{0,32}\b(list|array)\b.{0,32}\b(chunks?|batches|groups)\b",
                    low,
                )
            ),
            tmpl.examples,
        )
    if name == "rotate_string":
        return Template(
            name,
            tmpl.source,
            lambda low: bool(
                re.search(
                    r"\brota(?:te|tes|ting)(?: a)? string\b|\bstring rotation\b",
                    low,
                )
            )
            and "matrix" not in low
            and "image" not in low
            and "list" not in low,
            tmpl.examples,
        )
    if name == "find_max_average":
        return Template(
            name,
            tmpl.source,
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]max[_ ]average\b|"
                    r"\bmaximum average subarray\b|"
                    r"\bmax average of (a )?subarray\b",
                    low,
                )
            ),
            tmpl.examples,
        )
    return tmpl


def _load_pack(mod_name: str) -> list[Template]:
    try:
        mod = __import__(mod_name, fromlist=["TEMPLATES"])
        pack = getattr(mod, "TEMPLATES", None) or getattr(mod, "templates", None) or []
        out = []
        for t in pack:
            if isinstance(t, Template):
                out.append(_widen_loaded(t))
            elif isinstance(t, (list, tuple)) and len(t) >= 3:
                # legacy (name, source, match_fn, examples?)
                name, source, match = t[0], t[1], t[2]
                examples = t[3] if len(t) > 3 else ()
                out.append(_widen_loaded(Template(name, source, match, examples)))
        return out
    except Exception:
        return []


def _discover_packs() -> list[Template]:
    """Load code_synth_p*.py packs (lazy, once)."""
    import importlib
    import pkgutil
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent
    loaded: list[Template] = []
    seen: set[str] = set()

    # Prefer numbered packs in order
    for path in sorted(root.glob("code_synth_p*.py")):
        mod_name = path.stem
        if mod_name in seen:
            continue
        seen.add(mod_name)
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        pack = _load_pack(mod_name)
        loaded.extend(pack)

    # Built-in minimal templates if packs missing
    if not loaded:
        loaded = list(_builtin_templates())
    return loaded


def _builtin_templates() -> list[Template]:
    """Minimal always-available templates when packs are absent."""

    def add_match(low: str) -> bool:
        return bool(
            re.search(
                r"add(s|ing)?\b.{0,24}\b" + _TWO + r"\b.{0,24}\b(number|int|value)|"
                r"\badds? two\b",
                low,
            )
        )

    return [
        Template(
            "add",
            'def add(a, b):\n    """Return the sum of a and b."""\n    return a + b\n',
            add_match,
            (((1, 2), 3), ((-4, 10), 6)),
        ),
    ]


# Lazy cache
TEMPLATES: list[Template] | None = None
_TEMPLATES_CACHE: list[Template] | None = None


def templates() -> list[Template]:
    global TEMPLATES, _TEMPLATES_CACHE
    if _TEMPLATES_CACHE is not None:
        return _TEMPLATES_CACHE
    loaded = _discover_packs()
    # Dedup by name keeping first
    by_name: dict[str, Template] = {}
    for t in loaded:
        if t.name not in by_name:
            by_name[t.name] = t
    _TEMPLATES_CACHE = list(by_name.values())
    TEMPLATES = _TEMPLATES_CACHE
    return _TEMPLATES_CACHE


def __getattr__(name: str):
    if name == "TEMPLATES":
        return templates()
    raise AttributeError(name)


def match_template(request: str) -> Template | None:
    low = _low(request)
    for tmpl in templates():
        try:
            if tmpl.match(low):
                return tmpl
        except Exception:
            continue
    return None


def fallback_source(request: str) -> str:
    low = _low(request)
    slug = re.sub(r"[^a-z0-9]+", "_", low)[:40].strip("_") or "solve"
    return (
        f"def {slug}(*args, **kwargs):\n"
        f"    \"\"\"Draft from: {(request or '').strip()[:120]}\"\"\"\n"
        "    raise NotImplementedError('Paste a fenced snippet to run it, or specify the function body.')\n"
    )


def verify_source(source: str, examples: Sequence[tuple] | None = None) -> dict[str, Any]:
    """Exec source and check examples; return {ok, checked, name, error?}."""
    ns: dict[str, Any] = {}
    try:
        exec(source, ns, ns)
    except Exception as exc:
        return {"ok": False, "error": str(exc), "checked": 0}
    fn = None
    for val in ns.values():
        if callable(val) and getattr(val, "__code__", None) is not None:
            # prefer top-level functions defined in the source
            if getattr(val, "__module__", None) is None or True:
                fn = val
                break
    if fn is None:
        return {"ok": False, "error": "no function defined", "checked": 0}
    if not examples:
        return {"ok": True, "checked": 0, "name": getattr(fn, "__name__", "?")}
    checked = 0
    try:
        for args, expected in examples:
            got = fn(*copy.deepcopy(args))
            if got != expected:
                return {
                    "ok": False,
                    "error": f"{getattr(fn, '__name__', '?')}{args} -> {got!r} != {expected!r}",
                    "checked": checked,
                    "name": getattr(fn, "__name__", "?"),
                }
            checked += 1
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "checked": checked,
            "name": getattr(fn, "__name__", "?"),
        }
    return {"ok": True, "checked": checked, "name": getattr(fn, "__name__", "?")}


def synthesize_and_verify(request: str) -> dict[str, Any]:
    """Match a template, emit source, and self-check examples when present."""
    tmpl = match_template(request)
    if tmpl is None:
        return {
            "source": fallback_source(request),
            "verified": False,
            "fallback": True,
            "checked": 0,
            "name": None,
        }
    check = verify_source(tmpl.source, tmpl.examples)
    return {
        "source": tmpl.source,
        "verified": bool(check.get("ok")),
        "fallback": False,
        "checked": int(check.get("checked") or 0),
        "name": tmpl.name,
    }


def synthesize_python(request: str) -> str:
    """Return source only (legacy API used by agents / tests)."""
    bundle = synthesize_and_verify(request)
    return str(bundle.get("source") or "")
