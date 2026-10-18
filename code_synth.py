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

_TWO = r"(two|2|a pair of)"

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

TEMPLATES = get_templates()  # compat alias for tests

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
    "evaluate_division": "calcEquation",
    "maximum_performance_of_a_team": "max_team_performance",  # selects p146 template whose source is def maxPerformance (LC 1383 / code_1110)
    "roman_to_integer": "roman_to_int",
    "trapping_rain_water": "trap_rain_water",
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

_MATCH_CACHE: OrderedDict[str, Template | None] = OrderedDict()
_MATCH_CACHE_MAX = 2048

def match_template(request: str) -> Template | None:
    key = _low(request)
    if key in _MATCH_CACHE:
        _MATCH_CACHE.move_to_end(key)
        return _MATCH_CACHE[key]
    hits = iter_matching(request)
    if not hits:
        hit = None
    else:
        low = key
        best = hits[0]
        best_tok = set(_name_tokens(best.name))
        best_score = score_template(request, best)
        for tmpl in hits[1:]:
            tok = set(_name_tokens(tmpl.name))
            extra = tok - best_tok
            score = score_template(request, tmpl)
            if extra and best_tok <= tok and all(t in low for t in extra):
                best, best_tok, best_score = tmpl, tok, score
                continue
            if score > best_score and score >= 2:
                best, best_tok, best_score = tmpl, tok, score
        if ("function" in low or "leetcode" in low or "write a" in low) and best is not None:
            short_name = _SHORT_FOR_WRITE.get(best.name)
            if short_name:
                for tmpl in hits:
                    if tmpl.name == short_name:
                        best = tmpl
                        break
        hit = best
    _MATCH_CACHE[key] = hit
    _MATCH_CACHE.move_to_end(key)
    while len(_MATCH_CACHE) > _MATCH_CACHE_MAX:
        _MATCH_CACHE.popitem(last=False)
    return hit

def fallback_source(request: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", _low(request))[:40].strip("_") or "solve"
    return (
        f"def {slug}(*args, **kwargs):\n"
        f'    """Draft from: {(request or "").strip()[:120]}"""\n'
        "    raise NotImplementedError('Paste a fenced snippet to run it, or specify the function body.')\n"
    )

def _rewrite_def_name(source: str, short: str) -> str:
    m = re.match(r"(def\s+)([A-Za-z_]\w*)", source or "")
    if not m or not short:
        return source
    return source[: m.start(2)] + short + source[m.end(2) :]

def synthesize_python(request: str) -> str | None:
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
        exec(source or "", ns, ns)
    except Exception as e:
        return {"ok": False, "error": str(e), "name": None, "checked": 0}
    fn = None
    for v in ns.values():
        if callable(v) and getattr(v, "__name__", "").startswith(("_",)) is False:
            if getattr(v, "__code__", None) is not None:
                fn = v
                break
    if fn is None:
        for k, v in ns.items():
            if callable(v) and not k.startswith("_"):
                fn = v
                break
    if fn is None:
        return {"ok": False, "error": "no callable", "name": None, "checked": 0}
    checked = 0
    if examples:
        for args, expected in examples:
            try:
                if isinstance(args, (tuple, list)):
                    got = fn(*args)
                else:
                    got = fn(args)
            except Exception as e:
                return {"ok": False, "error": str(e), "name": getattr(fn, "__name__", None), "checked": checked}
            if got != expected:
                return {
                    "ok": False,
                    "error": f"expected {expected!r} got {got!r}",
                    "name": getattr(fn, "__name__", None),
                    "checked": checked,
                }
            checked += 1
    return {"ok": True, "error": None, "name": getattr(fn, "__name__", None), "checked": checked}

def synthesize_and_verify(request: str) -> dict[str, Any]:
    tmpl = match_template(request)
    if tmpl is None:
        return {
            "ok": False,
            "source": fallback_source(request),
            "error": "no template",
            "name": None,
            "verified": False,
            "fallback": True,
            "checked": 0,
        }
    src = synthesize_python(request)
    check = verify_source(src or "", tmpl.examples)
    return {
        "ok": bool(check.get("ok")),
        "source": src,
        "name": check.get("name") or getattr(tmpl, "name", None),
        "error": check.get("error"),
        "verified": bool(check.get("ok")),
        "fallback": False,
        "checked": int(check.get("checked") or 0),
    }

def __getattr__(name: str):
    if name == "TEMPLATES":
        return get_templates()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
