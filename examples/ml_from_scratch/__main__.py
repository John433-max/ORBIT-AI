"""CLI: python -m examples.ml_from_scratch [demo_name]"""

from __future__ import annotations

import json
import sys

from . import DEMOS, run_all, summary


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("all", "--all"):
        rows = run_all()
        for r in rows:
            status = "OK" if r.get("ok") else "FAIL"
            print(f"[{status}] {r.get('demo')}: {r.get('metric')} — {r.get('idea')}")
        s = summary()
        print("---")
        print(json.dumps({"ok": s["ok"], "n": s["n"]}, indent=2))
        return 0 if s["ok"] else 1
    name = argv[0]
    if name not in DEMOS:
        print(f"unknown demo {name!r}; choose from: {', '.join(DEMOS)}")
        return 2
    out = DEMOS[name]()
    out["demo"] = name
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
