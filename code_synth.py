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


_STOP = frozenset({"a", "an", "the", "of", "to", "in", "on", "for", "and", "or", "is"})


def _name_tokens(name: str) -> list[str]:
    parts = [p for p in (name or "").lower().replace("-", "_").split("_") if p and p not in _STOP]
    return parts


def score_template(request: str, tmpl: Template) -> float:
    low = _low(request)
    tokens = _name_tokens(getattr(tmpl, "name", "") or "")
    if not tokens:
        return 0.0
    return float(sum(1 for t in tokens if t in low))


def _templates() -> list[Template]:
    """Load split packs. Discover code_synth_p*.py dynamically; missing packs skipped."""
    import importlib
    import pathlib
    out: list[Template] = []
    seen: set[str] = set()
    packs: list[tuple[int, str]] = []
    root = pathlib.Path(__file__).resolve().parent
    for p in root.glob("code_synth_p*.py"):
        m = re.match(r"code_synth_p(\d+)\.py$", p.name)
        if m:
            packs.append((int(m.group(1)), p.stem))
    packs.sort(key=lambda t: t[0], reverse=True)
    for _, name in packs:
        try:
            mod = importlib.import_module(name)
        except Exception:
            continue
        fn = getattr(mod, "templates", None)
        if not callable(fn):
            continue
        try:
            pack = list(fn())
        except Exception:
            continue
        for tmpl in pack:
            key = getattr(tmpl, "name", None)
            if key in seen:
                continue
            if key:
                seen.add(key)
            out.append(tmpl)
    return out


def get_templates() -> list[Template]:
    global TEMPLATES
    cached = globals().get("_TEMPLATES_CACHE")
    if cached is not None:
        return cached
    loaded = _templates()
    globals()["_TEMPLATES_CACHE"] = loaded
    globals().get("_MATCH_CACHE", {}).clear()
    TEMPLATES = loaded
    return loaded


def __getattr__(name: str):
    if name == "TEMPLATES":
        return get_templates()
    raise AttributeError(name)


def iter_matching(request: str) -> list[Template]:
    low = _low(request)
    hits: list[Template] = []
    for tmpl in get_templates():
        try:
            if tmpl.match(low):
                hits.append(tmpl)
        except Exception:
            continue
    return hits


def match_template(request: str) -> Template | None:
    """Prefer higher name-token overlap; break ties by longer name."""
    key = _low(request)
    cache = globals().setdefault("_MATCH_CACHE", {})
    if key in cache:
        return cache[key]
    hits = iter_matching(request)
    if not hits:
        cache[key] = None
        return None
    best = hits[0]
    best_score = score_template(request, best)
    for tmpl in hits[1:]:
        score = score_template(request, tmpl)
        if score > best_score or (
            score == best_score and len(tmpl.name) > len(best.name)
        ):
            best = tmpl
            best_score = score
    if len(cache) >= 256:
        cache.clear()
    cache[key] = best
    return best


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
    ns: dict[str, Any] = {}
    try:
        exec(source, ns, ns)  # noqa: S102
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
        "name": check.get("name") or tmpl.name,
        "error": check.get("error"),
    }


TEMPLATES: list[Template] = []  # populated lazily via get_templates / __getattr__
