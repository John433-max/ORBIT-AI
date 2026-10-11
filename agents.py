# Cycle 566 bootstrap: fetch agents@340ff3b and apply factorial math early-out.
import urllib.request
_URL = (
    "https://raw.githubusercontent.com/John433-max/ORBIT-AI/"
    "340ff3b3c42b0a34e1b5e39fdb6aea7993656ff9/agents.py"
)
_src = urllib.request.urlopen(_URL, timeout=60).read().decode()
_needle = "    # Bare problem titles that match a verified template should synthesize,"
_guard = (
    "    # Cycle 566: numeric factorial is math, not a write ask.\n"
    "    if re.search(r\"\\bfactorial\\s+(?:of\\s+)?\\d+|\\d+\\s*!\", text, re.I):\n"
    "        return False\n"
    + _needle
)
if _needle not in _src:
    raise RuntimeError("Cycle 566 bootstrap: anchor not found")
if "Cycle 566" not in _src:
    _src = _src.replace(_needle, _guard, 1)
exec(compile(_src, __file__, "exec"), globals())
