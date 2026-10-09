"""Deterministic TinyLM-free templates for 'write a python function…' asks.

Cycle 207: each template carries tiny examples so CodeAgent can self-check
the generated body (HumanEval-style pass/fail) without calling the LLM.

Restored loader (post-placeholder): discovers code_synth_p*.py packs via
importlib rather than a hard-coded 200-name list so the file stays small.
"""
from __future__ import annotations

import copy
import importlib
import pkgutil
import re
from dataclasses import dataclass
from pathlib import Path
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


def _discover_pack_names() -> list[str]:
    """Prefer package-local modules named code_synth_p*."""
    names: list[str] = []
    try:
        import code_synth as self_mod
        root = Path(self_mod.__file__).resolve().parent
    except Exception:
        root = Path(__file__).resolve().parent
    for p in sorted(root.glob("code_synth_p*.py")):
        names.append(p.stem)
    # Fallback: walk sys.modules path
    if not names:
        try:
            import code_synth as self_mod
            prefix = "code_synth_p"
            for m in pkgutil.iter_modules(getattr(self_mod, "__path__", [])):
                if m.name.startswith(prefix):
                    names.append(m.name)
        except Exception:
            pass
    return names


def _load_pack_templates() -> list[Template]:
    out: list[Template] = []
    for name in _discover_pack_names():
        try:
            mod = importlib.import_module(name)
        except Exception:
            continue
        fn = getattr(mod, "templates", None)
        if not callable(fn):
            continue
        try:
            items = fn()
        except Exception:
            continue
        for t in items or []:
            if isinstance(t, Template):
                out.append(t)
            elif hasattr(t, "name") and hasattr(t, "source") and hasattr(t, "match"):
                out.append(
                    Template(
                        str(t.name),
                        str(t.source),
                        t.match,
                        getattr(t, "examples", ()) or (),
                    )
                )
    return out


_CACHE: list[Template] | None = None


def get_templates() -> list[Template]:
    global _CACHE
    if _CACHE is None:
        _CACHE = _load_pack_templates()
    return _CACHE


def match_template(request: str) -> Template | None:
    low = _low(request)
    best = None
    for t in get_templates():
        try:
            if t.match(low):
                best = t
                # keep first match (packs ordered by discovery)
                break
        except Exception:
            continue
    return best


def synthesize_python(request: str) -> str:
    t = match_template(request)
    if t is not None:
        return t.source
    low = _low(request)
    if re.search(r"add(s|ing)?\b.{0,24}\b" + _TWO + r"\b.{0,24}\b(number|int|value)", low) or "adds two" in low:
        return (
            "def add(a, b):\n"
            '    """Return the sum of a and b."""\n'
            "    return a + b\n"
        )
    slug = re.sub(r"[^a-z0-9]+", "_", low)[:40].strip("_") or "solve"
    return (
        f"def {slug}(*args, **kwargs):\n"
        f'    """Draft from: {(request or "").strip()[:120]}"""\n'
        "    raise NotImplementedError('Paste a fenced snippet to run it, or specify the function body.')\n"
    )


def verify_source(source: str, examples: Sequence[tuple]) -> dict:
    ns: dict[str, Any] = {}
    try:
        exec(source, ns, ns)
    except Exception as e:
        return {"ok": False, "checked": 0, "error": str(e)}
    fn = None
    for v in ns.values():
        if callable(v) and getattr(v, "__name__", "") != "Template":
            fn = v
            break
    if fn is None:
        return {"ok": False, "checked": 0, "error": "no function"}
    ok = 0
    for item in examples or ():
        try:
            args, exp = item
            if not isinstance(args, tuple):
                args = (args,)
            if fn(*args) == exp:
                ok += 1
        except Exception:
            pass
    return {"ok": ok == len(examples) and len(examples) > 0, "checked": ok}


def synthesize_and_verify(request: str) -> dict:
    t = match_template(request)
    if t is None:
        src = synthesize_python(request)
        return {
            "source": src,
            "verified": False,
            "checked": 0,
            "fallback": True,
            "name": None,
        }
    check = verify_source(t.source, t.examples)
    return {
        "source": t.source,
        "verified": bool(check.get("ok")),
        "checked": int(check.get("checked") or 0),
        "fallback": False,
        "name": t.name,
        "error": check.get("error"),
    }
