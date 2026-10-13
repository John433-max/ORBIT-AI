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
    """Phrase gaps: relax loaded matchers without changing pack bodies."""
    name = getattr(tmpl, "name", None)
    # Identity for most; specific wideners live in packs / prior cycles.
    return tmpl


def _templates() -> list[Template]:
    """Load split packs (Cycle 244). Discover code_synth_p*.py dynamically; missing packs skipped."""
    import pathlib
    out: list[Template] = []
    seen: set[str] = set()
    packs: list[tuple[int, str]] = []
    root = pathlib.Path(__file__).resolve().parent
    for p in root.glob("code_synth_p*.py"):
        m = re.match(r"code_synth_p(\d+)$", p.stem)
        if m:
            packs.append((int(m.group(1)), p.stem))
    packs.sort(key=lambda t: t[0], reverse=True)
    for _, name in packs:
        try:
            mod = __import__(name, fromlist=["templates"])
            fn = getattr(mod, "templates", None)
            if not callable(fn):
                continue
            pack = list(fn())
        except Exception:
            continue
        for tmpl in pack:
            n = getattr(tmpl, "name", None)
            if not n or n in seen:
                continue
            seen.add(n)
            out.append(_widen_loaded(tmpl))
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


def _name_tokens(name: str) -> list[str]:
    return [t for t in re.split(r"[_\s]+", (name or "").lower()) if t and len(t) > 1]


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
    key = _low(request)
    cache = globals().setdefault("_MATCH_CACHE", {})
    if key in cache:
        return cache[key]
    hit = _match_template_uncached(request)
    if len(cache) >= 256:
        cache.clear()
    cache[key] = hit
    return hit


def _match_template_uncached(request: str) -> Template | None:
    hits = iter_matching(request)
    if not hits:
        return None
    low = _low(request)
    best = hits[0]
    best_tok = set(_name_tokens(best.name))
    best_score = score_template(request, best)
    for tmpl in hits[1:]:
        tok = set(_name_tokens(tmpl.name))
        extra = tok - best_tok
        score = score_template(request, tmpl)
        if extra and best_tok <= tok and all(t in low for t in extra):
            best = tmpl
            best_tok = tok
            best_score = score
            continue
        if score > best_score and score >= 2:
            best = tmpl
            best_tok = tok
            best_score = score
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
    """Exec source and run optional (args, expected) examples."""
    ns: dict[str, Any] = {}
    try:
        exec(source, ns, ns)
    except Exception as e:
        return {"ok": False, "checked": 0, "error": str(e), "name": None}
    # find first def
    m = re.search(r"^def\s+(\w+)", source, re.M)
    name = m.group(1) if m else None
    fn = ns.get(name) if name else None
    if not callable(fn):
        return {"ok": False, "checked": 0, "error": "no callable", "name": name}
    checked = 0
    if examples:
        for args, expected in examples:
            try:
                if not isinstance(args, tuple):
                    args = (args,)
                got = fn(*args)
                if got != expected:
                    return {
                        "ok": False,
                        "checked": checked,
                        "error": f"example failed: {got!r} != {expected!r}",
                        "name": name,
                    }
                checked += 1
            except Exception as e:
                return {"ok": False, "checked": checked, "error": str(e), "name": name}
    return {"ok": True, "checked": checked, "error": None, "name": name}


def synthesize_and_verify(request: str) -> dict[str, Any]:
    tmpl = match_template(request)
    if tmpl is None:
        src = fallback_source(request)
        return {
            "source": src,
            "verified": False,
            "fallback": True,
            "checked": 0,
            "name": None,
            "error": "no template",
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
