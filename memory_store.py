"""
Minimal RAG / long-term-memory store (hashing-trick embeddings + cosine retrieval).
"""
import time
import hashlib
import json
import sqlite3
import threading
import numpy as np


def hash_embed(text: str, dim: int = 256, ngram: int = 3) -> np.ndarray:
    text = text.lower().strip()
    vec = np.zeros(dim, dtype=np.float64)
    if len(text) < ngram:
        grams = [text] if text else []
    else:
        grams = [text[i:i + ngram] for i in range(len(text) - ngram + 1)]
    for g in grams:
        h = int(hashlib.md5(g.encode("utf-8", errors="replace")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if (h // dim) % 2 == 0 else -1.0
        vec[idx] += sign
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


DUPLICATE_SIMILARITY_THRESHOLD = 0.98


def _locked(method):
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    wrapper.__name__ = method.__name__
    wrapper.__doc__ = method.__doc__
    return wrapper


class VectorStore:
    def __init__(self, dim: int = 256):
        self.dim = dim
        self._lock = threading.RLock()
        self._items = {}
        self._next_id = 1

    @_locked
    def add(self, text: str, metadata: dict = None, ttl_seconds: float = None,
            importance: float = 0.5, dedupe: bool = True) -> int:
        vec = hash_embed(text, self.dim)
        if dedupe:
            self._purge_expired()
            for item_id, item in self._items.items():
                sim = float(np.dot(vec, item["vec"]))
                if sim >= DUPLICATE_SIMILARITY_THRESHOLD:
                    item["importance"] = min(1.0, item["importance"] + 0.1)
                    return item_id
        item_id = self._next_id
        self._next_id += 1
        now = time.time()
        self._items[item_id] = {
            "text": text, "vec": vec, "metadata": metadata or {},
            "created_at": now,
            "expires_at": (now + ttl_seconds) if ttl_seconds else None,
            "importance": importance,
        }
        return item_id

    @_locked
    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None

    @_locked
    def update(self, item_id: int, text: str = None, importance: float = None,
               metadata: dict = None, ttl_seconds: float = None) -> bool:
        item = self._items.get(item_id)
        if item is None:
            return False
        if text is not None:
            item["text"] = text
            item["vec"] = hash_embed(text, self.dim)
        if importance is not None:
            item["importance"] = importance
        if metadata is not None:
            item["metadata"] = metadata
        if ttl_seconds is not None:
            item["expires_at"] = time.time() + ttl_seconds
        return True

    @_locked
    def _purge_expired(self):
        now = time.time()
        expired = [i for i, v in self._items.items() if v["expires_at"] and v["expires_at"] < now]
        for i in expired:
            del self._items[i]

    @_locked
    def query(self, text: str, k: int = 3):
        self._purge_expired()
        if not self._items:
            return []
        q = hash_embed(text, self.dim)
        scored = []
        for item_id, item in self._items.items():
            score = float(np.dot(q, item["vec"]))
            scored.append((score, item_id, item))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [
            {"id": item_id, "text": item["text"], "score": score, "metadata": item["metadata"],
             "importance": item["importance"]}
            for score, item_id, item in scored[:k]
        ]

    @_locked
    def list(self):
        self._purge_expired()
        return [{"id": i, "text": v["text"], "metadata": v["metadata"], "importance": v["importance"]}
                for i, v in self._items.items()]

    @_locked
    def export(self):
        self._purge_expired()
        return {i: {"text": v["text"], "metadata": v["metadata"], "importance": v["importance"]}
                for i, v in self._items.items()}


class SQLiteVectorStore(VectorStore):
    def __init__(self, db_path: str = "orbit_memory.db", dim: int = 256):
        super().__init__(dim=dim)
        self.db_path = db_path
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL,
                importance REAL NOT NULL DEFAULT 0.5
            )
        """)
        self._conn.commit()
        self._load_from_db()

    def _load_from_db(self):
        self._items = {}
        cur = self._conn.execute("SELECT id, text, metadata, created_at, expires_at, importance FROM memories")
        for item_id, text, metadata_json, created_at, expires_at, importance in cur.fetchall():
            self._items[item_id] = {
                "text": text,
                "vec": hash_embed(text, self.dim),
                "metadata": json.loads(metadata_json),
                "created_at": created_at,
                "expires_at": expires_at,
                "importance": importance,
            }
            self._next_id = max(self._next_id, item_id + 1)

    @_locked
    def add(self, text: str, metadata: dict = None, ttl_seconds: float = None,
            importance: float = 0.5, dedupe: bool = True) -> int:
        vec = hash_embed(text, self.dim)
        if dedupe:
            self._purge_expired()
            for item_id, item in self._items.items():
                sim = float(np.dot(vec, item["vec"]))
                if sim >= DUPLICATE_SIMILARITY_THRESHOLD:
                    item["importance"] = min(1.0, item["importance"] + 0.1)
                    self._conn.execute("UPDATE memories SET importance = ? WHERE id = ?",
                                        (item["importance"], item_id))
                    self._conn.commit()
                    return item_id
        now = time.time()
        expires_at = (now + ttl_seconds) if ttl_seconds else None
        cur = self._conn.execute(
            "INSERT INTO memories (text, metadata, created_at, expires_at, importance) VALUES (?, ?, ?, ?, ?)",
            (text, json.dumps(metadata or {}), now, expires_at, importance),
        )
        self._conn.commit()
        item_id = cur.lastrowid
        self._items[item_id] = {
            "text": text, "vec": vec, "metadata": metadata or {},
            "created_at": now, "expires_at": expires_at, "importance": importance,
        }
        self._next_id = max(self._next_id, item_id + 1)
        return item_id

    @_locked
    def delete(self, item_id: int) -> bool:
        existed = super().delete(item_id)
        if existed:
            self._conn.execute("DELETE FROM memories WHERE id = ?", (item_id,))
            self._conn.commit()
        return existed

    @_locked
    def update(self, item_id: int, text: str = None, importance: float = None,
               metadata: dict = None, ttl_seconds: float = None) -> bool:
        if item_id not in self._items:
            return False
        super().update(item_id, text=text, importance=importance, metadata=metadata,
                        ttl_seconds=ttl_seconds)
        item = self._items[item_id]
        self._conn.execute(
            "UPDATE memories SET text = ?, metadata = ?, importance = ?, expires_at = ? WHERE id = ?",
            (item["text"], json.dumps(item["metadata"]), item["importance"], item["expires_at"], item_id),
        )
        self._conn.commit()
        return True

    @_locked
    def _purge_expired(self):
        now = time.time()
        expired = [i for i, v in self._items.items() if v["expires_at"] and v["expires_at"] < now]
        for i in expired:
            del self._items[i]
            self._conn.execute("DELETE FROM memories WHERE id = ?", (i,))
        if expired:
            self._conn.commit()

    @_locked
    def close(self):
        self._conn.close()
