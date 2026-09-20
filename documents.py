"""Document chat / RAG — retrieval + extractive answers (not generative)."""
import re
import csv
import io
import json
import time
import sqlite3
import threading
from collections import Counter
from enum import Enum

import numpy as np
from memory_store import hash_embed

try:
    import pypdf
    _PDF_AVAILABLE = True
except ImportError:
    _PDF_AVAILABLE = False
try:
    import docx as _docx_lib
    _DOCX_AVAILABLE = True
except ImportError:
    _DOCX_AVAILABLE = False
try:
    from pptx import Presentation as _PptxPresentation
    _PPTX_AVAILABLE = True
except ImportError:
    _PPTX_AVAILABLE = False

SUPPORTED_FORMATS = {"txt", "md", "markdown", "csv", "json"}
if _PDF_AVAILABLE:
    SUPPORTED_FORMATS.add("pdf")
if _DOCX_AVAILABLE:
    SUPPORTED_FORMATS.add("docx")
if _PPTX_AVAILABLE:
    SUPPORTED_FORMATS.add("pptx")


class Support(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


def load_txt(raw_bytes: bytes):
    text = raw_bytes.decode("utf-8", errors="replace")
    return text, [(None, text)]

def load_markdown(raw_bytes: bytes):
    return load_txt(raw_bytes)

def load_csv(raw_bytes: bytes):
    text = raw_bytes.decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return "", [(None, "")]
    header, body = rows[0], rows[1:]
    lines = [", ".join(header)] + [", ".join(row) for row in body]
    rendered = "\n".join(lines)
    return rendered, [(None, rendered)]

def load_json(raw_bytes: bytes):
    text = raw_bytes.decode("utf-8", errors="replace")
    try:
        pretty = json.dumps(json.loads(text), indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        pretty = text
    return pretty, [(None, pretty)]

def load_pdf(raw_bytes: bytes):
    if not _PDF_AVAILABLE:
        raise RuntimeError("PDF support requires pypdf")
    reader = pypdf.PdfReader(io.BytesIO(raw_bytes))
    pages, full = [], []
    for i, page in enumerate(reader.pages, start=1):
        t = page.extract_text() or ""
        pages.append((i, t))
        full.append(t)
    return "\n".join(full), pages

def load_docx(raw_bytes: bytes):
    if not _DOCX_AVAILABLE:
        raise RuntimeError("DOCX support requires python-docx")
    doc = _docx_lib.Document(io.BytesIO(raw_bytes))
    text = "\n".join(p.text for p in doc.paragraphs)
    return text, [(None, text)]

def load_pptx(raw_bytes: bytes):
    if not _PPTX_AVAILABLE:
        raise RuntimeError("PPTX support requires python-pptx")
    prs = _PptxPresentation(io.BytesIO(raw_bytes))
    pages, full = [], []
    for i, slide in enumerate(prs.slides, start=1):
        parts = [s.text for s in slide.shapes if hasattr(s, "text") and s.text]
        page_text = "\n".join(parts)
        pages.append((i, page_text))
        full.append(page_text)
    return "\n\n".join(full), pages

_LOADERS = {
    "txt": load_txt, "md": load_markdown, "markdown": load_markdown,
    "csv": load_csv, "json": load_json, "pdf": load_pdf, "docx": load_docx, "pptx": load_pptx,
}

def sanitize_filename(filename: str) -> str:
    import os
    name = os.path.basename((filename or "").replace("\\", "/").strip())
    name = "".join(ch for ch in name if ch.isprintable() and ch not in ("\x00", "/"))
    if not name or name in (".", ".."):
        raise ValueError("invalid filename")
    return name[:255]

_MAGIC_PREFIXES = {
    "pdf": (b"%PDF",), "docx": (b"PK\x03\x04",), "pptx": (b"PK\x03\x04",),
}

def _check_magic(ext, raw_bytes):
    prefixes = _MAGIC_PREFIXES.get(ext)
    if prefixes and not any(raw_bytes.startswith(p) for p in prefixes):
        raise ValueError(f"file content does not match '.{ext}'")

def load_document(filename: str, raw_bytes: bytes):
    filename = sanitize_filename(filename)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"unsupported '.{ext}'. Supported: {', '.join(sorted(SUPPORTED_FORMATS))}")
    if not isinstance(raw_bytes, (bytes, bytearray)) or len(raw_bytes) == 0:
        raise ValueError("empty or invalid document")
    if len(raw_bytes) > 10_500_000:
        raise ValueError("document exceeds 10MB")
    _check_magic(ext, raw_bytes)
    return _LOADERS[ext](raw_bytes)

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

def split_sentences(text: str) -> list:
    text = text.strip()
    return [s.strip() for s in _SENTENCE_SPLIT_RE.split(text) if s.strip()] if text else []

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list:
    sentences = split_sentences(text)
    if not sentences:
        return []
    chunks, current, current_len = [], [], 0
    for sent in sentences:
        if current_len + len(sent) > chunk_size and current:
            chunks.append(" ".join(current))
            tail, tail_len = [], 0
            for s in reversed(current):
                if tail_len + len(s) > overlap:
                    break
                tail.insert(0, s)
                tail_len += len(s)
            current, current_len = tail, tail_len
        current.append(sent)
        current_len += len(sent)
    if current:
        chunks.append(" ".join(current))
    return chunks

def chunk_pages(pages, chunk_size=500, overlap=80):
    out = []
    for page_num, page_text in pages:
        for c in chunk_text(page_text, chunk_size, overlap):
            out.append((page_num, c))
    return out

_STOPWORDS = {"the","a","an","is","are","was","were","in","on","at","of","to","and","or","for","with","this","that","it","as","by","be","from","has","have","had"}

def extractive_summarize(text: str, n_sentences: int = 3) -> list:
    sentences = split_sentences(text)
    if len(sentences) <= n_sentences:
        return sentences
    words = re.findall(r"[a-zA-Z']+", text.lower())
    freqs = Counter(w for w in words if w not in _STOPWORDS)
    if not freqs:
        return sentences[:n_sentences]
    max_freq = max(freqs.values())
    scored = []
    for i, sent in enumerate(sentences):
        score = sum(freqs.get(w, 0) / max_freq for w in re.findall(r"[a-zA-Z']+", sent.lower()))
        if i == 0:
            score *= 1.2
        scored.append((score, i, sent))
    top = sorted(scored, key=lambda t: t[0], reverse=True)[:n_sentences]
    return [s for _, _, s in sorted(top, key=lambda t: t[1])]

def query_aware_extract(text: str, query: str, n_sentences: int = 2) -> list:
    sentences = split_sentences(text)
    if not sentences:
        return []
    if len(sentences) <= n_sentences:
        return sentences
    q_words = set(re.findall(r"[a-zA-Z']+", query.lower())) - _STOPWORDS
    if not q_words:
        return extractive_summarize(text, n_sentences)
    scored = [(len(q_words & set(re.findall(r"[a-zA-Z']+", s.lower()))), i, s) for i, s in enumerate(sentences)]
    top = sorted(scored, key=lambda t: t[0], reverse=True)[:n_sentences]
    if all(score == 0 for score, _, _ in top):
        return extractive_summarize(text, n_sentences)
    return [s for _, _, s in sorted(top, key=lambda t: t[1])]

def _locked(method):
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    wrapper.__name__ = method.__name__
    return wrapper


class DocumentStore:
    def __init__(self, db_path: str = "orbit_documents.db", dim: int = 256):
        self.dim = dim
        self._lock = threading.RLock()
        self._embed_cache = {}
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("""CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL,
            filetype TEXT NOT NULL, uploaded_at REAL NOT NULL,
            num_chunks INTEGER NOT NULL, char_count INTEGER NOT NULL)""")
        self._conn.execute("""CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL, page INTEGER, section TEXT, text TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id))""")
        self._conn.commit()

    @_locked
    def add_document(self, filename: str, raw_bytes: bytes, chunk_size: int = 500, overlap: int = 80) -> dict:
        filename = sanitize_filename(filename)
        text, pages = load_document(filename, raw_bytes)
        ext = filename.rsplit(".", 1)[-1].lower()
        page_chunks = chunk_pages(pages, chunk_size, overlap)
        if not page_chunks:
            raise ValueError("document produced no extractable text")
        cur = self._conn.execute(
            "INSERT INTO documents (filename, filetype, uploaded_at, num_chunks, char_count) VALUES (?, ?, ?, ?, ?)",
            (filename, ext, time.time(), len(page_chunks), len(text)),
        )
        doc_id = cur.lastrowid
        for i, (page_num, chunk) in enumerate(page_chunks):
            self._conn.execute(
                "INSERT INTO chunks (document_id, chunk_index, page, section, text) VALUES (?, ?, ?, ?, ?)",
                (doc_id, i, page_num, None, chunk),
            )
        self._conn.commit()
        return {"document_id": doc_id, "filename": filename, "num_chunks": len(page_chunks), "char_count": len(text)}

    @_locked
    def get_document_text(self, document_id: int) -> str:
        cur = self._conn.execute("SELECT text FROM chunks WHERE document_id = ? ORDER BY chunk_index", (int(document_id),))
        return "\n".join(r[0] for r in cur.fetchall() if r and r[0])

    @_locked
    def list_documents(self) -> list:
        cur = self._conn.execute("SELECT id, filename, filetype, uploaded_at, num_chunks, char_count FROM documents ORDER BY id")
        return [{"id": r[0], "filename": r[1], "filetype": r[2], "uploaded_at": r[3], "num_chunks": r[4], "char_count": r[5]} for r in cur.fetchall()]

    @_locked
    def delete_document(self, document_id: int) -> bool:
        if self._conn.execute("SELECT id FROM documents WHERE id = ?", (document_id,)).fetchone() is None:
            return False
        chunk_ids = [r[0] for r in self._conn.execute("SELECT id FROM chunks WHERE document_id = ?", (document_id,)).fetchall()]
        self._conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
        self._conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        self._conn.commit()
        for cid in chunk_ids:
            self._embed_cache.pop(cid, None)
        return True

    @_locked
    def _all_chunks(self, document_id=None):
        if document_id is not None:
            return self._conn.execute(
                "SELECT c.id, c.document_id, d.filename, c.chunk_index, c.page, c.section, c.text "
                "FROM chunks c JOIN documents d ON c.document_id = d.id WHERE c.document_id = ?", (document_id,)
            ).fetchall()
        return self._conn.execute(
            "SELECT c.id, c.document_id, d.filename, c.chunk_index, c.page, c.section, c.text "
            "FROM chunks c JOIN documents d ON c.document_id = d.id"
        ).fetchall()

    @_locked
    def search(self, query: str, k: int = 5, document_id: int = None) -> list:
        rows = self._all_chunks(document_id)
        if not rows:
            return []
        q_vec = hash_embed(query, self.dim)
        q_words = set(re.findall(r"[a-zA-Z']+", query.lower())) - _STOPWORDS
        scored = []
        for chunk_id, doc_id, filename, chunk_idx, page, section, text in rows:
            vec = self._embed_cache.get(chunk_id)
            if vec is None:
                vec = hash_embed(text, self.dim)
                self._embed_cache[chunk_id] = vec
            cos_sim = float(np.dot(q_vec, vec))
            overlap = len(q_words & set(re.findall(r"[a-zA-Z']+", text.lower()))) / max(1, len(q_words)) if q_words else 0.0
            score = 0.7 * cos_sim + 0.3 * overlap
            scored.append((score, {"chunk_id": chunk_id, "document_id": doc_id, "filename": filename,
                "chunk_index": chunk_idx, "page": page, "section": section, "text": text, "score": score}))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [item for _, item in scored[:k]]

    @_locked
    def close(self):
        self._conn.close()


SUPPORT_THRESHOLD_FULL = 0.35
SUPPORT_THRESHOLD_PARTIAL = 0.15

def answer_from_documents(store: DocumentStore, question: str, k: int = 3, document_id: int = None) -> dict:
    hits = store.search(question, k=k, document_id=document_id)
    if not hits:
        return {"answer": "I don't have any indexed documents that relate to this question.",
                "support": Support.UNKNOWN, "sources": []}
    top_score = hits[0]["score"]
    if top_score >= SUPPORT_THRESHOLD_FULL:
        support = Support.SUPPORTED
    elif top_score >= SUPPORT_THRESHOLD_PARTIAL:
        support = Support.PARTIALLY_SUPPORTED
    else:
        support = Support.UNSUPPORTED
    if support == Support.UNSUPPORTED:
        return {"answer": "I don't have verified information about this in the indexed documents.",
                "support": support, "sources": []}
    used = hits[:2] if support == Support.SUPPORTED else hits[:1]
    extracted, sources = [], []
    for hit in used:
        extracted.extend(query_aware_extract(hit["text"], question, n_sentences=2))
        loc = f"page {hit['page']}" if hit["page"] else f"chunk {hit['chunk_index']}"
        sources.append({"filename": hit["filename"], "location": loc, "score": round(hit["score"], 3)})
    return {"answer": " ".join(extracted), "support": support, "sources": sources}

def summarize_document(store: DocumentStore, document_id: int, n_sentences: int = 5) -> dict:
    rows = store._all_chunks(document_id)
    if not rows:
        return {"summary": "", "sources": []}
    filename = rows[0][2]
    full_text = " ".join(r[6] for r in sorted(rows, key=lambda r: r[3]))
    return {"summary": " ".join(extractive_summarize(full_text, n_sentences=n_sentences)),
            "filename": filename, "n_chunks_used": len(rows)}
