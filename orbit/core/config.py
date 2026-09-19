"""Central ORBIT configuration from environment + optional YAML."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _bool(v: Optional[str], default: bool = False) -> bool:
    if v is None or v == "":
        return default
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def _int(v: Optional[str], default: int) -> int:
    try:
        return int(v) if v is not None and str(v).strip() != "" else default
    except ValueError:
        return default


@dataclass
class OrbitConfig:
    model_provider: str = "auto"
    model_name: str = ""
    host: str = "127.0.0.1"
    port: int = 8000
    max_steps: int = 20
    max_tool_calls: int = 30
    max_tokens: int = 256
    temperature: float = 0.7
    rag_enabled: bool = True
    memory_enabled: bool = True
    web_enabled: bool = True
    ollama_base_url: str = "http://127.0.0.1:11434"
    openai_base_url: str = "http://127.0.0.1:8000/v1"
    openai_api_key: str = ""
    tinylm_preset: str = "rope"
    tinylm_ckpt: str = ""
    data_dir: str = ".orbit_data"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_provider": self.model_provider,
            "model_name": self.model_name,
            "host": self.host,
            "port": self.port,
            "max_steps": self.max_steps,
            "max_tool_calls": self.max_tool_calls,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "rag_enabled": self.rag_enabled,
            "memory_enabled": self.memory_enabled,
            "web_enabled": self.web_enabled,
            "ollama_base_url": self.ollama_base_url,
            "openai_base_url": self.openai_base_url,
            "tinylm_preset": self.tinylm_preset,
            "tinylm_ckpt": self.tinylm_ckpt or None,
            "data_dir": self.data_dir,
        }


def load_config(env: Optional[Dict[str, str]] = None) -> OrbitConfig:
    e = env if env is not None else os.environ
    return OrbitConfig(
        model_provider=(e.get("ORBIT_MODEL_PROVIDER") or e.get("ORBIT_MODEL") or "auto").strip().lower(),
        model_name=(e.get("ORBIT_MODEL_NAME") or "").strip(),
        host=(e.get("ORBIT_HOST") or "127.0.0.1").strip(),
        port=_int(e.get("ORBIT_PORT"), 8000),
        max_steps=_int(e.get("ORBIT_MAX_STEPS"), 20),
        max_tool_calls=_int(e.get("ORBIT_MAX_TOOL_CALLS"), 30),
        max_tokens=_int(e.get("ORBIT_MAX_TOKENS"), 256),
        temperature=float(e.get("ORBIT_TEMPERATURE") or 0.7),
        rag_enabled=_bool(e.get("ORBIT_RAG_ENABLED"), True),
        memory_enabled=_bool(e.get("ORBIT_MEMORY_ENABLED"), True),
        web_enabled=_bool(e.get("ORBIT_WEB_ENABLED"), True),
        ollama_base_url=(e.get("ORBIT_OLLAMA_BASE_URL") or "http://127.0.0.1:11434").rstrip("/"),
        openai_base_url=(e.get("ORBIT_OPENAI_BASE_URL") or "http://127.0.0.1:8000/v1").rstrip("/"),
        openai_api_key=(e.get("ORBIT_OPENAI_API_KEY") or e.get("OPENAI_API_KEY") or "").strip(),
        tinylm_preset=(e.get("ORBIT_TINYLM_PRESET") or "rope").strip(),
        tinylm_ckpt=(e.get("ORBIT_TINYLM_CKPT") or "").strip(),
        data_dir=(e.get("ORBIT_DATA_DIR") or ".orbit_data").strip(),
    )
