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


def _templates() -> list[Template]:
    """Load split packs (Cycle 244). Missing packs are skipped so CI still collects."""
    import importlib
    out: list[Template] = []
    seen: set[str] = set()
    for name in (
        "code_synth_p1",
        "code_synth_p1b",
        "code_synth_p2",
        "code_synth_p3",
        "code_synth_p4",
        "code_synth_p5",
        "code_synth_p6",
        "code_synth_p7",
        "code_synth_p8",
        "code_synth_p9",
        "code_synth_p10",
        "code_synth_p11",
        "code_synth_p12",
        "code_synth_p13",
        "code_synth_p14",
        "code_synth_p15",
        "code_synth_p16",
        "code_synth_p17",
        "code_synth_p18",
        "code_synth_p19",
        "code_synth_p20",
        "code_synth_p21",
        "code_synth_p22",
        "code_synth_p23",
        "code_synth_p24",
        "code_synth_p25",
        "code_synth_p26",
        "code_synth_p27",
        "code_synth_p28",
        "code_synth_p29",
        "code_synth_p30",
        "code_synth_p31",
        "code_synth_p32",
        "code_synth_p33",
    ):
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
            # One malformed pack must not break CI collection / chat routing.
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
    TEMPLATES = loaded
    return loaded


def __getattr__(name: str):
    if name == "TEMPLATES":
        return get_templates()
    raise AttributeError(name)


_STOP = frozenset(
    {
        "a",
        "an",
        "the",
        "of",
        "to",
        "in",
        "on",
        "for",
        "and",
        "or",
        "is",
        "a",
    }
)

_ROMAN = {"ii": "2", "iii": "3", "iv": "4"}


def _name_tokens(name: str) -> list[str]:
    parts = [p for p in (name or "").lower().replace("-", "_").split("_") if p]
    out: list[str] = []
    for p in parts:
        if p in _STOP:
            continue
        out.append(p)
        if p in _ROMAN:
            out.append(_ROMAN[p])
    return out


def score_template(request: str, tmpl: Template) -> float:
    """How many distinctive name tokens appear in the request."""
    low = _low(request)
    tokens = _name_tokens(getattr(tmpl, "name", "") or "")
    if not tokens:
        return 0.0
    return float(sum(1 for t in tokens if t in low))


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
    """First match, then upgrade to a token-superset sibling.

    Cycle 283: pack order stays the default (smoke depends on it). If a later
    hit's name tokens strictly contain the winner's tokens *and* the extra
    tokens appear in the request, prefer the more specific sibling.
    """
    hits = iter_matching(request)
    if not hits:
        return None
    low = _low(request)
    best = hits[0]
    best_tok = set(_name_tokens(best.name))
    for tmpl in hits[1:]:
        tok = set(_name_tokens(tmpl.name))
        extra = tok - best_tok
        if extra and best_tok <= tok and all(t in low for t in extra):
            best = tmpl
            best_tok = tok
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
        "name": check.get("name") or tmpl.name,
        "error": check.get("error"),
    }
