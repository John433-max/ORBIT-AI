"""Unit tests for ModelProvider abstraction (Phase C)."""

from __future__ import annotations

from orbit.core.config import OrbitConfig, load_config
from orbit.models.base import GenerateRequest
from orbit.models.echo import EchoProvider
from orbit.models.router import ModelRouter, build_provider


def test_load_config_defaults():
    cfg = load_config({})
    assert cfg.model_provider == "auto"
    assert cfg.host == "127.0.0.1"
    assert cfg.port == 8000


def test_load_config_env():
    cfg = load_config(
        {
            "ORBIT_MODEL_PROVIDER": "echo",
            "ORBIT_PORT": "9001",
            "ORBIT_MAX_STEPS": "5",
        }
    )
    assert cfg.model_provider == "echo"
    assert cfg.port == 9001
    assert cfg.max_steps == 5


def test_echo_provider_generate():
    p = EchoProvider()
    assert p.health_check()["ok"] is True
    r = p.generate(GenerateRequest(prompt="hello orbit"))
    assert r.ok and "hello orbit" in r.text
    r2 = p.generate(GenerateRequest(messages=[{"role": "user", "content": "ping"}]))
    assert "ping" in r2.text


def test_build_provider_echo():
    cfg = OrbitConfig(model_provider="echo")
    p = build_provider(cfg)
    assert p.name == "echo"
    assert p.generate(GenerateRequest(prompt="x")).ok


def test_model_router():
    router = ModelRouter(cfg=OrbitConfig(model_provider="echo"))
    out = router.generate(prompt="test")
    assert out.ok
    assert router.health()["ok"] is True
    info = router.info()
    assert info.provider == "echo"


def test_auto_prefers_healthy_ollama(monkeypatch):
    """Priority 5: auto must pick Ollama when its health check is ok."""
    from orbit.models import ollama as ollama_mod
    from orbit.models.ollama import OllamaProvider

    def fake_health(self):
        return {"ok": True, "provider": "ollama", "models": ["llama3.2"], "selected": self.model}

    monkeypatch.setattr(OllamaProvider, "health_check", fake_health)
    monkeypatch.setattr(ollama_mod.OllamaProvider, "health_check", fake_health)
    cfg = OrbitConfig(model_provider="auto")
    p = build_provider(cfg)
    assert p.name == "ollama"


def test_tinylm_provider_optional():
    from orbit.models.tinylm_provider import TinyLMProvider

    p = TinyLMProvider(preset="rope")
    hc = p.health_check()
    # Without full TinyLM stack in a partial checkout, health may fail — that is OK
    if not hc.get("ok"):
        return
    r = p.generate(GenerateRequest(prompt="hi", max_tokens=8, temperature=0.0))
    assert r.provider == "tinylm"


def test_tinylm_py310_fallback_generates():
    """CPython 3.12 bytecode snapshot must not block educational TinyLM on 3.10."""
    from pathlib import Path

    src = Path(__file__).resolve().parents[2] / "tinylm" / "_numpy_model_py310.py"
    if not src.exists():
        return
    from orbit.models.tinylm_provider import TinyLMProvider

    p = TinyLMProvider(preset="rope")
    hc = p.health_check()
    assert hc.get("ok"), hc
    r = p.generate(GenerateRequest(prompt="hi", max_tokens=4, temperature=0.0))
    assert r.ok, r.error
    assert r.provider == "tinylm"
    assert isinstance(r.text, str) and r.text


def test_ollama_urllib_health_and_generate_without_httpx():
    """Priority 5: a healthy daemon must be reachable without the httpx extra."""
    import json
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    from orbit.models.ollama import OllamaProvider

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            return

        def _send(self, payload: dict):
            raw = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            if self.path.startswith("/api/tags"):
                self._send({"models": [{"name": "llama3.2"}]})
                return
            self.send_response(404)
            self.end_headers()

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}")
            if self.path.startswith("/api/generate"):
                self._send({"response": f"echo:{body.get('prompt')}"})
                return
            if self.path.startswith("/api/chat"):
                msg = (body.get("messages") or [{}])[-1].get("content")
                self._send({"message": {"content": f"chat:{msg}"}})
                return
            self.send_response(404)
            self.end_headers()

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    # Exercise the stdlib path even when the API extra installed httpx.
    import builtins
    import sys
    saved_httpx = sys.modules.pop("httpx", None)
    real_import = builtins.__import__

    def _block_httpx(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "httpx" or name.startswith("httpx."):
            raise ImportError("httpx blocked for urllib fallback test")
        return real_import(name, globals, locals, fromlist, level)

    builtins.__import__ = _block_httpx
    try:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        p = OllamaProvider(model="llama3.2", base_url=base)
        hc = p.health_check()
        assert hc.get("ok") is True, hc
        assert "llama3.2" in hc.get("models", [])
        assert hc.get("transport") == "urllib"
        gen = p.generate(GenerateRequest(prompt="fusion", max_tokens=8))
        assert gen.ok and gen.text == "echo:fusion"
        chat = p.generate(GenerateRequest(messages=[{"role": "user", "content": "hi"}]))
        assert chat.ok and chat.text == "chat:hi"
    finally:
        builtins.__import__ = real_import
        if saved_httpx is not None:
            sys.modules["httpx"] = saved_httpx
        server.shutdown()
        server.server_close()
