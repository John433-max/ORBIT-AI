#!/usr/bin/env python3
"""
ORBIT launcher / CLI.

  python run_orbit.py                 # serve (default)
  python run_orbit.py serve
  python run_orbit.py doctor
  python run_orbit.py status
  python run_orbit.py chat "hello"
  python run_orbit.py --check         # legacy alias for doctor
  python run_orbit.py --port 8080
"""

from __future__ import annotations

import argparse
import json
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


def cmd_doctor(_args=None) -> int:
    """Diagnose runtime readiness with severity levels.

    CRITICAL / ERROR failures make Overall not READY.
    WARNING / OPTIONAL (e.g. Ollama down while TinyLM works) do not.
    """
    print("ORBIT Doctor")
    print("─" * 40)

    results: list[tuple[str, bool, str, str]] = []

    def row(name: str, ok: bool, detail: str = "", severity: str = "error"):
        mark = "✓" if ok else "✗"
        results.append((name, ok, detail, severity))
        sev = "" if ok else f" [{severity.upper()}]"
        extra = f"  {detail}" if detail else ""
        print(f"{name:<16} {mark}{sev}{extra}")

    row("Python", sys.version_info >= (3, 10), f"{sys.version.split()[0]}", "critical")

    problems = check_environment()
    missing_core = [x for x in problems if "not installed" in x and "fastapi" not in x and "uvicorn" not in x]
    missing_api = [x for x in problems if "fastapi" in x or "uvicorn" in x]
    if missing_core:
        row("Dependencies", False, "; ".join(missing_core + missing_api), "error")
    elif missing_api:
        row("Dependencies", False, "; ".join(missing_api) + " (needed for serve)", "warning")
    else:
        row("Dependencies", True, "ok", "info")

    try:
        from orbit.core.config import load_config
        from orbit.models.router import build_provider

        cfg = load_config()
        row("Config", True, f"provider={cfg.model_provider}", "info")
        provider = build_provider(cfg)
        hc = provider.health_check()
        row(
            "ModelProvider",
            bool(hc.get("ok")),
            f"{provider.name} {hc}",
            "critical",
        )
    except Exception as e:
        row("ModelProvider", False, str(e), "critical")

    try:
        from orbit.models.tinylm_provider import TinyLMProvider

        hc = TinyLMProvider().health_check()
        row("TinyLM", bool(hc.get("ok")), str(hc.get("weights") or hc.get("error") or ""), "warning")
    except Exception as e:
        row("TinyLM", False, str(e), "warning")

    try:
        from orbit.models.ollama import OllamaProvider

        hc = OllamaProvider().health_check()
        row(
            "Ollama",
            bool(hc.get("ok")),
            "available" if hc.get("ok") else str(hc.get("error", ""))[:60],
            "optional",
        )
    except Exception as e:
        row("Ollama", False, str(e), "optional")

    try:
        from tools.base import ToolRegistry
        from tools import CalculatorTool

        reg = ToolRegistry()
        reg.register(CalculatorTool())
        row("Tools", True, "registry ok", "info")
    except Exception as e:
        row("Tools", False, str(e), "error")

    try:
        from orbit_ai import OrbitAI

        ai = OrbitAI(persist=False, load_model=False)
        st = ai.status()
        row("OrbitAI", True, f"agents={len(st.get('agents') or [])}", "error")
    except Exception as e:
        row("OrbitAI", False, str(e), "error")

    root = Path(__file__).resolve().parent
    row("Web UI", (root / "webui" / "index.html").exists(), "", "warning")
    row("API module", (root / "api.py").exists(), "", "warning")

    data = root / ".orbit_data"
    row(
        "Data dir",
        True,
        str(data) + (" (exists)" if data.exists() else " (will create)"),
        "info",
    )

    print("─" * 40)
    blocking = [r for r in results if (not r[1]) and r[3] in ("critical", "error")]
    warnings = [r for r in results if (not r[1]) and r[3] in ("warning", "optional")]
    if not blocking:
        print("Overall: READY" + (f"  ({len(warnings)} non-blocking issue(s))" if warnings else ""))
        return 0
    print(f"Overall: NOT READY  ({len(blocking)} blocking, {len(warnings)} non-blocking)")
    for name, _ok, detail, sev in blocking:
        print(f"  - [{sev}] {name}: {detail}")
    return 1


def cmd_status(_args=None) -> int:
    try:
        from orbit.core.config import load_config
        from orbit.models.router import ModelRouter
        from orbit_ai import OrbitAI

        cfg = load_config()
        router = ModelRouter(cfg=cfg)
        ai = OrbitAI(persist=False, load_model=False)
        out = {
            "config": cfg.to_dict(),
            "provider": router.info().to_dict(),
            "provider_health": router.health(),
            "orbit": ai.status(),
        }
        print(json.dumps(out, indent=2, default=str))
        return 0
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1


def cmd_chat(args) -> int:
    msg = " ".join(args.message or []).strip()
    if not msg:
        print("Usage: python run_orbit.py chat \"your message\"")
        return 2
    from orbit_ai import OrbitAI

    ai = OrbitAI(persist=not getattr(args, "no_persist", False))
    print(ai.ask(msg))
    return 0


def cmd_serve(args) -> int:
    problems = check_environment()
    print("ORBIT launcher")
    print("--------------")
    if problems:
        print("Environment issues:")
        for x in problems:
            print("  -", x)
        if getattr(args, "check", False):
            return 1
        print("Continuing anyway (some features may be unavailable)...")
    else:
        print("Environment: OK")

    try:
        from orbit.core.config import load_config
        from orbit.models.router import ModelRouter

        cfg = load_config()
        router = ModelRouter(cfg=cfg)
        print(f"Model provider: {router.provider.name}  health={router.health().get('ok')}")
    except Exception as e:
        print(f"Model provider: {e}")

    try:
        from model import get_preset

        cfgm = get_preset("tiny")
        print(f"Default preset 'tiny': {cfgm.model.estimate_parameters():,} params")
    except Exception as e:
        print(f"Config: {e}")

    host = getattr(args, "host", None) or "127.0.0.1"
    port = getattr(args, "port", None) or 8000
    try:
        from orbit.core.config import load_config

        c = load_config()
        host = getattr(args, "host", None) or c.host
        port = getattr(args, "port", None) or c.port
    except Exception:
        pass

    url = f"http://{host}:{port}/"
    print(f"\nStarting UNIFIED ORBIT AI → {url}")
    print("  Chat UI:     /")
    print("  Health:      /health")
    print("  API docs:    /docs")
    print("  Chat API:    POST /v1/chat/completions")
    print()

    try:
        import uvicorn
    except ImportError:
        print("uvicorn is required: pip install uvicorn fastapi")
        return 1

    uvicorn.run("api:app", host=host, port=int(port), reload=bool(getattr(args, "reload", False)))
    return 0


def cmd_eval(args) -> int:
    from evals.runner import run_eval
    path = getattr(args, "dataset", None) or "evals/datasets/smoke.jsonl"
    report = run_eval(dataset_path=path)
    print(f"accuracy={report['accuracy']:.2%}  {report['n_ok']}/{report['n']}  → {report.get('path')}")
    for cat, st in (report.get("by_category") or {}).items():
        print(f"  {cat}: {st['ok']}/{st['n']} ({st['accuracy']:.0%})")
    return 0 if report["accuracy"] >= 0.5 else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0].startswith("-"):
        p = argparse.ArgumentParser(description="ORBIT one-command launcher")
        p.add_argument("--host", default=None)
        p.add_argument("--port", type=int, default=None)
        p.add_argument("--reload", action="store_true")
        p.add_argument("--check", action="store_true", help="Validate environment (doctor)")
        args = p.parse_args(argv)
        if args.check:
            return cmd_doctor(args)
        return cmd_serve(args)

    parser = argparse.ArgumentParser(description="ORBIT CLI")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("doctor", help="Check environment and providers")
    sub.add_parser("status", help="JSON status: config + provider + OrbitAI")
    p_chat = sub.add_parser("chat", help="One-shot chat via OrbitAI")
    p_chat.add_argument("message", nargs="*")
    p_chat.add_argument("--no-persist", action="store_true")
    p_eval = sub.add_parser("eval", help="Run smoke evaluation suite")
    p_eval.add_argument("--dataset", default="evals/datasets/smoke.jsonl")
    p_serve = sub.add_parser("serve", help="Start API + Web UI")
    p_serve.add_argument("--host", default=None)
    p_serve.add_argument("--port", type=int, default=None)
    p_serve.add_argument("--reload", action="store_true")

    args = parser.parse_args(argv)
    if args.cmd == "doctor":
        return cmd_doctor(args)
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "chat":
        return cmd_chat(args)
    if args.cmd == "eval":
        return cmd_eval(args)
    if args.cmd == "serve":
        return cmd_serve(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
