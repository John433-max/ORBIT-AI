#!/usr/bin/env python3
"""
One-command ORBIT launcher.

  python run_orbit.py              # start API + print UI URL
  python run_orbit.py --check      # validate env only
  python run_orbit.py --port 8080
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def check_environment() -> list[str]:
    problems = []
    try:
        import numpy  # noqa: F401
    except ImportError:
        problems.append("numpy not installed")
    try:
        import yaml  # noqa: F401
    except ImportError:
        problems.append("PyYAML not installed (pip install PyYAML)")
    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
    except ImportError:
        problems.append("fastapi/uvicorn not installed (pip install -r requirements.txt)")

    try:
        from model import TinyLM, get_preset  # noqa: F401
    except Exception as e:
        problems.append(f"model package import failed: {e}")

    root = Path(__file__).resolve().parent
    if not (root / "webui" / "index.html").exists():
        problems.append("webui/index.html missing")
    return problems


def main(argv=None):
    p = argparse.ArgumentParser(description="ORBIT one-command launcher")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--reload", action="store_true")
    p.add_argument("--check", action="store_true", help="Validate environment and exit")
    args = p.parse_args(argv)

    print("ORBIT launcher")
    print("--------------")
    problems = check_environment()
    if problems:
        print("Environment issues:")
        for x in problems:
            print("  -", x)
        if args.check:
            return 1
        print("Continuing anyway (some features may be unavailable)...")
    else:
        print("Environment: OK")

    try:
        from model import get_preset
        cfg = get_preset("tiny")
        print(f"Default preset 'tiny': {cfg.model.estimate_parameters():,} params")
    except Exception as e:
        print(f"Config: {e}")

    ckpt = Path("checkpoint_base.npz")
    ckpt2 = Path("checkpoint_large.npz")
    if ckpt.exists():
        print(f"Checkpoint: {ckpt}")
    elif ckpt2.exists():
        print(f"Checkpoint: {ckpt2}")
    else:
        print("Checkpoint: none (chat still works via retrieval/agents)")

    if args.check:
        return 0 if not problems else 1

    url = f"http://{args.host}:{args.port}/"
    print(f"\nStarting UNIFIED ORBIT AI → {url}")
    print("  Chat UI:     /")
    print("  Health:      /health")
    print("  API docs:    /docs")
    print("  Chat API:    POST /v1/chat/completions")
    print("  Documents:   POST /v1/documents")
    print("  Agents:      code, research, document, lab, calculator, memory, ...")
    print("  Facade:      python orbit_ai.py \"what is your name\"")
    print()

    try:
        import uvicorn
    except ImportError:
        print("uvicorn is required: pip install uvicorn fastapi")
        return 1

    uvicorn.run("api:app", host=args.host, port=args.port, reload=args.reload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
