"""Multi-provider failover + simple in-process response cache.

Wraps one or more ModelProvider instances and:
  - retries / fails over on HTTP 429, 5xx, timeouts, and transport errors
  - rotates among providers and optional API-key list
  - optionally caches identical GenerateRequest results (LRU, TTL)

Does not invent cloud providers: it only chains whatever providers you pass
(or that build_failover_chain() constructs from OrbitConfig / env).
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Sequence

from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider

logger = logging.getLogger("orbit.models.resilient")

# Status / error signals that justify trying the next provider or key.
_RETRYABLE_MARKERS = (
    "429",
    "rate limit",
    "rate_limit",
    "timeout",
    "timed out",
    "connection",
    "temporarily unavailable",
    "503",
    "502",
    "504",
    "overloaded",
)


def _is_retryable(result: GenerateResult) -> bool:
    if result.ok and result.text:
        return False
    err = (result.error or "").lower()
    if not err and not result.ok:
        return True
    return any(m in err for m in _RETRYABLE_MARKERS)


def _request_cache_key(req: GenerateRequest) -> str:
    payload = {
        "prompt": req.prompt or "",
        "messages": req.messages or [],
        "max_tokens": req.max_tokens,
        "temperature": req.temperature,
        "stop": req.stop,
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class _CacheEntry:
    result: GenerateResult
    expires_at: float


class LRUResponseCache:
    """Thread-safe LRU with TTL for identical generation requests."""

    def __init__(self, max_entries: int = 256, ttl_s: float = 300.0):
        self.max_entries = max(1, max_entries)
        self.ttl_s = max(1.0, ttl_s)
        self._data: OrderedDict[str, _CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[GenerateResult]:
        now = time.time()
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self.misses += 1
                return None
            if entry.expires_at < now:
                self._data.pop(key, None)
                self.misses += 1
                return None
            self._data.move_to_end(key)
            self.hits += 1
            return entry.result

    def put(self, key: str, result: GenerateResult) -> None:
        if not result.ok or not result.text:
            return
        with self._lock:
            self._data[key] = _CacheEntry(result=result, expires_at=time.time() + self.ttl_s)
            self._data.move_to_end(key)
            while len(self._data) > self.max_entries:
                self._data.popitem(last=False)

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {"hits": self.hits, "misses": self.misses, "size": len(self._data)}


@dataclass
class ProviderSlot:
    """One callable backend, optionally with a dedicated API key override."""

    provider: ModelProvider
    label: str = ""
    api_key: Optional[str] = None  # if set, applied before generate when supported


class ResilientProvider(ModelProvider):
    """Failover across ProviderSlot list; optional LRU cache."""

    name = "resilient"

    def __init__(
        self,
        slots: Sequence[ProviderSlot],
        *,
        max_attempts: int = 4,
        cache: Optional[LRUResponseCache] = None,
        cache_enabled: bool = True,
    ):
        if not slots:
            raise ValueError("ResilientProvider requires at least one ProviderSlot")
        self.slots: List[ProviderSlot] = list(slots)
        self.max_attempts = max(1, max_attempts)
        self.cache = cache if cache is not None else LRUResponseCache()
        self.cache_enabled = cache_enabled
        self._lock = threading.Lock()
        self._cursor = 0
        self.failover_count = 0

    def health_check(self) -> Dict[str, Any]:
        reports = []
        any_ok = False
        for slot in self.slots:
            try:
                hc = slot.provider.health_check()
            except Exception as e:
                hc = {"ok": False, "error": str(e)}
            reports.append({"label": slot.label or slot.provider.name, **hc})
            if hc.get("ok"):
                any_ok = True
        return {"ok": any_ok, "provider": "resilient", "backends": reports}

    def info(self) -> ModelInfo:
        primary = self.slots[0].provider
        try:
            base = primary.info()
        except Exception:
            base = ModelInfo(name="resilient", provider="resilient")
        return ModelInfo(
            name=f"resilient:{base.name}",
            provider="resilient",
            supports_tools=base.supports_tools,
            supports_stream=base.supports_stream,
            context_length=base.context_length,
            metadata={
                "backends": [s.label or s.provider.name for s in self.slots],
                "cache": self.cache.stats() if self.cache_enabled else None,
            },
        )

    def _apply_key(self, slot: ProviderSlot) -> None:
        if slot.api_key is None:
            return
        # OpenAICompatibleProvider and similar keep api_key as a public attr.
        if hasattr(slot.provider, "api_key"):
            setattr(slot.provider, "api_key", slot.api_key)

    def generate(self, request: GenerateRequest) -> GenerateResult:
        if self.cache_enabled and not request.stream:
            key = _request_cache_key(request)
            hit = self.cache.get(key)
            if hit is not None:
                return hit
        else:
            key = None

        errors: List[str] = []
        n = len(self.slots)
        with self._lock:
            start = self._cursor

        for attempt in range(min(self.max_attempts, n * 2)):
            idx = (start + attempt) % n
            slot = self.slots[idx]
            label = slot.label or slot.provider.name
            try:
                self._apply_key(slot)
                result = slot.provider.generate(request)
            except Exception as e:
                result = GenerateResult(
                    text="", ok=False, error=str(e), provider=label, model=getattr(slot.provider, "model", "")
                )

            if result.ok and result.text is not None:
                with self._lock:
                    self._cursor = idx
                if key is not None:
                    self.cache.put(key, result)
                if attempt > 0:
                    self.failover_count += 1
                    logger.info("resilient failover succeeded via %s after %d attempt(s)", label, attempt + 1)
                return result

            errors.append(f"{label}: {result.error or 'empty/failed'}")
            if not _is_retryable(result) and attempt + 1 >= n:
                # Non-retryable from every tried backend — stop early.
                break
            logger.warning("resilient: backend %s failed (%s); trying next", label, result.error)

        self.failover_count += 1
        return GenerateResult(
            text="",
            ok=False,
            error="all providers failed: " + " | ".join(errors[:6]),
            provider="resilient",
        )

    def stream(self, request: GenerateRequest) -> Iterator[str]:
        # Stream from first healthy slot; on failure fall back to generate().
        for slot in self.slots:
            try:
                self._apply_key(slot)
                if slot.provider.health_check().get("ok"):
                    yield from slot.provider.stream(request)
                    return
            except Exception as e:
                logger.warning("resilient stream skip %s: %s", slot.label or slot.provider.name, e)
        result = self.generate(request)
        if result.text:
            yield result.text


def _split_keys(raw: str) -> List[str]:
    return [k.strip() for k in (raw or "").replace(";", ",").split(",") if k.strip()]


def build_failover_chain(cfg=None) -> ResilientProvider:
    """Build ResilientProvider from OrbitConfig / environment.

    Env knobs:
      ORBIT_OPENAI_API_KEY or OPENAI_API_KEY — comma-separated keys to rotate
      ORBIT_FAILOVER_PROVIDERS — comma list: openai,ollama,tinylm,echo
      ORBIT_CACHE_TTL_S / ORBIT_CACHE_MAX — response cache
    """
    from orbit.core.config import load_config
    from orbit.models.echo import EchoProvider
    from orbit.models.ollama import OllamaProvider
    from orbit.models.openai_compatible import OpenAICompatibleProvider
    from orbit.models.tinylm_provider import TinyLMProvider

    cfg = cfg or load_config()
    order = [
        p.strip().lower()
        for p in (os.environ.get("ORBIT_FAILOVER_PROVIDERS") or "openai,ollama,tinylm,echo").split(",")
        if p.strip()
    ]
    keys = _split_keys(os.environ.get("ORBIT_OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY") or cfg.openai_api_key)
    if not keys:
        keys = [""]

    slots: List[ProviderSlot] = []
    for kind in order:
        if kind in ("openai", "openai_compatible", "remote"):
            for i, key in enumerate(keys):
                slots.append(
                    ProviderSlot(
                        provider=OpenAICompatibleProvider(
                            model=cfg.model_name or "gpt-4o-mini",
                            base_url=cfg.openai_base_url,
                            api_key=key,
                        ),
                        label=f"openai[{i}]",
                        api_key=key or None,
                    )
                )
        elif kind == "ollama":
            slots.append(
                ProviderSlot(
                    provider=OllamaProvider(model=cfg.model_name or "llama3.2", base_url=cfg.ollama_base_url),
                    label="ollama",
                )
            )
        elif kind == "tinylm":
            try:
                slots.append(
                    ProviderSlot(
                        provider=TinyLMProvider(preset=cfg.tinylm_preset, ckpt_path=cfg.tinylm_ckpt or None),
                        label="tinylm",
                    )
                )
            except Exception as e:
                logger.warning("tinylm slot skipped: %s", e)
        elif kind in ("echo", "test"):
            slots.append(ProviderSlot(provider=EchoProvider(), label="echo"))

    if not slots:
        slots = [ProviderSlot(provider=EchoProvider(), label="echo")]

    ttl = float(os.environ.get("ORBIT_CACHE_TTL_S") or 300)
    max_entries = int(os.environ.get("ORBIT_CACHE_MAX") or 256)
    cache_on = (os.environ.get("ORBIT_CACHE_ENABLED") or "1").strip().lower() not in ("0", "false", "no")
    return ResilientProvider(
        slots,
        cache=LRUResponseCache(max_entries=max_entries, ttl_s=ttl),
        cache_enabled=cache_on,
    )
