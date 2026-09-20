"""Persona retrieval + optional generation for MainChatAgent (Cycles 62–63).

Retrieval-first chat is the documented quality path for the toy model.
Generation is opt-in and still quality-gated in MainChatAgent — the tool
only meters the raw decode so Orchestrator.metrics()["tools"] sees both
the hit path (`chat.retrieve`) and the miss path (`chat.generate`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


from tools.base import BaseTool, ToolResult


def query_persona(store, query: str, top_k: int = 3, threshold: float = 0.42):
    """Search a VectorStore of persona Q/A rows.

    Returns a dict with hits, best match, and whether it clears `threshold`.
    """
    query = (query or "").strip()
    k = max(1, int(top_k or 3))
    if store is None or not query or not hasattr(store, "query"):
        return {
            "ok": True,
            "matched": False,
            "score": 0.0,
            "answer": None,
            "hits": [],
            "query": query,
        }
    raw_hits = store.query(query, k=k) or []
    hits = []
    for h in raw_hits:
        meta = h.get("metadata") or {}
        hits.append(
            {
                "score": float(h.get("score") or 0.0),
                "text": h.get("text") or "",
                "answer": meta.get("answer"),
            }
        )
    best = hits[0] if hits else None
    score = float(best["score"]) if best else 0.0
    matched = bool(best and best.get("answer") and score >= float(threshold))
    return {
        "ok": True,
        "matched": matched,
        "score": score,
        "answer": best.get("answer") if matched else None,
        "hits": hits,
        "query": query,
        "threshold": float(threshold),
    }


class ChatRetrieveTool(BaseTool):
    name = "chat.retrieve"
    description = "Retrieve a persona-KB answer for a user chat turn."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "User message to match"},
            "top_k": {"type": "integer", "default": 3},
            "threshold": {"type": "number", "default": 0.42},
        },
        "required": ["query"],
    }
    timeout_s = 5.0

    def __init__(self, store=None):
        self.store = store

    def execute(
        self,
        query: str = "",
        top_k: int = 3,
        threshold: float = 0.42,
        **_,
    ) -> ToolResult:
        query = (query or "").strip()
        if not query:
            return ToolResult(ok=False, content="", error="query is required")
        data = query_persona(self.store, query, top_k=top_k, threshold=threshold)
        if data.get("matched"):
            content = data["answer"] or ""
        elif data.get("hits"):
            content = f"No persona match above threshold (best={data['score']:.3f})."
        else:
            content = "Persona knowledge base is empty or unmatched."
        return ToolResult(ok=True, content=content, data=data)


PERSONA_PREAMBLE = (
    "You are ORBIT — a sharp, helpful AI that runs locally. Speak in the first person as yourself. Be clear, concise, and a little dry; prefer substance over filler. Use tools for math, science, memory, documents, and code. Never invent capabilities you lack. If unsure, say so and suggest a better angle.\n"
)


def _byte_ids(text: str, vocab_size: int) -> list:
    """Map UTF-8 bytes into (1 .. vocab-2); 0 reserved, vocab-1 = EOS."""
    vs = max(8, int(vocab_size or 128))
    lo, hi = 1, vs - 2
    span = hi - lo + 1
    out = []
    for b in (text or "").encode("utf-8", errors="replace"):
        out.append(lo + (int(b) % span))
    return out or [lo]


def _ids_to_text(ids, vocab_size: int) -> str:
    vs = max(8, int(vocab_size or 128))
    lo, hi = 1, vs - 2
    span = hi - lo + 1
    raw = bytes(int((int(i) - lo) % 256) % 256 for i in ids if lo <= int(i) <= hi)
    # Byte-mod vocab is lossy; surface printable latin-1 for the lab path.
    return raw.decode("latin-1", errors="replace")


def _load_chat_bpe(path: str):
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from bpe_tokenizer import BPETokenizer

    return BPETokenizer.load(path)


def _resolve_chat_tokenizer(model):
    """Cycle 70: use sidecar BPE when the ckpt was trained with tokenizer=bpe."""
    meta = getattr(model, "_ckpt_meta", None) or {}
    if str(meta.get("tokenizer") or "").lower() != "bpe":
        return None
    path = meta.get("tokenizer_path")
    if not path:
        ckpt = getattr(model, "_ckpt_path", None)
        if ckpt:
            path = str(Path(ckpt).with_suffix(".bpe.json"))
    if not path or not Path(path).exists():
        return None
    try:
        return _load_chat_bpe(path)
    except Exception:
        return None


def _persona_ckpt_candidates(
    prefer_bpe: bool = False,
    prefer_int4: bool = False,
    prefer_int4_emb: bool = False,
    prefer_l4: bool = False,
    prefer_n4m: bool = False,
):
    """Cycle 72–79: byte default; BPE / L4 / INT4 / n4m packs are opt-in."""
    root = Path(__file__).resolve().parent.parent
    bpe_l4 = [
        "checkpoints/tinylm_persona_bpe_l4.npz",
        str(root / "checkpoints" / "tinylm_persona_bpe_l4.npz"),
    ]
    bpe_l4_int4emb = [
        "checkpoints/tinylm_persona_bpe_l4_int4emb.npz",
        str(root / "checkpoints" / "tinylm_persona_bpe_l4_int4emb.npz"),
    ]
    bpe_l4_int4 = [
        "checkpoints/tinylm_persona_bpe_l4_int4.npz",
        str(root / "checkpoints" / "tinylm_persona_bpe_l4_int4.npz"),
    ]
    bpe_l4_n4m = [
        "checkpoints/tinylm_persona_bpe_l4_int4emb.n4m",
        str(root / "checkpoints" / "tinylm_persona_bpe_l4_int4emb.n4m"),
    ]
    bpe_int4emb = [
        "checkpoints/tinylm_persona_bpe_int4emb.npz",
        str(root / "checkpoints" / "tinylm_persona_bpe_int4emb.npz"),
    ]
    bpe_int4 = [
        "checkpoints/tinylm_persona_bpe_int4.npz",
        str(root / "checkpoints" / "tinylm_persona_bpe_int4.npz"),
    ]
    bpe = [
        "checkpoints/tinylm_persona_bpe.npz",
        str(root / "checkpoints" / "tinylm_persona_bpe.npz"),
    ]
    byte = [
        "checkpoints/tinylm_persona.npz",
        str(root / "checkpoints" / "tinylm_persona.npz"),
    ]
    packed_small = (bpe_int4emb + bpe_int4) if prefer_int4_emb else (bpe_int4 + bpe_int4emb)
    packed_l4 = (bpe_l4_int4emb + bpe_l4_int4) if prefer_int4_emb else (bpe_l4_int4 + bpe_l4_int4emb)
    if prefer_n4m:
        packed_l4 = bpe_l4_n4m + packed_l4
        packed_small = bpe_l4_n4m + packed_small
    packed = packed_l4 + packed_small if prefer_l4 else packed_small
    if prefer_n4m and not (prefer_int4_emb or prefer_int4):
        n4m_head = bpe_l4_n4m if prefer_l4 else bpe_l4_n4m
        if prefer_l4 and prefer_bpe:
            return n4m_head + bpe_l4 + bpe + byte
        if prefer_l4:
            return n4m_head + bpe_l4 + byte + bpe
        if prefer_bpe:
            return n4m_head + bpe + byte
        return n4m_head + byte + bpe
    if prefer_int4_emb or prefer_int4:
        if prefer_bpe:
            return packed + (bpe_l4 if prefer_l4 else []) + bpe + byte
        return packed + byte + bpe
    if prefer_l4 and prefer_bpe:
        return bpe_l4 + bpe + byte
    if prefer_l4:
        return bpe_l4 + byte + bpe
    if prefer_bpe:
        return bpe + byte
    return byte + bpe


def _prefer_l4_ckpt() -> bool:
    import os

    flag = (os.environ.get("ORBIT_TINYLM_L4") or "").strip().lower()
    size = (os.environ.get("ORBIT_TINYLM_SIZE") or "").strip().lower()
    return flag in ("1", "true", "yes") or size in ("l4", "l4d64", "medium")


def _prefer_bpe_ckpt() -> bool:
    import os

    flag = (os.environ.get("ORBIT_TINYLM_PREFER_BPE") or "").strip().lower()
    tok = (os.environ.get("ORBIT_TINYLM_TOKENIZER") or "").strip().lower()
    return flag in ("1", "true", "yes") or tok == "bpe"


def _prefer_int4_ckpt() -> bool:
    import os

    flag = (os.environ.get("ORBIT_TINYLM_INT4") or "").strip().lower()
    emb = (os.environ.get("ORBIT_TINYLM_INT4_EMB") or "").strip().lower()
    return flag in ("1", "true", "yes") or emb in ("1", "true", "yes")


def _prefer_int4_emb_ckpt() -> bool:
    import os

    flag = (os.environ.get("ORBIT_TINYLM_INT4_EMB") or "").strip().lower()
    return flag in ("1", "true", "yes")


def _prefer_n4m_ckpt() -> bool:
    import os

    flag = (os.environ.get("ORBIT_TINYLM_N4M") or "").strip().lower()
    fmt = (os.environ.get("ORBIT_TINYLM_FORMAT") or "").strip().lower()
    return flag in ("1", "true", "yes") or fmt in ("n4m", "mmap", "orbit.n4m")


def _extend_context_enabled(explicit=None) -> bool:
    """Cycle 83: opt-in YaRN/NTK decode past trained block_size."""
    import os

    if explicit is not None:
        return bool(explicit)
    flag = (os.environ.get("ORBIT_TINYLM_EXTEND") or os.environ.get("ORBIT_TINYLM_YARN") or "").strip().lower()
    return flag in ("1", "true", "yes", "yarn", "ntk")


def apply_rope_context_extension(cfg, prompt_len: int, want: int, max_factor: float = 4.0):
    """Raise RoPE factor so prompt+new tokens fit; return (keep, n_new, factor).

    Learned-pos models stay clamped at block_size. RoPE models may grow
    max_seq_len() to block_size * factor (capped at max_factor).
    """
    import math

    block = int(getattr(cfg, "block_size", 64) or 64)
    want = max(1, int(want or 1))
    prompt_len = max(1, int(prompt_len))
    use_rope = bool(getattr(cfg, "use_rope", False))
    if not use_rope:
        keep = max(1, min(prompt_len, block - 1))
        n_new = max(1, min(want, block - keep))
        return keep, n_new, 1.0
    target = prompt_len + want
    cap = max(block, int(block * float(max_factor)))
    target = min(target, cap)
    factor = max(1.0, float(math.ceil(target / float(block))))
    factor = min(factor, float(max_factor))
    if factor > float(getattr(cfg, "rope_factor", 1.0) or 1.0):
        cfg.rope_factor = factor
        scaling = (getattr(cfg, "rope_scaling", None) or "none").lower()
        if scaling in ("none", "", "off"):
            cfg.rope_scaling = "yarn"
    limit = int(cfg.max_seq_len())
    keep = max(1, min(prompt_len, limit - 1))
    n_new = max(1, min(want, limit - keep))
    return keep, n_new, float(getattr(cfg, "rope_factor", 1.0) or 1.0)


def build_chat_tinylm(preset: str = "rope", ckpt_path: str = None):
    """Cycle 65/67: construct TinyLM; load a trained NumPy ckpt when given."""
    import os
    from tinylm import TinyLMConfig, TinyLMNumPy

    path = ckpt_path or os.environ.get("ORBIT_TINYLM_CKPT") or ""
    if not path:
        # Cycle 68/72: default educational persona checkpoint when present
        for cand in _persona_ckpt_candidates(
            prefer_bpe=_prefer_bpe_ckpt(),
            prefer_int4=_prefer_int4_ckpt(),
            prefer_int4_emb=_prefer_int4_emb_ckpt(),
            prefer_l4=_prefer_l4_ckpt(),
            prefer_n4m=_prefer_n4m_ckpt(),
        ):
            if Path(cand).exists():
                path = cand
                break
    if path:
        from tinylm import load_numpy_checkpoint

        model, meta = load_numpy_checkpoint(path, seed=0)
        model._weights_source = "checkpoint"
        model._ckpt_path = path
        model._ckpt_meta = meta
        return model
    cfg = TinyLMConfig.preset(
        preset or "rope",
        vocab_size=128,
        n_layer=4,
        n_embd=64,
        n_head=4,
        block_size=64,
    )
    model = TinyLMNumPy.from_config(cfg, seed=0)
    model._weights_source = "random"
    model._ckpt_path = None
    return model


def _float_env(name: str, default: float, explicit=None) -> float:
    if explicit is not None:
        try:
            return float(explicit)
        except (TypeError, ValueError):
            explicit = None
    import os

    raw = (os.environ.get(name) or "").strip()
    if raw == "":
        return float(default)
    flag = raw.lower()
    if flag in ("off", "false", "no"):
        return 0.0
    try:
        return float(raw)
    except ValueError:
        return float(default)


def _presence_penalty(explicit=None) -> float:
    """Cycle 88: OpenAI presence penalty. Default 0. ORBIT_TINYLM_PRESENCE."""
    return _float_env("ORBIT_TINYLM_PRESENCE", 0.0, explicit)


def _typical_p(explicit=None) -> float:
    """Cycle 89: Meister typical decoding mass. Default 1.0 (off).

    ORBIT_TINYLM_TYPICAL_P=0.95 enables locally-typical filtering.
    Values <=0 or >=1 disable (HF convention).
    """
    return _float_env("ORBIT_TINYLM_TYPICAL_P", 1.0, explicit)


def _dry_multiplier(explicit=None) -> float:
    """Cycle 90: llama.cpp DRY multiplier. Chat default 0.8.

    ORBIT_TINYLM_DRY=0 disables. llama.cpp recommended live value is 0.8.
    """
    return _float_env("ORBIT_TINYLM_DRY", 0.8, explicit)


def _dry_base(explicit=None) -> float:
    return _float_env("ORBIT_TINYLM_DRY_BASE", 1.75, explicit)


def _mirostat(explicit=None) -> int:
    """Cycle 91: llama.cpp Mirostat mode. 0 off, 2 = Mirostat 2.0.

    Chat default 0. ORBIT_TINYLM_MIROSTAT=2 enables.
    """
    if explicit is not None:
        try:
            m = int(explicit)
            return 2 if m == 2 else 0
        except (TypeError, ValueError):
            return 0
    import os

    raw = (os.environ.get("ORBIT_TINYLM_MIROSTAT") or "").strip().lower()
    if raw in ("2", "v2", "mirostat2", "on", "true", "yes"):
        return 2
    return 0


def _mirostat_tau(explicit=None) -> float:
    return _float_env("ORBIT_TINYLM_MIROSTAT_TAU", 5.0, explicit)


def _mirostat_eta(explicit=None) -> float:
    return _float_env("ORBIT_TINYLM_MIROSTAT_ETA", 0.1, explicit)


def _xtc_probability(explicit=None) -> float:
    """Cycle 92: XTC fire probability. Chat default 0. ORBIT_TINYLM_XTC."""
    return _float_env("ORBIT_TINYLM_XTC", 0.0, explicit)


def _xtc_threshold(explicit=None) -> float:
    return _float_env("ORBIT_TINYLM_XTC_THRESHOLD", 0.1, explicit)


def _dry_allowed_length(explicit=None) -> int:
    if explicit is not None:
        try:
            return max(0, int(explicit))
        except (TypeError, ValueError):
            return 2
    import os

    raw = (os.environ.get("ORBIT_TINYLM_DRY_ALLOWED") or "").strip()
    if raw == "":
        return 2
    try:
        return max(0, int(raw))
    except ValueError:
        return 2


def _frequency_penalty(explicit=None) -> float:
    """Cycle 88: OpenAI frequency penalty. Chat default 0.2 so repeated
    tokens lose a linear amount of logit each time they appear.
    ORBIT_TINYLM_FREQUENCY=0 disables.
    """
    return _float_env("ORBIT_TINYLM_FREQUENCY", 0.2, explicit)


def _min_p(explicit=None, temperature: float = 0.0) -> float:
    """Cycle 87: min-p nucleus relative to the mode token.

    Default 0.05 when temperature>0 so tail tokens cannot dominate a tiny
    softmax. Greedy (temp<=0) stays 0. ORBIT_TINYLM_MIN_P overrides.
    """
    if explicit is not None:
        try:
            return max(0.0, float(explicit))
        except (TypeError, ValueError):
            explicit = None
    import os

    raw = (os.environ.get("ORBIT_TINYLM_MIN_P") or "").strip()
    if raw != "":
        try:
            return max(0.0, float(raw))
        except ValueError:
            flag = raw.lower()
            if flag in ("0", "off", "false", "no"):
                return 0.0
    if temperature and float(temperature) > 0:
        return 0.05
    return 0.0


def _no_repeat_ngram_size(explicit=None) -> int:
    """Cycle 86: HF-style no_repeat_ngram on the chat path.

    Default 3 so tiny models cannot loop 'the the the' / bigram cycles.
    Set ORBIT_TINYLM_NO_REPEAT_NGRAM=0 to disable.
    """
    if explicit is not None:
        try:
            return max(0, int(explicit))
        except (TypeError, ValueError):
            return 3
    import os

    raw = (os.environ.get("ORBIT_TINYLM_NO_REPEAT_NGRAM") or "").strip()
    if raw == "":
        return 3
    try:
        return max(0, int(raw))
    except ValueError:
        flag = raw.lower()
        if flag in ("0", "off", "false", "no"):
            return 0
        return 3


def _min_new_tokens(explicit=None) -> int:
    """Cycle 85: suppress immediate EOS on the first generated token.

    Default 1 so empty first-token EOS replies are avoided. Set
    ORBIT_TINYLM_MIN_NEW=0 to restore Cycle 69 halt-on-first-EOS.
    """
    if explicit is not None:
        try:
            return max(0, int(explicit))
        except (TypeError, ValueError):
            return 1
    import os

    raw = (os.environ.get("ORBIT_TINYLM_MIN_NEW") or "").strip()
    if raw == "":
        return 1
    try:
        return max(0, int(raw))
    except ValueError:
        flag = raw.lower()
        if flag in ("0", "off", "false", "no"):
            return 0
        return 1


def _stop_on_newline_enabled(explicit=None) -> bool:
    """Cycle 84: single newline is no longer a default stop token.

    Opt-in via `stop_on_newline=True` or ORBIT_TINYLM_STOP_NEWLINE=1.
    """
    if explicit is not None:
        return bool(explicit)
    import os

    flag = (os.environ.get("ORBIT_TINYLM_STOP_NEWLINE") or "").strip().lower()
    return flag in ("1", "true", "yes", "on")


def trim_chat_completion(text: str, stop_on_newline: bool = False) -> str:
    """Drop a new user/assistant turn and optional first-line-only halt."""
    raw = text or ""
    lower = raw.lower()
    cut = len(raw)
    for marker in ("\nuser:", "\nassistant:", "\n\n"):
        i = lower.find(marker)
        if i >= 0:
            cut = min(cut, i)
    raw = raw[:cut]
    if stop_on_newline:
        raw = raw.split("\n")[0]
    return raw.strip()


def generate_chat_tinylm(
    request: str,
    history=None,
    max_tokens: int = 24,
    temperature: float = 0.0,
    preamble: str = PERSONA_PREAMBLE,
    preset: str = "rope",
    use_cache: bool = True,
    model=None,
    ckpt_path: str = None,
    extend_context=None,
    stop_on_newline=None,
    min_new_tokens=None,
    no_repeat_ngram_size=None,
    min_p=None,
    presence_penalty=None,
    frequency_penalty=None,
    typical_p=None,
    dry_multiplier=None,
    dry_base=None,
    dry_allowed_length=None,
    mirostat=None,
    mirostat_tau=None,
    mirostat_eta=None,
    xtc_probability=None,
    xtc_threshold=None,
) -> dict:
    """Cycle 64/65: TinyLM cached decode for chat.generate.

    Educational model + byte-id prompt. Quality is still gated by MainChatAgent.
    Pass `model` to reuse a lazy-bound instance (Cycle 65).
    """
    import time

    request = (request or "").strip()
    if not request:
        return {"ok": False, "text": "", "error": "request is required", "n_new": 0}
    try:
        import numpy as np
        from tinylm.generate import generate_numpy
    except Exception as e:
        return {"ok": False, "text": "", "error": str(e), "n_new": 0, "backend": "tinylm"}

    history_lines = ""
    if history:
        history_lines = "".join(
            f"{h.get('role', 'user')}: {h.get('content', '')}\n" for h in history
        )
    prompt = preamble + history_lines + f"user: {request}\nassistant:"

    reused = model is not None
    if model is None:
        try:
            model = build_chat_tinylm(preset, ckpt_path=ckpt_path)
        except Exception as e:
            return {"ok": False, "text": "", "error": str(e), "n_new": 0, "backend": "tinylm"}
    cfg = getattr(model, "cfg", None) or getattr(model, "config", None)

    vocab = int(getattr(cfg, "vocab_size", 128) or 128)
    tok = _resolve_chat_tokenizer(model)
    halt_newline = _stop_on_newline_enabled(stop_on_newline)
    min_new = _min_new_tokens(min_new_tokens)
    ngram_n = _no_repeat_ngram_size(no_repeat_ngram_size)
    minp = _min_p(min_p, temperature=float(temperature or 0.0))
    pres = _presence_penalty(presence_penalty)
    freq = _frequency_penalty(frequency_penalty)
    typ = _typical_p(typical_p)
    dry_m = _dry_multiplier(dry_multiplier)
    dry_b = _dry_base(dry_base)
    dry_allow = _dry_allowed_length(dry_allowed_length)
    m_mode = _mirostat(mirostat)
    m_tau = _mirostat_tau(mirostat_tau)
    m_eta = _mirostat_eta(mirostat_eta)
    xtc_p = _xtc_probability(xtc_probability)
    xtc_t = _xtc_threshold(xtc_threshold)
    if tok is not None:
        ids = tok.encode(prompt, add_bos=False, add_eos=False) or [tok.PAD]
        eos_id = int(tok.EOS)
        if halt_newline:
            nl_ids = tok.encode("\n", add_bos=False, add_eos=False) or []
            stop_ids = tuple(int(x) for x in nl_ids)
        else:
            stop_ids = ()
    else:
        ids = _byte_ids(prompt, vocab)
        eos_id = vocab - 1
        if halt_newline:
            lo, hi = 1, vocab - 2
            span = max(1, hi - lo + 1)
            stop_ids = (lo + (10 % span),)
        else:
            stop_ids = ()
    block = int(getattr(cfg, "block_size", 64) or 64)
    want = max(1, int(max_tokens or 24))
    if _extend_context_enabled(extend_context) and cfg is not None:
        keep, n_new, _factor = apply_rope_context_extension(cfg, len(ids), want)
    else:
        keep = max(1, min(len(ids), block - 1))
        n_new = max(1, min(want, block - len(ids[-keep:])))
    ids = ids[-keep:]
    idx = np.array(ids, dtype=np.int64)[None, :]
    t0 = time.perf_counter()
    out = generate_numpy(
        model,
        idx,
        n_new=n_new,
        use_cache=bool(use_cache),
        prealloc=True,
        temperature=float(temperature or 0.0),
        top_p=0.9 if (temperature and temperature > 0) else 1.0,
        repetition_penalty=1.3,
        seed=0,
        eos_id=eos_id,
        stop_ids=stop_ids,
        min_new_tokens=min_new,
        no_repeat_ngram_size=ngram_n,
        min_p=minp,
        presence_penalty=pres,
        frequency_penalty=freq,
        typical_p=typ,
        dry_multiplier=dry_m,
        dry_base=dry_b,
        dry_allowed_length=dry_allow,
        mirostat=m_mode,
        mirostat_tau=m_tau,
        mirostat_eta=m_eta,
        xtc_probability=xtc_p,
        xtc_threshold=xtc_t,
    )
    elapsed = max(time.perf_counter() - t0, 1e-9)
    new_ids = out[0, idx.shape[1] :].tolist()
    halt = {int(eos_id), *[int(s) for s in stop_ids]}
    while new_ids and int(new_ids[-1]) in halt:
        new_ids.pop()
    if tok is not None:
        decoded = tok.decode(new_ids)
        text = trim_chat_completion(decoded, stop_on_newline=halt_newline) or "(tinylm decode)"
        tok_name = "bpe"
        byte_len = len(prompt.encode("utf-8"))
        tok_len = max(1, len(ids))
        compression = byte_len / tok_len
    else:
        decoded = _ids_to_text(new_ids, vocab)
        text = trim_chat_completion(decoded, stop_on_newline=halt_newline) or "(tinylm decode)"
        tok_name = "byte"
        compression = 1.0
    return {
        "ok": True,
        "text": text,
        "error": None,
        "n_new": len(new_ids),
        "loaded": True,
        "backend": "tinylm",
        "use_cache": bool(use_cache),
        "tok_s": len(new_ids) / elapsed,
        "elapsed_s": elapsed,
        "preset": preset or "rope",
        "reused": bool(reused),
        "weights": getattr(model, "_weights_source", "random"),
        "ckpt": getattr(model, "_ckpt_path", None),
        "tokenizer": tok_name,
        "prompt_compression": compression,
        "prompt_tokens": keep,
        "block_size": block,
        "rope_factor": float(getattr(cfg, "rope_factor", 1.0) or 1.0) if cfg is not None else 1.0,
        "extended": bool(_extend_context_enabled(extend_context) and cfg is not None and getattr(cfg, "use_rope", False) and keep > max(1, block - 1)),
        "stop_on_newline": bool(halt_newline),
        "min_new_tokens": int(min_new),
        "no_repeat_ngram_size": int(ngram_n),
        "min_p": float(minp),
        "presence_penalty": float(pres),
        "frequency_penalty": float(freq),
        "typical_p": float(typ),
        "dry_multiplier": float(dry_m),
        "dry_base": float(dry_b),
        "dry_allowed_length": int(dry_allow),
        "mirostat": int(m_mode),
        "mirostat_tau": float(m_tau),
        "mirostat_eta": float(m_eta),
        "xtc_probability": float(xtc_p),
        "xtc_threshold": float(xtc_t),
    }


def resolve_generate_backend(backend, model=None, tokenizer=None) -> str:
    """Cycle 66: auto uses TinyLM when the Orbit decoder is missing."""
    chosen = (backend or "auto").strip().lower()
    if chosen in ("tinylm", "tiny"):
        return "tinylm"
    if chosen in ("legacy", "orbit"):
        return "legacy"
    # auto / default
    if model is not None and tokenizer is not None:
        return "legacy"
    return "tinylm"



def generate_chat_provider(
    request: str,
    history=None,
    max_tokens: int = 40,
    temperature: float = 0.7,
    preamble: str = PERSONA_PREAMBLE,
) -> dict:
    """Phase C+: miss-path via ModelRouter (Ollama / GGUF / OpenAI / TinyLM / echo)."""
    try:
        from orbit.models.router import get_default_provider
        from orbit.models.base import GenerateRequest
        from orbit.core.config import load_config
    except Exception as e:
        return {"ok": False, "text": "", "error": str(e), "n_new": 0, "backend": "provider"}

    cfg = load_config()
    # Only take this path when explicitly configured away from pure tinylm default,
    # or when ORBIT_CHAT_PROVIDER=1 forces provider for all miss-path generation.
    import os
    force = (os.environ.get("ORBIT_CHAT_PROVIDER") or "").strip().lower() in ("1", "true", "yes", "on")
    provider_name = (cfg.model_provider or "auto").lower()
    if not force and provider_name in ("auto", "tinylm", ""):
        # Keep historical TinyLM path unless user opted into ollama/gguf/openai/echo
        return {"ok": False, "text": "", "error": "provider path not selected", "backend": "provider", "skip": True}

    messages = []
    if preamble:
        messages.append({"role": "system", "content": preamble.strip()})
    if history:
        for h in history:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
    messages.append({"role": "user", "content": request})
    prov = get_default_provider(cfg)
    res = prov.generate(
        GenerateRequest(messages=messages, max_tokens=max_tokens, temperature=temperature)
    )
    return {
        "ok": bool(res.ok),
        "text": res.text or "",
        "error": res.error,
        "n_new": int((res.usage or {}).get("n_new") or 0),
        "backend": f"provider:{res.provider}",
        "model": res.model,
        "loaded": res.ok,
    }


def generate_chat(
    model,
    tokenizer,
    request: str,
    history=None,
    max_tokens: int = 40,
    temperature: float = 0.7,
    preamble: str = PERSONA_PREAMBLE,
    backend: str = "auto",
    use_cache: bool = True,
    tinylm_preset: str = "rope",
    tinylm_model=None,
    ckpt_path: str = None,
) -> dict:
    """Run the toy decoder on a chat prompt.

    Returns a dict; never raises for a missing model — the agent hedges.
    backend:
      - auto (default): Orbit LM if bound, else TinyLM
      - legacy: Orbit decoder or the explicit unbound stub
      - tinylm: educational cached TinyLM
    """
    request = (request or "").strip()
    if not request:
        return {"ok": False, "text": "", "error": "request is required", "n_new": 0}
    backend = resolve_generate_backend(backend, model=model, tokenizer=tokenizer)
    # ModelRouter path when ORBIT_CHAT_PROVIDER=1 or ORBIT_MODEL_PROVIDER is ollama/gguf/openai/echo
    _prov = generate_chat_provider(
        request, history=history, max_tokens=max_tokens,
        temperature=temperature, preamble=preamble,
    )
    if _prov.get("ok") and not _prov.get("skip"):
        return _prov
    if backend in ("tinylm", "tiny"):
        return generate_chat_tinylm(
            request,
            history=history,
            max_tokens=max_tokens,
            temperature=temperature,
            preamble=preamble,
            preset=tinylm_preset,
            use_cache=use_cache,
            model=tinylm_model,
            ckpt_path=ckpt_path,
        )
    if model is None or tokenizer is None:
        return {
            "ok": True,
            "text": "(no model loaded)",
            "error": None,
            "n_new": 0,
            "loaded": False,
            "backend": "legacy",
        }
    history_lines = ""
    if history:
        history_lines = "".join(
            f"{h.get('role', 'user')}: {h.get('content', '')}\n" for h in history
        )
    prompt = preamble + history_lines + f"user: {request}\nassistant:"
    try:
        import hashlib
        import numpy as np
        from sampling import sample_next_token
    except Exception as e:
        return {"ok": False, "text": "", "error": str(e), "n_new": 0}

    def _stable_seed(text: str) -> int:
        digest = hashlib.sha256(text.encode("utf-8", errors="replace")).digest()
        return int.from_bytes(digest[:8], "big") % (2**32)

    ids = list(tokenizer.encode(prompt, add_bos=False, add_eos=False))
    rng = np.random.default_rng(_stable_seed(request))
    max_seq = int(getattr(model, "max_seq_len", 128) or 128)
    n_new = 0
    eos = getattr(tokenizer, "EOS", None)
    for _ in range(max(1, int(max_tokens or 40))):
        x = np.array(ids[-max_seq:])[None, :]
        logits = model(x)
        data = logits.data if hasattr(logits, "data") else logits
        next_id = sample_next_token(
            data[-1],
            recent_ids=ids[-16:],
            temperature=float(temperature or 0.7),
            top_p=0.9,
            repetition_penalty=1.3,
            rng=rng,
        )
        ids.append(int(next_id))
        n_new += 1
        if eos is not None and int(next_id) == int(eos):
            break
    text = tokenizer.decode(ids)
    reply = text.split("assistant:", 1)[-1].strip()
    return {
        "ok": True,
        "text": reply,
        "error": None,
        "n_new": n_new,
        "loaded": True,
        "backend": "legacy",
    }


class ChatGenerateTool(BaseTool):
    name = "chat.generate"
    description = (
        "Run the toy MainChat decoder on a user turn. Quality is not guaranteed; "
        "the agent still applies the generation quality gate / hedge."
    )
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "request": {"type": "string", "description": "User message"},
            "max_tokens": {"type": "integer", "default": 40},
            "temperature": {"type": "number", "default": 0.7},
            "backend": {
                "type": "string",
                "description": "auto (TinyLM if Orbit LM missing), legacy, or tinylm",
                "default": "auto",
            },
        },
        "required": ["request"],
    }
    timeout_s = 30.0

    def __init__(
        self,
        model=None,
        tokenizer=None,
        max_tokens=40,
        temperature=0.7,
        backend="auto",
        tinylm_preset="rope",
        tinylm_model=None,
        ckpt_path=None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.backend = backend or "auto"
        self.tinylm_preset = tinylm_preset
        self.tinylm_model = tinylm_model
        self.ckpt_path = ckpt_path
        self._tinylm_factory = None

    def bind_tinylm(self, model=None, factory=None, preset=None, backend=None):
        """Cycle 65: attach a shared TinyLM (or factory) without rebuilding per call."""
        if preset is not None:
            self.tinylm_preset = preset
        if backend is not None:
            self.backend = backend
        if factory is not None:
            self._tinylm_factory = factory
        if model is not None:
            self.tinylm_model = model
        return self.tinylm_model

    def ensure_tinylm(self):
        if self.tinylm_model is not None:
            return self.tinylm_model
        if self._tinylm_factory is not None:
            self.tinylm_model = self._tinylm_factory()
            return self.tinylm_model
        self.tinylm_model = build_chat_tinylm(self.tinylm_preset, ckpt_path=self.ckpt_path)
        return self.tinylm_model

    def execute(
        self,
        request: str = "",
        max_tokens: int = None,
        temperature: float = None,
        history=None,
        backend: str = None,
        use_cache: bool = True,
        **_,
    ) -> ToolResult:
        request = (request or "").strip()
        if not request:
            return ToolResult(ok=False, content="", error="request is required")
        chosen = (backend if backend is not None else self.backend) or "auto"
        resolved = resolve_generate_backend(chosen, model=self.model, tokenizer=self.tokenizer)
        tinylm_model = self.tinylm_model
        if resolved in ("tinylm", "tiny"):
            try:
                tinylm_model = self.ensure_tinylm()
            except Exception:
                tinylm_model = self.tinylm_model
        data = generate_chat(
            self.model,
            self.tokenizer,
            request,
            history=history,
            max_tokens=max_tokens if max_tokens is not None else self.max_tokens,
            temperature=temperature if temperature is not None else self.temperature,
            backend=resolved,
            use_cache=use_cache,
            tinylm_preset=self.tinylm_preset,
            tinylm_model=tinylm_model,
            ckpt_path=self.ckpt_path,
        )
        if not data.get("ok"):
            return ToolResult(ok=False, content="", error=data.get("error") or "generate failed", data=data)
        return ToolResult(ok=True, content=data.get("text") or "", data=data)
