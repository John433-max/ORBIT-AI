"""Deterministic TinyLM-free templates for write-a-function asks (emergency restore).

Full local module is larger; this restore keeps pack discovery + core API so
agents/tests can import match_template, synthesize_python, synthesize_and_verify,
verify_source, get_templates, TEMPLATES.
"""
from __future__ import annotations

import importlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

@dataclass(frozen=True)
class Template:
    name: str
    source: str
    match: Callable[[str], bool]
    examples: Sequence[tuple]

_TEMPLATES: list[Template] | None = None

def _low(request: str) -> str:
    return (request or "").lower()

def _load_packs() -> list[Template]:
    out: list[Template] = []
    root = Path(__file__).resolve().parent
    for p in sorted(root.glob("code_synth_p*.py"), key=lambda x: x.name):
        m = re.match(r"code_synth_p(\d+)\.py$", p.name)
        if not m:
            continue
        name = f"code_synth_p{m.group(1)}"
        try:
            mod = importlib.import_module(name)
        except Exception:
            continue
        raw = getattr(mod, "TEMPLATES", None) or getattr(mod, "templates", None) or []
        for t in raw:
            if isinstance(t, Template):
                out.append(t)
                continue
            if not isinstance(t, dict):
                continue
            n = t.get("name") or t.get("id") or "tmpl"
            src = t.get("source") or t.get("code") or t.get("body") or ""
            examples = t.get("examples") or ()
            matcher = t.get("match")
            if callable(matcher):
                match_fn = matcher
            else:
                keys = t.get("matchers") or t.get("triggers") or t.get("match") or []
                if isinstance(keys, str):
                    keys = [keys]
                keys = [str(k).lower() for k in keys if k]
                def match_fn(low, keys=keys):
                    return any(k in low for k in keys)
            out.append(Template(str(n), str(src), match_fn, tuple(examples)))
    return out

def get_templates() -> list[Template]:
    global _TEMPLATES
    if _TEMPLATES is None:
        _TEMPLATES = _load_packs()
    return _TEMPLATES

def match_template(request: str) -> Template | None:
    low = _low(request)
    for t in get_templates():
        try:
            if t.match(low):
                return t
        except Exception:
            continue
    return None

def iter_matching(request: str) -> list[Template]:
    low = _low(request)
    out = []
    for t in get_templates():
        try:
            if t.match(low):
                out.append(t)
        except Exception:
            continue
    return out

def verify_source(source: str, examples: Sequence[tuple] | None = None) -> dict[str, Any]:
    if not source or not isinstance(source, str):
        return {"ok": False, "checked": 0, "error": "empty"}
    ns: dict[str, Any] = {}
    try:
        exec(source, ns, ns)
    except Exception as e:
        return {"ok": False, "checked": 0, "error": str(e)}
    fn = None
    for k, v in ns.items():
        if callable(v) and not k.startswith("_"):
            fn = v
            break
    if fn is None:
        return {"ok": False, "checked": 0, "error": "no function"}
    checked = 0
    if examples:
        for ex in examples:
            try:
                if len(ex) == 2:
                    args, expected = ex
                    if not isinstance(args, tuple):
                        args = (args,)
                    got = fn(*args)
                    if got != expected:
                        return {"ok": False, "checked": checked, "error": f"{got!r} != {expected!r}", "name": getattr(fn, "__name__", None)}
                    checked += 1
            except Exception as e:
                return {"ok": False, "checked": checked, "error": str(e), "name": getattr(fn, "__name__", None)}
    return {"ok": True, "checked": checked, "name": getattr(fn, "__name__", None)}

def synthesize_python(request: str) -> str:
    t = match_template(request)
    if t is None:
        return f"def solution(*args, **kwargs):\n    raise NotImplementedError({request!r})\n"
    return t.source

def synthesize_and_verify(request: str) -> dict[str, Any]:
    t = match_template(request)
    if t is None:
        return {"source": synthesize_python(request), "verified": False, "fallback": True, "checked": 0, "name": None, "error": "no match"}
    check = verify_source(t.source, t.examples)
    return {
        "source": t.source,
        "verified": bool(check.get("ok")),
        "fallback": False,
        "checked": int(check.get("checked") or 0),
        "name": check.get("name") or t.name,
        "error": check.get("error"),
    }

def __getattr__(name: str):
    if name == "TEMPLATES":
        return get_templates()
    raise AttributeError(name)

synthesize = synthesize_python
