"""Restricted YAML subset for ORBIT configs when PyYAML is absent.

Supports the shapes in configs/*.yaml:
- comments and blank lines
- nested maps
- scalars: null, bool, int, float, plain/quoted strings
- flow sequences: [0.9, 0.95]
- block sequences: - item

Does not support anchors, tags, multiline |/> blocks, or complex keys.
When PyYAML is installed, callers should prefer yaml.safe_load.
"""

from __future__ import annotations

from typing import Any, List, Tuple


def _strip_comment(line: str) -> str:
    out = []
    quote = ""
    for ch in line:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in ("'", '"'):
            quote = ch
            out.append(ch)
            continue
        if ch == "#":
            break
        out.append(ch)
    return "".join(out).rstrip()


def _parse_scalar(text: str) -> Any:
    s = text.strip()
    if s == "" or s in ("null", "~", "Null", "NULL"):
        return None
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part) for part in _split_flow(inner)]
    try:
        if any(c in s for c in (".", "e", "E")):
            return float(s)
        return int(s)
    except ValueError:
        return s


def _split_flow(inner: str) -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    quote = ""
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            continue
        if ch in "[{":
            depth += 1
            buf.append(ch)
            continue
        if ch in "]}":
            depth -= 1
            buf.append(ch)
            continue
        if ch == "," and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    if buf:
        parts.append("".join(buf).strip())
    return parts


def _lines(text: str) -> List[Tuple[int, str]]:
    rows: List[Tuple[int, str]] = []
    for raw in text.splitlines():
        cleaned = _strip_comment(raw)
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        rows.append((indent, cleaned.strip()))
    return rows


def _parse_block(rows: List[Tuple[int, str]], i: int, indent: int) -> Tuple[Any, int]:
    if i >= len(rows) or rows[i][0] < indent:
        return {}, i
    if rows[i][1].startswith("- "):
        return _parse_list(rows, i, indent)
    return _parse_map(rows, i, indent)


def _parse_map(rows: List[Tuple[int, str]], i: int, indent: int) -> Tuple[dict, int]:
    out: dict = {}
    while i < len(rows) and rows[i][0] == indent and not rows[i][1].startswith("- "):
        key, _, rest = rows[i][1].partition(":")
        key = key.strip()
        rest = rest.strip()
        i += 1
        if rest == "":
            if i < len(rows) and rows[i][0] > indent:
                child, i = _parse_block(rows, i, rows[i][0])
                out[key] = child
            else:
                out[key] = None
        else:
            out[key] = _parse_scalar(rest)
    return out, i


def _parse_list(rows: List[Tuple[int, str]], i: int, indent: int) -> Tuple[list, int]:
    out: list = []
    while i < len(rows) and rows[i][0] == indent and rows[i][1].startswith("- "):
        rest = rows[i][1][2:].strip()
        i += 1
        if rest == "":
            if i < len(rows) and rows[i][0] > indent:
                child, i = _parse_block(rows, i, rows[i][0])
                out.append(child)
            else:
                out.append(None)
        elif ":" in rest and not rest.startswith("[") and not (rest[:1] in ("'", '"')):
            # "- key: value" inline map item
            key, _, val = rest.partition(":")
            item = {key.strip(): _parse_scalar(val.strip()) if val.strip() else None}
            if val.strip() == "" and i < len(rows) and rows[i][0] > indent:
                child, i = _parse_block(rows, i, rows[i][0])
                if isinstance(child, dict):
                    item[key.strip()] = child
            out.append(item)
        else:
            out.append(_parse_scalar(rest))
    return out, i


def safe_load(text: str) -> Any:
    rows = _lines(text or "")
    if not rows:
        return None
    value, i = _parse_block(rows, 0, rows[0][0])
    if i != len(rows):
        raise ValueError(f"yaml_lite: unparsed content at {rows[i]!r}")
    return value


def safe_dump(obj: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(obj, dict):
        lines = []
        for key, val in obj.items():
            if isinstance(val, (dict, list)) and val:
                lines.append(f"{pad}{key}:")
                lines.append(safe_dump(val, indent + 2).rstrip("\n"))
            else:
                lines.append(f"{pad}{key}: {_emit_scalar(val)}")
        return "\n".join(lines) + "\n"
    if isinstance(obj, list):
        lines = []
        for item in obj:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(safe_dump(item, indent + 2).rstrip("\n"))
            else:
                lines.append(f"{pad}- {_emit_scalar(item)}")
        return "\n".join(lines) + "\n"
    return pad + _emit_scalar(obj) + "\n"


def _emit_scalar(val: Any) -> str:
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return repr(val) if isinstance(val, float) else str(val)
    if isinstance(val, list) and all(not isinstance(x, (dict, list)) for x in val):
        return "[" + ", ".join(_emit_scalar(x) for x in val) + "]"
    text = str(val)
    if text == "" or any(c in text for c in ":#[]{}") or text.lower() in ("null", "true", "false"):
        return '"' + text.replace('"', '\\"') + '"'
    return text
