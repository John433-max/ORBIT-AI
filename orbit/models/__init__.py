"""Model provider abstraction — agents depend on ModelProvider, not TinyLM."""

from orbit.models.base import (
    GenerateRequest,
    GenerateResult,
    ModelProvider,
    ModelInfo,
)
from orbit.models.router import ModelRouter, get_default_provider
from orbit.models.gguf import GGUFProvider
from orbit.models.resilient import ResilientProvider, build_failover_chain

__all__ = [
    "GenerateRequest",
    "GenerateResult",
    "ModelProvider",
    "ModelInfo",
    "ModelRouter",
    "get_default_provider",
    "GGUFProvider",
    "ResilientProvider",
    "build_failover_chain",
]
