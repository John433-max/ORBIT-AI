"""
Unified ORBIT AI facade — one object for chat, agents, documents, and TinyLM lab.

Usage:
    from orbit_ai import OrbitAI
    ai = OrbitAI()
    print(ai.chat("what is your name"))
    print(ai.ask("calculate 12*7"))
    print(ai.status())
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional


class OrbitAI:
    """Single entry point over Orchestrator + DocumentStore + optional TinyLM lab."""

    def __init__(
        self,
        sandbox_root: str = ".",
        memory_db_path: Optional[str] = None,
        document_db_path: Optional[str] = None,
        conversation_db_path: Optional[str] = None,
        load_model: bool = True,
        persist: bool = True,
        conversation_id: str = "default",
        use_thinking: bool = True,
    ):
        self.root = Path(sandbox_root).resolve()
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.active_checkpoint = None
        self.conversation_id = conversation_id
        self.use_thinking = use_thinking

        # Cycle 53: default on-disk stores under .orbit_data/
        if persist:
            data = self.root / ".orbit_data"
            data.mkdir(parents=True, exist_ok=True)
            memory_db_path = memory_db_path or str(data / "memory.db")
            document_db_path = document_db_path or str(data / "documents.db")
            conversation_db_path = conversation_db_path or str(data / "conversations.db")

        if load_model:
            self._try_load_checkpoint()

        from agents import Orchestrator

        self.orch = Orchestrator(
            sandbox_root=str(self.root),
            chat_model=self.model,
            chat_tokenizer=self.tokenizer,
            memory_db_path=memory_db_path,
            document_db_path=document_db_path,
            conversation_db_path=conversation_db_path,
        )

    def _try_load_checkpoint(self) -> None:
        from bpe_tokenizer import BPETokenizer
        from train import build_model_from_checkpoint

        candidates = [
            ("bpe_tokenizer_large.json", "checkpoint_large.npz"),
            ("bpe_tokenizer.json", "checkpoint_base.npz"),
        ]
        for tok_path, ckpt_path in candidates:
            tok_p = self.root / tok_path
            ckpt_p = self.root / ckpt_path
            if not tok_p.exists() or not ckpt_p.exists():
                continue
            try:
                tok = BPETokenizer.load(str(tok_p))
                model, meta = build_model_from_checkpoint(str(ckpt_p))
                vs = int(meta.get("vocab_size", getattr(model, "vocab_size", 0)))
                if vs and vs != tok.VOCAB_SIZE:
                    continue
                self.tokenizer = tok
                self.model = model
                self.model_loaded = True
                self.active_checkpoint = str(ckpt_p.name)
                return
            except Exception:
                continue

    # ---- chat / agents ----
    def chat(self, message: str, history: Optional[List[dict]] = None) -> Dict[str, Any]:
        if history is None and self.orch.conversations is not None:
            try:
                history = self.orch.conversations.get_recent(self.conversation_id, limit=12)
            except Exception:
                history = None
        if self.use_thinking and hasattr(self.orch, "think"):
            result = self.orch.think(message, history=history)
        else:
            result = self.orch.handle(message, history=history)
        try:
            self.orch.conversations.add_message(self.conversation_id, "user", message)
            self.orch.conversations.add_message(
                self.conversation_id, "assistant", result.get("content", "")
            )
        except Exception:
            pass
        return result

    def ask(self, message: str, history: Optional[List[dict]] = None) -> str:
        return self.chat(message, history=history).get("content", "")

    def metrics(self) -> Dict[str, Any]:
        return self.orch.metrics() if hasattr(self.orch, "metrics") else {}

    # ---- documents / RAG ----
    def add_document(self, filename: str, raw: bytes) -> dict:
        return self.orch.documents.add_document(filename, raw)

    def list_documents(self) -> list:
        return self.orch.documents.list_documents()

    def query_documents(self, question: str) -> str:
        return self.ask(f"according to the document: {question}")

    # ---- TinyLM lab (educational stack) ----
    def lab_status(self) -> dict:
        try:
            from tinylm import TinyLMConfig
            from tinylm.regression import run_regression

            reg = run_regression()
            cfg = TinyLMConfig.preset("modern")
            return {
                "available": True,
                "modern_params": cfg.estimate_parameters(),
                "regression_ok": reg.get("ok"),
            }
        except Exception as e:
            return {"available": False, "error": str(e)}

    def lab_bench(self, preset: str = "rope", n_new: int = 24) -> dict:
        from tinylm.config import TinyLMConfig
        from tinylm.generate import bench_numpy
        from tinylm.numpy_model import TinyLMNumPy

        cfg = TinyLMConfig.preset(preset, vocab_size=64, n_layer=4, n_embd=64, n_head=4, block_size=64)
        m = TinyLMNumPy.from_config(cfg, seed=0)
        tps = bench_numpy(m, prompt_len=8, n_new=n_new, use_cache=True)
        return {"preset": preset, "numpy_tok_s": tps, "params": cfg.estimate_parameters()}

    # ---- status ----
    def status(self) -> dict:
        agents = list(self.orch.agents.keys())
        persona_ckpt = self.root / "checkpoints" / "tinylm_persona.npz"
        return {
            "product": "ORBIT unified AI",
            "model_loaded": self.model_loaded,
            "checkpoint": self.active_checkpoint,
            "vocab_size": getattr(self.tokenizer, "VOCAB_SIZE", None),
            "agents": agents,
            "tinylm_lab": self.lab_status(),
            "tinylm_persona_ckpt": persona_ckpt.exists(),
            "use_thinking": bool(getattr(self, "use_thinking", True)),
            "webui": (self.root / "webui" / "index.html").exists(),
            "api": "uvicorn api:app  OR  python run_orbit.py",
            "metrics": self.metrics(),
            "data_dir": str(self.root / ".orbit_data"),
        }


def main():
    import json
    import sys

    ai = OrbitAI()
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        print(ai.ask(msg))
    else:
        print(json.dumps(ai.status(), indent=2))


if __name__ == "__main__":
    main()
