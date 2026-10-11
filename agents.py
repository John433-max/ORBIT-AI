# Cycle 566 self-extracting agents.py (CI restore)
import base64, gzip
from pathlib import Path
_dir = Path(__file__).resolve().parent
_B64 = (_dir / "agents_b64_a.txt").read_text() + (_dir / "agents_b64_b.txt").read_text()
_src = gzip.decompress(base64.b64decode(_B64)).decode()
exec(compile(_src, __file__, "exec"), globals())
