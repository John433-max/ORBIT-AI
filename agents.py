"""ORBIT agents (GitHub CI surface) — gzip payload + expand on import."""
from __future__ import annotations
import base64, gzip, sys, types

_B64 = """
H4sIAAAAAAAAA+1ba2/bOhL9vl8h7W4BNyiSIuXH3QZFkyZt0jTdNGna3S9YlGzbRCXRpeQ4vfW/35Gx
"""

def _expand():
    code = gzip.decompress(base64.b64decode(_B64)).decode("utf-8")
    mod = types.ModuleType("agents")
    mod.__file__ = __file__
    exec(compile(code, __file__, "exec"), mod.__dict__)
    return mod

_m = _expand()
globals().update({k: v for k, v in _m.__dict__.items() if not k.startswith("_")})
