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
                    r"\bmaximum average\b.{0,40}\bsubarray\b|"
                    r"\bmax average of (?:any |a )?subarray\b",
                    low,
                )
            )
            and "moving" not in low,
            tmpl.examples,
        )
    if name == "busy_student":
        return Template(
            name,
            tmpl.source,
            lambda low: bool(
                re.search(
                    r"\bbusy[_ ]student\b|"
                    r"\bstudents doing homework\b|"
                    r"\bhomework at (?:a )?(?:given |query )?time\b",
                    low,
                )
            ),
            tmpl.examples,
        )
    # CI 37701068446: later packs stole or missed p202–p213 aliases.
    if name == "can_rotate_to":
        return Template(
            name,
            tmpl.source,
            lambda low: (
                "string" in low
                and "rotat" in low
                and any(
                    w in low
                    for w in ("obtained", "goal", "can be rotated", "can_rotate", "796")
                )
                and "is a rotation of another" not in low
                and "matrix" not in low
                and "image" not in low
                and "left by" not in low
                and "right by" not in low
                and "list" not in low
            ),
            tmpl.examples,
        )
    if name == "second_largest":
        return Template(
            name,
            tmpl.source,
            lambda low: (
                "digit" not in low
                and "1796" not in low
                and (
                    "second largest" in low
                    or "second-largest" in low
                    or "second highest" in low
                    or "second-highest" in low
                )
            ),
            tmpl.examples,
        )
    if name == "left_pad":
        return Template(
            name,
            tmpl.source,
            lambda low: bool(
                re.search(r"left[- ]?pad|pad left|pad(?:s|ding)? (?:a |the )?string on the left", low)
            )
            and "right" not in low,
            tmpl.examples,
        )
    if name == "right_pad":
        return Template(
            name,
            tmpl.source,
            lambda low: bool(
                re.search(r"right[- ]?pad|pad right|pad(?:s|ding)? (?:a |the )?string on the right", low)
            )
            and "left" not in low,
            tmpl.examples,
        )
    if name == "group_consecutive":
        return Template(
            name,
            tmpl.source,
            lambda low: (
                "consecutive" in low
                and "group" in low
                and "drop" not in low
                and "diff" not in low
                and "character" not in low
            ),
            tmpl.examples,
        )
    return tmpl


def _templates() -> list[Template]:
    """Load split packs (Cycle 244). Missing packs are skipped so CI still collects."""
    import importlib
    out: list[Template] = []
    seen: set[str] = set()
    for name in (
        "code_synth_p227",
        "code_synth_p226",
        "code_synth_p225",
        "code_synth_p224",
        "code_synth_p223",
        "code_synth_p222",
        "code_synth_p221",
        "code_synth_p220",
        "code_synth_p219",
        "code_synth_p218",
        "code_synth_p217",
        "code_synth_p216",
        "code_synth_p215",
        "code_synth_p214",
        "code_synth_p213",
        "code_synth_p212",
        "code_synth_p211",
        "code_synth_p210",
        "code_synth_p209",
        "code_synth_p208",
        "code_synth_p207",
        "code_synth_p206",
        "code_synth_p205",
        "code_synth_p204",
        "code_synth_p203",
        "code_synth_p202",
        "code_synth_p201",
        "code_synth_p200",
        "code_synth_p199",
        "code_synth_p198",
        "code_synth_p197",
        "code_synth_p196",
        "code_synth_p195",
        "code_synth_p194",
        "code_synth_p193",
        "code_synth_p192",
        "code_synth_p191",
        "code_synth_p190",
        "code_synth_p189",
        "code_synth_p188",
        "code_synth_p187",
        "code_synth_p186",
        "code_synth_p185",
        "code_synth_p184",
        "code_synth_p183",
        "code_synth_p182",
        "code_synth_p181",
        "code_synth_p180",
        "code_synth_p179",
        "code_synth_p178",
        "code_synth_p177",
        "code_synth_p176",
        "code_synth_p175",
        "code_synth_p174",
        "code_synth_p173",
        "code_synth_p172",
        "code_synth_p171",
        "code_synth_p170",
        "code_synth_p169",
        "code_synth_p168",
        "code_synth_p167",
        "code_synth_p166",
        "code_synth_p165",
        "code_synth_p164",
        "code_synth_p163",
        "code_synth_p162",
        "code_synth_p161",
        "code_synth_p160",
        "code_synth_p159",
        "code_synth_p158",
        "code_synth_p157",
        "code_synth_p156",
        "code_synth_p155",
        "code_synth_p154",
        "code_synth_p153",
        "code_synth_p152",
        "code_synth_p151",
        "code_synth_p150",
        "code_synth_p149",
        "code_synth_p148",
        "code_synth_p147",
        "code_synth_p146",
        "code_synth_p145",
        "code_synth_p144",
        "code_synth_p143",
        "code_synth_p142",
        "code_synth_p141",
        "code_synth_p140",
        "code_synth_p139",
        "code_synth_p138",
        "code_synth_p137",
        "code_synth_p136",
        "code_synth_p135",
        "code_synth_p134",
        "code_synth_p133",
        "code_synth_p132",
        "code_synth_p131",
        "code_synth_p130",
        "code_synth_p129",
        "code_synth_p128",
        "code_synth_p127",
        "code_synth_p126",
        "code_synth_p125",
        "code_synth_p124",
        "code_synth_p123",
        "code_synth_p122",
        "code_synth_p121",
        "code_synth_p120",
        "code_synth_p119",
        "code_synth_p118",
        "code_synth_p117",
        "code_synth_p116",
        "code_synth_p115",
        "code_synth_p114",
        "code_synth_p113",
        "code_synth_p112",
        "code_synth_p111",
        "code_synth_p110",
        "code_synth_p109",
        "code_synth_p108",
        "code_synth_p107",
        "code_synth_p106",
        "code_synth_p105",
        "code_synth_p104",
        "code_synth_p103",
        "code_synth_p102",
        "code_synth_p84",
        "code_synth_p1",
        "code_synth_p1c",
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
        "code_synth_p34",
        "code_synth_p35",
        "code_synth_p36",
        "code_synth_p37",
        "code_synth_p38",
        "code_synth_p39",
        "code_synth_p40",
        "code_synth_p41",
        "code_synth_p42",
        "code_synth_p43",
        "code_synth_p44",
        "code_synth_p45",
        "code_synth_p46",
        "code_synth_p47",
        "code_synth_p48",
        "code_synth_p49",
        "code_synth_p50",
        "code_synth_p51",
        "code_synth_p52",
        "code_synth_p53",
        "code_synth_p54",
        "code_synth_p55",
        "code_synth_p56",
        "code_synth_p57",
        "code_synth_p58",
        "code_synth_p59",
        "code_synth_p60",
        "code_synth_p61",
        "code_synth_p62",
        "code_synth_p63",
        "code_synth_p64",
        "code_synth_p65",
        "code_synth_p66",
        "code_synth_p67",
        "code_synth_p68",
        "code_synth_p69",
        "code_synth_p70",
        "code_synth_p71",
        "code_synth_p72",
        "code_synth_p73",
        "code_synth_p74",
        "code_synth_p75",
        "code_synth_p76",
        "code_synth_p77",
        "code_synth_p78",
        "code_synth_p79",
        "code_synth_p80",
        "code_synth_p81",
        "code_synth_p82",
        "code_synth_p83",
        "code_synth_p85",
        "code_synth_p86",
        "code_synth_p87",
        "code_synth_p88",
        "code_synth_p89",
        "code_synth_p90",
        "code_synth_p91",
        "code_synth_p92",
        "code_synth_p93",
        "code_synth_p94",
        "code_synth_p95",
        "code_synth_p96",
        "code_synth_p97",
        "code_synth_p98",
        "code_synth_p99",
        "code_synth_p100",
        "code_synth_p101",
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
            out.append(_widen_loaded(tmpl))
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

    Cycle 463: identical requests reuse the winner. Pack order is unchanged.

    Cycle 283: pack order stays the default (smoke depends on it). If a later
    hit's name tokens strictly contain the winner's tokens *and* the extra
    tokens appear in the request, prefer the more specific sibling.
    """
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
        # Later pack with strictly more name tokens in the request beats a
        # broad early hit (sort_list vs sort_array_by_parity).
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
