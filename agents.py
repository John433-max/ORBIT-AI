"""Assembled agents module (parts on disk for GitHub size limits)."""
from pathlib import Path
_dir = Path(__file__).resolve().parent
_parts = sorted(_dir.glob("_agents_part_*.py.txt"))
if not _parts:
    raise ImportError("missing _agents_part_*.py.txt fragments")
_src = "".join(p.read_text(encoding="utf-8") for p in _parts)
exec(compile(_src, str(_dir / "agents_assembled.py"), "exec"), globals())
