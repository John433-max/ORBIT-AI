"""ORBIT FastAPI entrypoint (OpenAI-compatible + v2 routes).

Full local tree also contains chat/completions streaming and model load
in the complete workspace api.py. This published module mounts the extracted
routers so the server imports on the GitHub tree.

Run: uvicorn api:app --reload --port 8000
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("orbit.api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ORBIT AI — Local AI Agent Runtime API")

_ORBIT_API_KEY = (os.environ.get("ORBIT_API_KEY") or "").strip()
if _ORBIT_API_KEY:

    @app.middleware("http")
    async def _api_key_gate(request: Request, call_next):
        if request.url.path in ("/health", "/healthz", "/", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)
        auth = request.headers.get("authorization") or ""
        xkey = request.headers.get("x-api-key") or ""
        token = ""
        if auth.lower().startswith("bearer "):
            token = auth[7:].strip()
        elif xkey:
            token = xkey.strip()
        if token != _ORBIT_API_KEY:
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        return await call_next(request)

try:
    from api_routes.openai_compat import router as _openai_router
    app.include_router(_openai_router)
except Exception as exc:
    logger.warning("openai_compat router not mounted: %s", exc)

try:
    from api_routes.routes_extra import router as _v2_router
    app.include_router(_v2_router)
except Exception as exc:
    logger.warning("v2 router not mounted: %s", exc)


@app.get("/")
def root():
    return {"ok": True, "service": "orbit-api"}


@app.get("/health")
@app.get("/healthz")
def health():
    return {"ok": True, "status": "healthy"}
