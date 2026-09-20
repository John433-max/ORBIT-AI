from __future__ import annotations

from typing import Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import TinyLMConfig
from .rope import rope_inv_freq, yarn_attn_scale


def rms_norm(x: torch.Tensor, weight: torch.Tensor, eps: float) -> torch.Tensor:
    rms = torch.sqrt(x.pow(2).mean(dim=-1, keepdim=True) + eps)
    return (x / rms) * weight


def ring_store_gather(
    pk: torch.Tensor,
    pv: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    cache_pos: int,
    used: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Cycle 71: ring write + chronological gather via ≤2 contiguous slices."""
    cap = pk.size(2)
    t = k.size(2)
    s = int(cache_pos) % cap
    if t == 1:
        pk[:, :, s : s + 1].copy_(k)
        pv[:, :, s : s + 1].copy_(v)
    elif s + t <= cap:
        pk[:, :, s : s + t].copy_(k)
        pv[:, :, s : s + t].copy_(v)
    else:
        n1 = cap - s
        pk[:, :, s:].copy_(k[:, :, :n1])
        pk[:, :, : t - n1].copy_(k[:, :, n1:])
        pv[:, :, s:].copy_(v[:, :, :n1])
        pv[:, :, : t - n1].copy_(v[:, :, n1:])
    n = min(int(used), cap)
    start_slot = (int(used) - n) % cap
    if start_slot + n <= cap:
        return pk[:, :, start_slot : start_slot + n], pv[:, :, start_slot : start_slot + n]
    n1 = cap - start_slot
    k_out = torch.cat([pk[:, :, start_slot:], pk[:, :, : n - n1]], dim=2)
    v_out = torch.cat([pv[:, :, start_slot:], pv[:, :, : n - n1]], dim=2)
    return k_out, v_out


def rope_cos_sin(
    positions: torch.Tensor,
    head_dim: int,
    theta: float,
    scaling: str = "none",
    factor: float = 1.0,
    orig_ctx: int = 64,
) -> tuple[torch.Tensor, torch.Tensor]:
    inv_np = rope_inv_freq(head_dim, theta, scaling=scaling, factor=factor, orig_ctx=orig_ctx)
    inv_freq = torch.from_numpy(inv_np).to(device=positions.device, dtype=torch.float32)
    freqs = positions.to(torch.float32)[:, None] * inv_freq[None, :]
    return torch.cos(freqs), torch.sin(freqs)


def apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    x1 = x[..., 0::2]
    x2 = x[..., 1::2]
    c = cos[None, None, :, :]
    s = sin[None, None, :, :]
    return torch.stack((x1 * c - x2 * s, x1 * s + x2 * c), dim=-1).flatten(-2)


class TinyBlock(nn.Module):
    def __init__(self, c: TinyLMConfig):
        super().__init__()
        rscale = c.residual_scale()
        kv_dim = c.n_kv_head * c.head_dim
        ff = c.ffn_dim()
        self.ln1_w = nn.Parameter(torch.ones(c.n_embd))
        self.ln2_w = nn.Parameter(torch.ones(c.n_embd))
        self.wq = nn.Linear(c.n_embd, c.n_embd, bias=False)
        self.wk = nn.Linear(c.n_embd, kv_dim, bias=False)
        self.wv = nn.Linear(c.n_embd, kv_dim, bias=False)
        self.wo = nn.Linear(c.n_embd, c.n_embd, bias=False)
        if c.use_swiglu:
            # gate and up fused into w1: (2*ff, d)
            self.w1 = nn.Linear(c.n_embd, 2 * ff, bias=False)
            self.w2 = nn.Linear(ff, c.n_embd, bias=False)
        else:
            self.w1 = nn.Linear(c.n_embd, ff, bias=False)
            self.w2 = nn.Linear(ff, c.n_embd, bias=False)
        self.q_norm = nn.Parameter(torch.ones(c.head_dim))
        self.k_norm = nn.Parameter(torch.ones(c.head_dim))
        nn.init.normal_(self.wq.weight, 0, c.init_std)
        nn.init.normal_(self.wk.weight, 0, c.init_std)
        nn.init.normal_(self.wv.weight, 0, c.init_std)
        nn.init.normal_(self.wo.weight, 0, c.init_std * rscale)
        nn.init.normal_(self.w1.weight, 0, c.init_std)
        nn.init.normal_(self.w2.weight, 0, c.init_std * rscale)


class TinyLMTorch(nn.Module):
    def __init__(self, config: TinyLMConfig):
        super().__init__()
        self.config = config
        c = config
        self.tok_emb = nn.Embedding(c.vocab_size, c.n_embd)
        # Learned absolute positions only when not using RoPE (Cycle 21).
        if c.use_rope:
            self.pos_emb = None
        else:
            self.pos_emb = nn.Embedding(c.block_size, c.n_embd)
            nn.init.normal_(self.pos_emb.weight, 0, c.init_std)
        self.ln_f_w = nn.Parameter(torch.ones(c.n_embd))
        self.layers = nn.ModuleList([TinyBlock(c) for _ in range(c.n_layer)])
        nn.init.normal_(self.tok_emb.weight, 0, c.init_std)

    @classmethod
    def from_config(cls, config: TinyLMConfig) -> "TinyLMTorch":
        return cls(config)

    def load_numpy_state(self, np_model) -> None:
        with torch.no_grad():
            self.tok_emb.weight.copy_(torch.from_numpy(np_model.tok_emb))
            if self.pos_emb is not None and np_model.pos_emb.size > 0:
                self.pos_emb.weight.copy_(torch.from_numpy(np_model.pos_emb))
            self.ln_f_w.copy_(torch.from_numpy(np_model.ln_f_w))
            for tl, nl in zip(self.layers, np_model.layers):
                tl.ln1_w.copy_(torch.from_numpy(nl["ln1_w"]))
                tl.ln2_w.copy_(torch.from_numpy(nl["ln2_w"]))
                tl.wq.weight.copy_(torch.from_numpy(nl["wq"].T))
                tl.wk.weight.copy_(torch.from_numpy(nl["wk"].T))
                tl.wv.weight.copy_(torch.from_numpy(nl["wv"].T))
                tl.wo.weight.copy_(torch.from_numpy(nl["wo"].T))
                tl.w1.weight.copy_(torch.from_numpy(nl["w1"].T))
                tl.w2.weight.copy_(torch.from_numpy(nl["w2"].T))
                tl.q_norm.copy_(torch.from_numpy(nl["q_norm"]))
                tl.k_norm.copy_(torch.from_numpy(nl["k_norm"]))

    def dump_numpy_state(self) -> dict:
        """Export Torch weights in NumPy layout (Cycle 67). Linear weights are transposed."""
        sd = {
            "tok_emb": self.tok_emb.weight.detach().cpu().numpy().astype("float32"),
            "ln_f_w": self.ln_f_w.detach().cpu().numpy().astype("float32"),
        }
        if self.pos_emb is not None:
            sd["pos_emb"] = self.pos_emb.weight.detach().cpu().numpy().astype("float32")
        else:
            sd["pos_emb"] = np.zeros((0, int(self.config.n_embd)), dtype=np.float32)
        for i, tl in enumerate(self.layers):
            sd[f"layers.{i}.ln1_w"] = tl.ln1_w.detach().cpu().numpy().astype("float32")
            sd[f"layers.{i}.ln2_w"] = tl.ln2_w.detach().cpu().numpy().astype("float32")
            sd[f"layers.{i}.wq"] = tl.wq.weight.detach().cpu().numpy().T.astype("float32")
            sd[f"layers.{i}.wk"] = tl.wk.weight.detach().cpu().numpy().T.astype("float32")
            sd[f"layers.{i}.wv"] = tl.wv.weight.detach().cpu().numpy().T.astype("float32")
            sd[f"layers.{i}.wo"] = tl.wo.weight.detach().cpu().numpy().T.astype("float32")
            sd[f"layers.{i}.w1"] = tl.w1.weight.detach().cpu().numpy().T.astype("float32")
            sd[f"layers.{i}.w2"] = tl.w2.weight.detach().cpu().numpy().T.astype("float32")
            sd[f"layers.{i}.q_norm"] = tl.q_norm.detach().cpu().numpy().astype("float32")
            sd[f"layers.{i}.k_norm"] = tl.k_norm.detach().cpu().numpy().astype("float32")
        return sd

    def alloc_kv_caches(self, batch: int, max_len: int, device=None) -> list:
        """Preallocated KV. Cycle 54: cap = min(max_len, W) when SWA is on."""
        c = self.config
        device = device or next(self.parameters()).device
        cap = int(max_len)
        if c.sliding_window > 0:
            cap = min(cap, int(c.sliding_window))
        caches = []
        for _ in range(c.n_layer):
            k = torch.zeros(batch, c.n_kv_head, cap, c.head_dim, device=device)
            v = torch.zeros_like(k)
            caches.append((k, v))
        return caches

    def _attn(
        self,
        x,
        layer: TinyBlock,
        kv_cache=None,
        cache_pos: Optional[int] = None,
        positions: Optional[torch.Tensor] = None,
    ):
        c = self.config
        b, t, _ = x.shape
        h, kvh, d = c.n_head, c.n_kv_head, c.head_dim
        q = layer.wq(x).view(b, t, h, d).transpose(1, 2)
        k = layer.wk(x).view(b, t, kvh, d).transpose(1, 2)
        v = layer.wv(x).view(b, t, kvh, d).transpose(1, 2)
        if c.qk_norm:
            q = rms_norm(q, layer.q_norm, c.rms_eps)
            k = rms_norm(k, layer.k_norm, c.rms_eps)
        if c.use_rope:
            if positions is None:
                raise ValueError("positions required when use_rope=True")
            cos, sin = rope_cos_sin(
                positions,
                d,
                c.rope_theta,
                scaling=c.rope_scaling,
                factor=c.rope_factor,
                orig_ctx=c.block_size,
            )
            q = apply_rope(q, cos, sin)
            k = apply_rope(k, cos, sin)
            yscale = yarn_attn_scale(c.rope_scaling, c.rope_factor)
            if yscale != 1.0:
                q = q * yscale
        if kv_cache is not None and cache_pos is not None:
            pk, pv = kv_cache
            cap = pk.size(2)
            win = int(c.sliding_window)
            used = cache_pos + t
            if win > 0 and cap <= win:
                k, v = ring_store_gather(pk, pv, k, v, cache_pos, used)
            else:
                pk[:, :, cache_pos : cache_pos + t].copy_(k)
                pv[:, :, cache_pos : cache_pos + t].copy_(v)
                k = pk[:, :, :used]
                v = pv[:, :, :used]
            new_cache = kv_cache
        elif kv_cache is not None:
            pk, pv = kv_cache
            k = torch.cat([pk, k], dim=2)
            v = torch.cat([pv, v], dim=2)
            new_cache = (k, v)
        else:
            new_cache = (k, v)
        win_trim = int(c.sliding_window)
        if win_trim > 0 and t == 1 and k.size(2) > win_trim:
            k = k[:, :, -win_trim:]
            v = v[:, :, -win_trim:]
        # GQA: expand KV heads to match Q heads
        if kvh != h:
            rep = h // kvh
            k = k.repeat_interleave(rep, dim=1)
            v = v.repeat_interleave(rep, dim=1)
        klen = k.size(2)
        qlen = q.size(2)
        past = klen - qlen
        win = int(c.sliding_window)
        q_pos = torch.arange(qlen, device=x.device)[:, None] + past
        k_pos = torch.arange(klen, device=x.device)[None, :]
        allowed = k_pos <= q_pos
        if win > 0:
            allowed = allowed & ((q_pos - k_pos) < win)
        attn_drop = float(c.attn_pdrop) if self.training else 0.0
        use_sdpa = c.attn_logit_softcap <= 0
        if use_sdpa:
            need_explicit = win > 0 or not (qlen == 1 or past == 0)
            if not need_explicit:
                attn = F.scaled_dot_product_attention(
                    q, k, v, attn_mask=None, dropout_p=attn_drop, is_causal=(qlen > 1)
                )
            else:
                attn = F.scaled_dot_product_attention(
                    q, k, v, attn_mask=allowed, dropout_p=attn_drop, is_causal=False
                )
            out = attn.transpose(1, 2).contiguous().view(b, t, c.n_embd)
            return layer.wo(out), new_cache
        scores = (q @ k.transpose(-2, -1)) / (d ** 0.5)
        if c.attn_logit_softcap > 0:
            scores = c.attn_logit_softcap * torch.tanh(scores / c.attn_logit_softcap)
        scores = scores.masked_fill(~allowed, float("-inf"))
        w = torch.softmax(scores, dim=-1)
        if attn_drop > 0:
            w = F.dropout(w, p=attn_drop)
        out = (w @ v).transpose(1, 2).contiguous().view(b, t, c.n_embd)
        return layer.wo(out), new_cache

    def forward(
        self,
        idx: torch.Tensor,
        kv_caches: Optional[list] = None,
        cache_pos: Optional[int] = None,
    ):
        c = self.config
        t = idx.size(1)
        if cache_pos is not None:
            pos0 = cache_pos
        elif kv_caches is None:
            pos0 = 0
        else:
            pos0 = kv_caches[0][0].size(2)
        limit = c.max_seq_len()
        if pos0 + t > limit:
            raise ValueError(
                f"sequence length {pos0 + t} exceeds max_seq_len {limit} (block_size={c.block_size})"
            )
        pos = torch.arange(pos0, pos0 + t, device=idx.device)
        x = self.tok_emb(idx)
        if not c.use_rope and self.pos_emb is not None:
            x = x + self.pos_emb(pos)[None, :, :]
        new_caches = []
        for i, layer in enumerate(self.layers):
            n1 = rms_norm(x, layer.ln1_w, c.rms_eps)
            cache = None if kv_caches is None else kv_caches[i]
            attn_out, new_c = self._attn(
                n1, layer, cache, cache_pos=cache_pos, positions=pos
            )
            if self.training and c.resid_pdrop > 0:
                attn_out = F.dropout(attn_out, p=c.resid_pdrop)
            x = x + attn_out
            n2 = rms_norm(x, layer.ln2_w, c.rms_eps)
            if c.use_swiglu:
                gu = layer.w1(n2)
                ff = gu.shape[-1] // 2
                gate, up = gu[..., :ff], gu[..., ff:]
                mlp_out = layer.w2(F.silu(gate) * up)
            else:
                mlp_out = layer.w2(F.relu(layer.w1(n2)))
            if self.training and c.resid_pdrop > 0:
                mlp_out = F.dropout(mlp_out, p=c.resid_pdrop)
            x = x + mlp_out
            new_caches.append(new_c)
        x = rms_norm(x, self.ln_f_w, c.rms_eps)
        logits = F.linear(x, self.tok_emb.weight)
        return logits, new_caches
