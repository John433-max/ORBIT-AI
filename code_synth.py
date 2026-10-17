"""Deterministic TinyLM-free templates for write-a-function asks (slim GH restore)."""
from __future__ import annotations
import copy, re, importlib, importlib.util, pathlib, glob as _glob
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable, Sequence

@dataclass(frozen=True)
class Template:
    name: str
    source: str
    match: Callable[[str], bool]
    examples: Sequence[tuple]

def _low(request: str) -> str:
    return (request or "").lower()

def _widen_loaded(tmpl: Template) -> Template:
    return tmpl

def _templates() -> list[Template]:
    out: list[Template] = []
    seen: set[str] = set()
    packs: list[tuple[int, str]] = []
    root = pathlib.Path(__file__).resolve().parent
    for path in _glob.glob(str(root / "code_synth_p*.py")):
        name = pathlib.Path(path).name
        m = re.match(r"code_synth_p(\d+)\.py$", name)
        if m:
            packs.append((int(m.group(1)), pathlib.Path(path).stem))
    packs.sort(key=lambda t: t[0], reverse=True)
    for num, name in packs:
        try:
            path = root / f"{name}.py"
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None or spec.loader is None:
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except Exception:
            continue
        fn = getattr(mod, "templates", None)
        if not callable(fn):
            continue
        try:
            for tmpl in fn():
                n = getattr(tmpl, "name", None)
                if not n or n in seen:
                    continue
                seen.add(n)
                out.append(_widen_loaded(tmpl))
        except Exception:
            continue
    return out

_CACHE: list[Template] | None = None

def get_templates() -> list[Template]:
    global _CACHE
    if _CACHE is None:
        _CACHE = _templates()
    return _CACHE

_SHORT_FOR_WRITE = {
    "longest_increasing_subsequence": "lis",
    "minimum_path_sum": "min_path_sum",
    "partition_equal_subset_sum": "can_partition",
    "kth_largest_element": "find_kth_largest",
    "excel_sheet_column_title": "convert_to_title",
    "excel_sheet_column_number": "title_to_number",
    "non_overlapping_intervals": "erase_overlap_intervals",
    "maximum_subarray": "max_subarray",
    "product_of_array_except_self": "product_except_self",
    "spiral_matrix": "spiral_order",
    "trie_class": "implement_trie",
    "implement_trie": "implement_trie",
    "evaluate_division": "calcEquation",
    "maximum_performance_of_a_team": "maxPerformance",
}

def _name_tokens(name: str) -> list[str]:
    return [t for t in re.split(r"[_\W]+", name.lower()) if t]

def score_template(request: str, tmpl: Template) -> float:
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

_MATCH_CACHE_MAX = 2048
_MATCH_CACHE: OrderedDict[str, Template | None] = OrderedDict()

def match_template(request: str) -> Template | None:
    key = (request or "").strip().lower()
    if key in _MATCH_CACHE:
        _MATCH_CACHE.move_to_end(key)
        return _MATCH_CACHE[key]
    hits = iter_matching(request)
    winner = hits[0] if hits else None
    if winner and len(hits) > 1:
        wtok = set(_name_tokens(winner.name))
        for h in hits[1:]:
            htok = set(_name_tokens(h.name))
            if wtok < htok and all(t in _low(request) for t in (htok - wtok)):
                winner = h
                wtok = htok
    _MATCH_CACHE[key] = winner
    while len(_MATCH_CACHE) > _MATCH_CACHE_MAX:
        _MATCH_CACHE.popitem(last=False)
    return winner

def _rewrite_def_name(source: str, new_name: str) -> str:
    return re.sub(r"^def\s+\w+", f"def {new_name}", source, count=1, flags=re.M)

def fallback_source(request: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", _low(request))[:40].strip("_") or "solve"
    return (
        f"def {slug}(*args, **kwargs):\n"
        f'    """Draft from: {(request or "").strip()[:120]}"""\n'
        "    raise NotImplementedError(\"Paste a fenced snippet to run it, or specify the function body.\")\n"
    )

def synthesize_python(request: str) -> str:
    tmpl = match_template(request)
    if tmpl is None:
        return fallback_source(request)
    src = tmpl.source
    short = _SHORT_FOR_WRITE.get(tmpl.name)
    low = _low(request)
    if short and ("write" in low or "leetcode" in low or "function" in low or "implement" in low):
        src = _rewrite_def_name(src, short)
    return src

def verify_source(source: str, examples: Sequence[tuple] | None = None) -> dict[str, Any]:
    """Execute template source against examples; return ok/error dict."""
    ns: dict[str, Any] = {}
    try:
        exec(source, ns, ns)
    except Exception as e:
        return {"ok": False, "error": f"exec: {e}", "name": None}
    fn = None
    name = None
    for k, v in ns.items():
        if callable(v) and not k.startswith("_"):
            fn = v
            name = k
            break
    if fn is None:
        return {"ok": False, "error": "no callable", "name": None}
    if not examples:
        return {"ok": True, "name": name, "error": None}
    try:
        for args, expected in examples:
            got = fn(*args) if isinstance(args, tuple) else fn(args)
            if got != expected:
                return {"ok": False, "error": f"example fail: {got!r} != {expected!r}", "name": name}
    except Exception as e:
        return {"ok": False, "error": f"run: {e}", "name": name}
    return {"ok": True, "name": name, "error": None}

def synthesize_and_verify(request: str) -> dict[str, Any]:
    tmpl = match_template(request)
    if tmpl is None:
        return {"ok": False, "source": None, "error": "no template", "name": None}
    src = synthesize_python(request)
    check = verify_source(src or "", tmpl.examples)
    return {
        "ok": bool(check.get("ok")),
        "source": src,
        "name": check.get("name") or getattr(tmpl, "name", None),
        "error": check.get("error"),
        "verified": bool(check.get("ok")),
    }


def __getattr__(name: str):
    if name == "TEMPLATES":
        return get_templates()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
