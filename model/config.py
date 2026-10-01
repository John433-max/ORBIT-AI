"""
ORBIT model & training configuration system.

All important dimensions and hyper-parameters live here (or in YAML files
under configs/).  Nothing that affects model shape or training dynamics
should be hard-coded inside model.py / model_torch.py / train*.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict, fields
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from model.yaml_lite import safe_dump as _yaml_lite_dump
from model.yaml_lite import safe_load as _yaml_lite_load


# ---------------------------------------------------------------------------
# ModelConfig — expanded parameter set
# ---------------------------------------------------------------------------

@dataclass
class ModelConfig:
    """Architecture hyper-parameters for TinyLM / TinyLMTorch."""

    # Core dimensions
    d_model: int = 128
    n_layers: int = 4
    n_heads: int = 8
    n_kv_heads: int = 4
    context_length: int = 128          # max_seq_len
    vocab_size: int = 1500

    # Derived / optional FFN
    ffn_multiplier: float = 8 / 3      # d_ff = int(d_model * ffn_multiplier)
    d_ff: Optional[int] = None         # if set, overrides ffn_multiplier
    multiple_of: int = 1               # round d_ff up to multiple_of (e.g. 64)

    # Positional / norm
    rope_theta: float = 10000.0
    rope_scaling: Optional[float] = None  # optional linear scale factor
    norm_epsilon: float = 1e-6
    norm_type: str = "rmsnorm"         # "rmsnorm" | "layernorm" (future)

    # Regularization / misc
    dropout: float = 0.0
    attention_dropout: float = 0.0
    residual_dropout: float = 0.0
    tie_embeddings: bool = True
    bias: bool = False                 # linear biases (kept False for TinyLM)

    # Attention extras
    use_flash_attention: bool = False  # advisory; CPU path ignores
    max_position_embeddings: Optional[int] = None  # alias override for context

    # Optional recursive reasoning (Architecture B)
    use_recursive_reasoning: bool = False
    n_sup: int = 4                     # supervision steps for reasoner

    # Init
    seed: int = 0
    emb_init_std: float = 0.02
    residual_init_scale: float = 1.0

    def __post_init__(self) -> None:
        if self.max_position_embeddings is not None and self.context_length == 128:
            # only apply if caller set max_position and left default context
            pass
        if self.max_position_embeddings:
            self.context_length = self.max_position_embeddings
        if self.d_ff is None:
            raw = int(self.d_model * self.ffn_multiplier)
            if self.multiple_of > 1:
                raw = ((raw + self.multiple_of - 1) // self.multiple_of) * self.multiple_of
            self.d_ff = raw
        self.validate()

    def validate(self) -> None:
        if self.vocab_size <= 0:
            raise ValueError(f"vocab_size must be positive, got {self.vocab_size}")
        if self.d_model % self.n_heads != 0:
            raise ValueError(
                f"d_model ({self.d_model}) must be divisible by n_heads ({self.n_heads})"
            )
        if self.n_heads % self.n_kv_heads != 0:
            raise ValueError(
                f"n_heads ({self.n_heads}) must be divisible by n_kv_heads ({self.n_kv_heads}) for GQA"
            )
        if self.n_kv_heads > self.n_heads:
            raise ValueError(
                f"n_kv_heads ({self.n_kv_heads}) cannot exceed n_heads ({self.n_heads})"
            )
        if self.n_layers <= 0:
            raise ValueError(f"n_layers must be positive, got {self.n_layers}")
        if self.context_length <= 0:
            raise ValueError(f"context_length must be positive, got {self.context_length}")
        if self.d_ff is not None and self.d_ff <= 0:
            raise ValueError(f"d_ff must be positive, got {self.d_ff}")
        if not (0.0 <= self.dropout <= 1.0):
            raise ValueError(f"dropout must be in [0,1], got {self.dropout}")

    @property
    def d_head(self) -> int:
        return self.d_model // self.n_heads

    @property
    def max_seq_len(self) -> int:
        """Alias used by existing model constructors."""
        return self.context_length

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelConfig":
        known = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in d.items() if k in known}
        if "max_seq_len" in d and "context_length" not in filtered:
            filtered["context_length"] = d["max_seq_len"]
        return cls(**filtered)

    def estimate_parameters(self) -> int:
        """Parameter count aligned with TinyLM.param_count logic."""
        V, D, L = self.vocab_size, self.d_model, self.n_layers
        H, KVH, dh = self.n_heads, self.n_kv_heads, self.d_head
        d_ff = self.d_ff or int(D * self.ffn_multiplier)

        emb = V * D
        attn = D * (H * dh) + D * (KVH * dh) + D * (KVH * dh) + (H * dh) * D
        mlp = D * d_ff + D * d_ff + d_ff * D
        norms = 2 * D
        per_block = attn + mlp + norms
        final_norm = D
        total = emb + L * per_block + final_norm

        if self.use_recursive_reasoning:
            total += (3 * D * D) + (2 * D * D) + 2 * D

        return total

    def estimate_weight_memory_mb(self, bytes_per_param: int = 4) -> float:
        return self.estimate_parameters() * bytes_per_param / (1024 * 1024)

    def estimate_activation_memory_mb(
        self, batch_size: int = 1, seq_len: Optional[int] = None, bytes_per: int = 4
    ) -> float:
        S = seq_len or self.context_length
        act = batch_size * S * self.d_model
        act += batch_size * self.n_heads * S * S
        act *= self.n_layers * 2
        return act * bytes_per / (1024 * 1024)

    def estimate_optimizer_memory_mb(self, bytes_per_param: int = 4) -> float:
        """AdamW keeps 2 moment buffers ≈ 2× weights (fp32)."""
        return 2 * self.estimate_weight_memory_mb(bytes_per_param)

    def summary(self) -> Dict[str, Any]:
        return {
            "d_model": self.d_model,
            "n_layers": self.n_layers,
            "n_heads": self.n_heads,
            "n_kv_heads": self.n_kv_heads,
            "d_head": self.d_head,
            "d_ff": self.d_ff,
            "context_length": self.context_length,
            "vocab_size": self.vocab_size,
            "parameters": self.estimate_parameters(),
            "weight_memory_mb_fp32": round(self.estimate_weight_memory_mb(4), 2),
            "weight_memory_mb_fp16": round(self.estimate_weight_memory_mb(2), 2),
            "optimizer_memory_mb_fp32": round(self.estimate_optimizer_memory_mb(4), 2),
            "activation_memory_mb_b1": round(self.estimate_activation_memory_mb(1), 2),
        }


# ---------------------------------------------------------------------------
# TrainingConfig — expanded
# ---------------------------------------------------------------------------

@dataclass
class TrainingConfig:
    batch_size: int = 8
    gradient_accumulation: int = 1
    learning_rate: float = 3e-4
    weight_decay: float = 0.1
    warmup_steps: int = 100
    max_steps: int = 1000
    eval_interval: int = 100
    save_interval: int = 200
    seed: int = 0
    grad_clip: float = 1.0

    # scheduler
    lr_scheduler: str = "cosine"          # "cosine" | "linear" | "constant" | "cosine_restarts"
    min_lr_ratio: float = 0.1
    lr_restarts: int = 1

    # optimizer
    optimizer: str = "adamw"              # "adamw" | "adam" | "sgd"
    betas: Optional[List[float]] = None   # default [0.9, 0.95]
    eps: float = 1e-8
    momentum: float = 0.9                 # for SGD

    # data
    seq_len: Optional[int] = None         # defaults to model.context_length
    num_workers: int = 0
    shuffle: bool = True

    # logging / checkpointing
    log_interval: int = 10
    keep_last_n_checkpoints: int = 3
    save_optimizer_state: bool = True
    resume_from: Optional[str] = None

    # early stopping
    early_stopping_patience: Optional[int] = None
    early_stopping_min_delta: float = 0.0

    def __post_init__(self) -> None:
        if self.betas is None:
            self.betas = [0.9, 0.95]


# ---------------------------------------------------------------------------
# RuntimeConfig — expanded
# ---------------------------------------------------------------------------

@dataclass
class RuntimeConfig:
    device: str = "cpu"                   # "cpu" | "cuda" | "auto" | "mps"
    dtype: str = "float32"                # "float32" | "float16" | "bfloat16"
    threads: Optional[int] = None
    max_memory: Optional[str] = None      # advisory, e.g. "4GB"
    compile: bool = False                 # torch.compile if available
    seed: int = 0
    deterministic: bool = False


# ---------------------------------------------------------------------------
# GenerationConfig
# ---------------------------------------------------------------------------

@dataclass
class GenerationConfig:
    temperature: float = 0.8
    top_k: int = 0
    top_p: float = 0.9
    repetition_penalty: float = 1.1
    max_new_tokens: int = 128
    seed: Optional[int] = None
    stop_tokens: Optional[List[str]] = None
    do_sample: bool = True
    use_kv_cache: bool = True


# ---------------------------------------------------------------------------
# Dataset / Mix config
# ---------------------------------------------------------------------------

@dataclass
class DatasetMixConfig:
    books: float = 0.40
    code: float = 0.20
    documentation: float = 0.15
    instruction: float = 0.10
    math: float = 0.05
    filipino: float = 0.05
    tool_use: float = 0.05

    def normalize(self) -> "DatasetMixConfig":
        total = sum(asdict(self).values())
        if total <= 0:
            raise ValueError("dataset mix weights must sum to > 0")
        for f in fields(self):
            setattr(self, f.name, getattr(self, f.name) / total)
        return self


# ---------------------------------------------------------------------------
# Top-level OrbitConfig
# ---------------------------------------------------------------------------

@dataclass
class OrbitConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    dataset_mix: DatasetMixConfig = field(default_factory=DatasetMixConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)

    @property
    def d_model(self) -> int:
        return self.model.d_model

    @property
    def n_layers(self) -> int:
        return self.model.n_layers

    @property
    def vocab_size(self) -> int:
        return self.model.vocab_size

    @property
    def context_length(self) -> int:
        return self.model.context_length

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model.to_dict(),
            "training": asdict(self.training),
            "runtime": asdict(self.runtime),
            "dataset_mix": asdict(self.dataset_mix),
            "generation": asdict(self.generation),
        }

    def save_yaml(self, path: Union[str, Path]) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = self.to_dict()
        if yaml is None:
            path.write_text(_yaml_lite_dump(payload), encoding="utf-8")
            return
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(payload, f, sort_keys=False, default_flow_style=False)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OrbitConfig":
        def _filter(section: str, dc):
            known = {f.name for f in fields(dc)}
            raw = d.get(section, {}) or {}
            return {k: v for k, v in raw.items() if k in known}

        return cls(
            model=ModelConfig.from_dict(d.get("model", {})),
            training=TrainingConfig(**_filter("training", TrainingConfig)),
            runtime=RuntimeConfig(**_filter("runtime", RuntimeConfig)),
            dataset_mix=DatasetMixConfig(**_filter("dataset_mix", DatasetMixConfig)),
            generation=GenerationConfig(**_filter("generation", GenerationConfig)),
        )

    @classmethod
    def load(cls, path: Union[str, Path]) -> "OrbitConfig":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if yaml is None:
            data = _yaml_lite_load(text) or {}
        else:
            data = yaml.safe_load(text) or {}
        return cls.from_dict(data)

    @classmethod
    def load_or_default(cls, name: str = "tiny") -> "OrbitConfig":
        candidates = [
            Path("configs") / f"{name}.yaml",
            Path(__file__).resolve().parent.parent / "configs" / f"{name}.yaml",
        ]
        for p in candidates:
            if p.exists():
                return cls.load(p)
        return _builtin_preset(name)


def _builtin_preset(name: str) -> OrbitConfig:
    """Fallback presets when YAML is missing."""
    presets = {
        "development": dict(d_model=64, n_layers=2, n_heads=4, n_kv_heads=2,
                            context_length=64, vocab_size=1000),
        "tiny": dict(d_model=128, n_layers=4, n_heads=8, n_kv_heads=4,
                     context_length=128, vocab_size=1500),
        "small": dict(d_model=256, n_layers=6, n_heads=8, n_kv_heads=4,
                      context_length=256, vocab_size=3000),
        "medium": dict(d_model=384, n_layers=8, n_heads=8, n_kv_heads=4,
                       context_length=512, vocab_size=5000),
        "large": dict(d_model=512, n_layers=12, n_heads=8, n_kv_heads=4,
                      context_length=1024, vocab_size=8000),
        "xlarge": dict(d_model=768, n_layers=16, n_heads=12, n_kv_heads=4,
                       context_length=2048, vocab_size=16000),
        "xxlarge": dict(d_model=1024, n_layers=24, n_heads=16, n_kv_heads=8,
                        context_length=2048, vocab_size=32000),
    }
    if name not in presets:
        return OrbitConfig()
    return OrbitConfig(model=ModelConfig(**presets[name]))


def get_preset(name: str) -> OrbitConfig:
    """Return a named preset (development/tiny/small/medium/large/xlarge/xxlarge)."""
    return OrbitConfig.load_or_default(name)


# Backwards-compatible alias
Config = OrbitConfig

# Public list of known preset names
PRESET_NAMES = [
    "development", "tiny", "small", "medium", "large", "xlarge", "xxlarge",
]
