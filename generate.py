"""
Load a checkpoint and generate text.

Uses checkpoint metadata (or a named preset) instead of hard-coded
dimensions — a regression risk called out in the v2 audit.

Run:
  python3 generate.py
  python3 generate.py --prompt "hello" --preset development --max-tokens 40
  python3 generate.py --checkpoint checkpoint_large.npz --tokenizer bpe_tokenizer_large.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from bpe_tokenizer import BPETokenizer
from model import TinyLM, get_preset
from sampling import sample_next_token
import time


def _load_model_and_tokenizer(checkpoint, tokenizer_path, preset):
    candidates = []
    if checkpoint or tokenizer_path:
        candidates.append(
            (tokenizer_path or "bpe_tokenizer.json", checkpoint or "checkpoint_base.npz")
        )
    candidates.extend(
        [
            ("bpe_tokenizer_large.json", "checkpoint_large.npz"),
            ("bpe_tokenizer.json", "checkpoint_base.npz"),
        ]
    )

    last_err = None
    for tok_path, ckpt_path in candidates:
        tok_p, ckpt_p = Path(tok_path), Path(ckpt_path)
        if not tok_p.exists() or not ckpt_p.exists():
            continue
        try:
            tok = BPETokenizer.load(str(tok_p))
        except Exception as e:
            last_err = e
            continue
        meta_path = ckpt_p.with_suffix(".json")
        meta = {}
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        try:
            from train import build_model_from_checkpoint

            model, meta = build_model_from_checkpoint(str(ckpt_p))
        except Exception as e:
            last_err = e
            cfg = get_preset(preset).model
            kwargs = dict(
                vocab_size=tok.VOCAB_SIZE,
                d_model=int(meta.get("d_model", cfg.d_model)),
                n_layers=int(meta.get("n_layers", cfg.n_layers)),
                n_heads=int(meta.get("n_heads", cfg.n_heads)),
                n_kv_heads=int(meta.get("n_kv_heads", cfg.n_kv_heads)),
                max_seq_len=int(
                    meta.get("seq_len", meta.get("context_length", cfg.context_length))
                ),
                use_recursive_reasoning=bool(meta.get("use_recursive_reasoning", False)),
                seed=int(meta.get("seed", 0)),
            )
            model = TinyLM(**kwargs)
            from train import load_into

            load_into(model, str(ckpt_p))
        if model.vocab_size != tok.VOCAB_SIZE:
            last_err = ValueError(
                f"vocab mismatch: model={model.vocab_size} tok={tok.VOCAB_SIZE}"
            )
            continue
        return model, tok, str(ckpt_p), meta

    cfg = get_preset(preset)
    try:
        tok = BPETokenizer.load("bpe_tokenizer.json")
        vocab = tok.VOCAB_SIZE
    except Exception:
        from tokenizer import ByteTokenizer

        tok = ByteTokenizer()
        vocab = tok.VOCAB_SIZE
    model = TinyLM.from_config(cfg.model, vocab_size=vocab)
    print(
        f"WARNING: no checkpoint loaded ({last_err}); using untrained "
        f"preset={preset!r} ({model.param_count():,} params)"
    )
    return model, tok, None, {"preset": preset}


def main(argv=None):
    p = argparse.ArgumentParser(description="ORBIT text generation")
    p.add_argument("--prompt", default="the quick brown")
    p.add_argument("--max-tokens", type=int, default=40)
    p.add_argument("--temperature", type=float, default=0.8)
    p.add_argument("--top-p", type=float, default=0.9)
    p.add_argument("--top-k", type=int, default=0)
    p.add_argument("--repetition-penalty", type=float, default=1.3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--preset", default="development")
    p.add_argument("--checkpoint", default=None)
    p.add_argument("--tokenizer", default=None)
    args = p.parse_args(argv)

    model, tok, ckpt, meta = _load_model_and_tokenizer(
        args.checkpoint, args.tokenizer, args.preset
    )
    max_seq = getattr(model, "max_seq_len", 64)
    print(f"checkpoint: {ckpt or '(none)'}")
    print(
        f"params: {model.param_count():,}  max_seq_len: {max_seq}  vocab: {model.vocab_size}"
    )

    ids = tok.encode(args.prompt, add_bos=False, add_eos=False)
    prompt_len = len(ids)
    t0 = time.perf_counter()
    rng = np.random.default_rng(args.seed)
    eos = getattr(tok, "EOS", None)

    for _ in range(args.max_tokens):
        window = ids[-max_seq:]
        x = np.array(window)[None, :]
        logits = model(x)
        data = logits.data if hasattr(logits, "data") else logits
        row = data[-1] if data.ndim == 2 else data[0, -1]
        next_id = sample_next_token(
            row,
            recent_ids=ids[-16:],
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            repetition_penalty=args.repetition_penalty,
            rng=rng,
        )
        ids.append(int(next_id))
        if eos is not None and next_id == eos:
            break

    elapsed = time.perf_counter() - t0
    n_new = max(0, len(ids) - prompt_len)
    try:
        from monitoring.metrics import record_generation
        stats = record_generation(
            n_tokens=n_new,
            elapsed_s=elapsed,
            model_params=model.param_count(),
            checkpoint=ckpt,
            prompt_len=prompt_len,
        )
        print(f"speed: {stats['tokens_per_sec']} tok/s  ({n_new} tokens in {elapsed:.2f}s)")
    except Exception:
        print(f"speed: {n_new / elapsed:.1f} tok/s  ({n_new} tokens in {elapsed:.2f}s)" if elapsed else "")
    print("prompt:", repr(args.prompt))
    print("continuation:", repr(tok.decode(ids)))
    print()
    print(
        "NOTE: sampling quality and model capacity are separate — a small "
        "checkpoint cannot invent coherent prose it was never trained to produce."
    )


if __name__ == "__main__":
    main()
