from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class TinyLMConfig:
    vocab_size: int = 128
    n_layer: int = 4
    n_embd: int = 64
    n_head: int = 4
    n_kv_head: int = 0  # 0 => n_head (MHA); < n_head enables GQA (Cycle 22)
    block_size: int = 64
    residual_init_scale: bool = True
    qk_norm: bool = False
    use_rope: bool = False
    rope_theta: float = 10000.0
    rope_scaling: str = "none"  # none | linear | ntk | yarn
    rope_factor: float = 1.0  # context extension factor (>=1)
    attn_logit_softcap: float = 0.0  # 0 disables
    use_swiglu: bool = False  # Cycle 23: SwiGLU MLP instead of ReLU
    ffn_mult: float = 4.0  # intermediate = int(ffn_mult * n_embd); SwiGLU often ~8/3
    rms_eps: float = 1e-6
    init_std: float = 0.02
    sliding_window: int = 0  # 0 = full causal; >0 = attend only last W keys (Cycle 51)
    resid_pdrop: float = 0.0  # Cycle 32: residual dropout (train only)
    attn_pdrop: float = 0.0  # Cycle 32: attention weight dropout (torch path)

    def __post_init__(self) -> None:
        if self.n_kv_head <= 0:
            self.n_kv_head = self.n_head
        if self.n_embd % self.n_head != 0:
            raise ValueError(f"n_embd ({self.n_embd}) must be divisible by n_head ({self.n_head})")
        if self.n_head % self.n_kv_head != 0:
            raise ValueError(
                f"n_head ({self.n_head}) must be divisible by n_kv_head ({self.n_kv_head}) for GQA"
            )
        if self.n_kv_head > self.n_head:
            raise ValueError(f"n_kv_head ({self.n_kv_head}) cannot exceed n_head ({self.n_head})")
        if self.n_layer < 1 or self.vocab_size < 1 or self.block_size < 1:
            raise ValueError("n_layer, vocab_size, block_size must be positive")
        if self.sliding_window < 0:
            raise ValueError("sliding_window must be >= 0 (0 disables)")

    @property
    def head_dim(self) -> int:
        return self.n_embd // self.n_head

    @property
    def n_kv_heads(self) -> int:
        return self.n_kv_head

    def ffn_dim(self) -> int:
        return int(self.ffn_mult * self.n_embd)

    def estimate_parameters(self) -> int:
        """Rough parameter count (tied LM head, optional pos_emb, GQA, SwiGLU)."""
        d, L, V, H, KV = self.n_embd, self.n_layer, self.vocab_size, self.n_head, self.n_kv_head
        dh = d // H
        emb = V * d
        if not self.use_rope:
            emb += self.block_size * d
        q = d * (H * dh)
        k = d * (KV * dh)
        v = d * (KV * dh)
        o = (H * dh) * d
        if self.use_swiglu:
            ff = self.ffn_dim()
            mlp = d * ff * 2 + ff * d
        else:
            ff = self.ffn_dim()
            mlp = d * ff + ff * d
        qk_n = 2 * dh if self.qk_norm else 0
        layer = 2 * d + q + k + v + o + mlp + qk_n
        return emb + L * layer + d

    def residual_scale(self) -> float:
        if not self.residual_init_scale:
            return 1.0
        return 1.0 / (2 * self.n_layer) ** 0.5

    def max_seq_len(self) -> int:
        """Hard length cap. Learned pos is block_size; RoPE can extend."""
        if not self.use_rope:
            return self.block_size
        factor = max(float(self.rope_factor), 1.0)
        return max(self.block_size, int(self.block_size * factor))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "TinyLMConfig":
        fields = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**fields)

    def to_json(self, path: str) -> None:
        """Cycle 29: persist config as JSON."""
        import json
        from pathlib import Path

        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def from_json(cls, path: str) -> "TinyLMConfig":
        import json
        from pathlib import Path

        return cls.from_dict(json.loads(Path(path).read_text()))

    @classmethod
    def preset(cls, name: str = "default", **overrides) -> "TinyLMConfig":
        """Named educational presets."""
        name = name.lower()
        if name == "default":
            cfg = cls()
        elif name == "stable":
            cfg = cls(qk_norm=True, residual_init_scale=True, attn_logit_softcap=30.0)
        elif name == "rope":
            cfg = cls(qk_norm=True, residual_init_scale=True, use_rope=True, attn_logit_softcap=0.0)
        elif name == "yarn":
            cfg = cls(
                qk_norm=True,
                residual_init_scale=True,
                use_rope=True,
                rope_scaling="yarn",
                rope_factor=2.0,
                attn_logit_softcap=0.0,
            )
        elif name == "ntk":
            cfg = cls(
                qk_norm=True,
                residual_init_scale=True,
                use_rope=True,
                rope_scaling="ntk",
                rope_factor=2.0,
                attn_logit_softcap=0.0,
            )
        elif name == "gqa":
            cfg = cls(
                qk_norm=True,
                residual_init_scale=True,
                use_rope=True,
                n_kv_head=0,
                attn_logit_softcap=0.0,
            )
            cfg.n_kv_head = max(1, cfg.n_head // 2)
        elif name == "modern":
            cfg = cls(
                qk_norm=True,
                residual_init_scale=True,
                use_rope=True,
                use_swiglu=True,
                ffn_mult=8 / 3,
                attn_logit_softcap=0.0,
            )
            cfg.n_kv_head = max(1, cfg.n_head // 2)
        elif name == "swa":
            cfg = cls(
                qk_norm=True,
                residual_init_scale=True,
                use_rope=True,
                attn_logit_softcap=0.0,
                sliding_window=32,
            )
        else:
            raise ValueError(f"unknown TinyLM preset: {name!r}")
        if overrides:
            for k, v in overrides.items():
                if k not in cls.__dataclass_fields__:
                    raise TypeError(f"unknown config field {k!r}")
                setattr(cfg, k, v)
        return cfg
