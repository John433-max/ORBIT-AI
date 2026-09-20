"""Model provider abstraction — agents depend on ModelProvider, not TinyLM."""

from orbit.models.base import (
    GenerateRequest,
    GenerateResult,
    ModelProvider,
    ModelInfo,
)
from orbit.models.router import ModelRouter, get_default_provider
from orbit.models.gguf import GGUFProvider

# Optional extras: a missing sibling file must not break EchoProvider imports in CI.
try:
    from orbit.models.resilient import ResilientProvider, build_failover_chain
except ImportError:  # pragma: no cover
    ResilientProvider = None  # type: ignore[misc, assignment]
    build_failover_chain = None  # type: ignore[misc, assignment]

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
