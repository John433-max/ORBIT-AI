"""CI unit tests for memory_store (hash-embed + in-memory + SQLite)."""
import time

import numpy as np
import pytest

from memory_store import SQLiteVectorStore, VectorStore, hash_embed


@pytest.fixture(params=["memory", "sqlite"])
def store(request, tmp_path):
    if request.param == "memory":
        yield VectorStore()
        return
    db_path = str(tmp_path / "test.db")
    s = SQLiteVectorStore(db_path)
    yield s
    s.close()


def test_add_and_query(store):
    store.add("the user likes hiking on weekends")
    store.add("the weather today is sunny")
    hits = store.query("hiking", k=1)
    assert len(hits) == 1
    assert "hiking" in hits[0]["text"]


def test_delete(store):
    item_id = store.add("temporary fact")
    assert store.delete(item_id) is True
    assert store.delete(item_id) is False
    assert store.query("temporary", k=5) == []


def test_ttl_expiry(store):
    store.add("short-lived note", ttl_seconds=0.15, dedupe=False)
    assert len(store.query("short-lived", k=5)) == 1
    time.sleep(0.25)
    assert len(store.query("short-lived", k=5)) == 0


def test_duplicate_detection_reuses_id(store):
    id1 = store.add("the user's favorite color is blue")
    id2 = store.add("the user's favorite color is blue")
    assert id1 == id2
    assert len(store.list()) == 1


def test_hash_embed_is_deterministic_and_normalized():
    v1 = hash_embed("hello world")
    v2 = hash_embed("hello world")
    assert (v1 == v2).all()
    assert abs(np.linalg.norm(v1) - 1.0) < 1e-9


def test_sqlite_persists_across_reconnect(tmp_path):
    db_path = str(tmp_path / "persist.db")
    s1 = SQLiteVectorStore(db_path)
    s1.add("persisted fact", importance=0.8, dedupe=False)
    s1.close()
    s2 = SQLiteVectorStore(db_path)
    items = s2.list()
    assert len(items) == 1
    assert items[0]["text"] == "persisted fact"
    assert items[0]["importance"] == 0.8
    s2.close()
