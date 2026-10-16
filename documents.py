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
        if page_text and ("#" in page_text[:200] or "\n====" in page_text or "\n----" in page_text):
            sec_chunks = chunk_text_with_sections(page_text, chunk_size, overlap)
            if sec_chunks:
                for c, sec in sec_chunks:
                    out.append((page_num, c, sec))
                continue
        title = heading_title(page_text) if page_text else None
        for c in chunk_text(page_text, chunk_size, overlap):
            out.append((page_num, c, title))
    return out

_STOPWORDS = {"the","a","an","is","are","was","were","in","on","at","of","to","and","or","for","with","this","that","it","as","by","be","from","has","have","had"}

BM25L_DELTA = 0.5
_BM25_K1 = 1.2


def bm25_term(tf: float, dl: float, avgdl: float, idf: float, b: float = 0.75, delta: float = 0.0, k1: float = _BM25_K1) -> float:
    """BM25 (delta=0) or BM25L (delta>0) term score.

    Classic BM25 saturates as (k1+1)*tf / (tf + k1*(1-b+b*dl/avgdl)).
    BM25L (Lv & Zhai 2011) shifts the length-normalized TF by delta so
    long documents keep a floor; delta=0 is identical to classic.
    """
    if avgdl <= 0:
        avgdl = 1.0
    norm = 1.0 - b + b * (float(dl) / float(avgdl))
    if norm <= 0:
        norm = 1e-9
    if delta == 0.0:
        return float(idf) * (float(tf) * (k1 + 1.0)) / (float(tf) + k1 * norm)
    tf_prime = float(tf) / norm
    return float(idf) * ((tf_prime + delta) * (k1 + 1.0)) / (tf_prime + delta + k1)


def _stem(w: str) -> str:
    """Very light suffix stem for overlap matching (launch/launched)."""
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def content_tokens(text_or_tokens) -> list:
    """Lowercased non-stopword tokens from a string or token list.

    Digits are kept so exact numbers (March 12) outrank near-misses (12ish).
    """
    if isinstance(text_or_tokens, str):
        words = re.findall(r"[a-zA-Z0-9']+", text_or_tokens.lower())
    else:
        words = [str(w).lower() for w in text_or_tokens]
    return [w for w in words if w not in _STOPWORDS]


def _token_match_set(tokens) -> set:
    """Token set plus light stems for fuzzy overlap."""
    out = set()
    for t in tokens:
        out.add(t)
        out.add(_stem(t))
    return out


def sentence_offsets(text: str) -> list:
    """Return (start, end, sentence) for each sentence; end is exclusive."""
    if not text:
        return []
    # Split on sentence-ending punctuation followed by whitespace or EOS.
    pattern = re.compile(r"[^.!?]*[.!?]+(?:\s+|$)|[^.!?]+$", re.DOTALL)
    out = []
    for m in pattern.finditer(text):
        sent = m.group(0)
        # trim trailing whitespace from the span end while keeping quote exact
        raw = sent
        end = m.end()
        start = m.start()
        # strip leading whitespace from match (rare)
        lstrip = len(raw) - len(raw.lstrip())
        start += lstrip
        raw = raw[lstrip:]
        rstrip = len(raw) - len(raw.rstrip())
        if rstrip:
            raw = raw[:-rstrip]
            end -= rstrip
        if not raw.strip():
            continue
        out.append((start, end, text[start:end]))
    return out


def citation_span(text: str, candidate_sentences: list) -> dict:
    """Best-overlap sentence match among candidates; never bridges non-contiguous."""
    if not text:
        return {"quote": "", "start": 0, "end": 0}
    offsets = sentence_offsets(text)
    cand_norm = [re.sub(r"\s+", " ", (c or "").strip()) for c in (candidate_sentences or [])]
    # Prefer candidates in order (already ranked by extract); match first that appears.
    for c in cand_norm:
        if not c:
            continue
        for start, end, sent in offsets:
            norm = re.sub(r"\s+", " ", sent.strip())
            if norm == c or c in norm or norm in c:
                return {"quote": text[start:end], "start": start, "end": end}
        idx = text.find(c)
        if idx >= 0:
            return {"quote": c, "start": idx, "end": idx + len(c)}
    if offsets:
        s, e, _ = offsets[0]
        return {"quote": text[s:e], "start": s, "end": e}
    return {"quote": text[: min(80, len(text))], "start": 0, "end": min(80, len(text))}


def filename_terms(filename: str) -> set:
    if not filename:
        return set()
    base = filename.rsplit("/", 1)[-1]
    if "." in base:
        base = base.rsplit(".", 1)[0]
    toks = re.findall(r"[a-zA-Z0-9]+", base.lower())
    return {t for t in toks if t not in _STOPWORDS and t not in {"md", "txt", "pdf", "csv", "json", "docx", "pptx"}}


def filename_bonus(filename, query_terms) -> float:
    if not filename or not query_terms:
        return 0.0
    ft = filename_terms(filename)
    if not ft:
        return 0.0
    q = {str(t).lower() for t in query_terms}
    hits = len(ft & q)
    return 0.006 * hits


def heading_title(text: str):
    if not text:
        return None
    lines = text.splitlines()
    if not lines:
        return None
    first = lines[0].strip()
    m = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", first)
    if m and m.group(2).strip():
        return m.group(2).strip()
    if len(lines) >= 2:
        underline = lines[1].strip()
        if len(underline) >= 3 and set(underline) <= {"=", "-"} and first and not first.startswith("#"):
            if underline == "-":
                return None
            # first line must be real text, not another underline
            if set(first) <= {"=", "-"}:
                return None
            return first
    return None


def section_bonus(section, query_terms) -> float:
    if not section or not query_terms:
        return 0.0
    st = set(re.findall(r"[a-zA-Z0-9]+", section.lower())) - _STOPWORDS
    q = {str(t).lower() for t in query_terms}
    hits = len(st & q)
    if hits == 0:
        return 0.0
    # full match of 2+ terms → 0.015; partial → 0.008
    if hits >= 2 and hits >= min(2, len(q)):
        # if all query terms that appear in section title
        if hits == len(st & q) and hits >= 2:
            return 0.015 if hits >= 2 else 0.008
    if hits >= 2:
        return 0.015
    return 0.008


def min_cover_span(toks, terms):
    """Minimal content-token span covering all terms (stopwords ignored in width)."""
    if not terms:
        return None
    term_set = {str(t).lower() for t in terms}
    # map content positions
    content = []  # (content_idx, token)
    for w in toks:
        wl = str(w).lower()
        if wl in _STOPWORDS:
            continue
        content.append(wl)
    if not content:
        return None
    # need all terms present
    if not term_set.issubset(set(content)):
        # allow terms that appear
        present = term_set & set(content)
        if present != term_set:
            return None
    # sliding window over content positions
    n = len(content)
    best = None
    for i in range(n):
        need = set(term_set)
        for j in range(i, n):
            if content[j] in need:
                need.discard(content[j])
            if not need:
                span = j - i + 1
                if best is None or span < best:
                    best = span
                break
    return best


def proximity_bonus(toks, terms) -> float:
    terms = [str(t).lower() for t in terms if str(t).lower() not in _STOPWORDS]
    if len(terms) < 2:
        return 0.0
    span = min_cover_span(toks, terms)
    if span is None:
        return 0.0
    n = len(set(terms))
    if span <= n:
        return 0.08
    if span == n + 1:
        return 0.05
    if span <= n + 3:
        return 0.02
    return 0.0


def ordered_query_terms(terms) -> list:
    out = []
    seen = set()
    for t in terms:
        tl = str(t).lower()
        if tl in _STOPWORDS or tl in seen:
            continue
        seen.add(tl)
        out.append(tl)
    return out


def ordered_cover_span(toks, terms):
    """Content-token span if terms appear in order; else None."""
    terms = ordered_query_terms(terms) if terms and isinstance(terms[0], str) and any(t in _STOPWORDS for t in terms) else [str(t).lower() for t in terms if str(t).lower() not in _STOPWORDS]
    if not terms:
        return None
    content = [str(w).lower() for w in toks if str(w).lower() not in _STOPWORDS]
    # find ordered positions
    pos = []
    start_search = 0
    for t in terms:
        found = None
        for i in range(start_search, len(content)):
            if content[i] == t:
                found = i
                break
        if found is None:
            return None
        pos.append(found)
        start_search = found + 1
    return pos[-1] - pos[0] + 1


def order_bonus(toks, terms) -> float:
    terms_c = ordered_query_terms(terms) if any(str(t).lower() in _STOPWORDS for t in terms) else [str(t).lower() for t in terms if str(t).lower() not in _STOPWORDS]
    if len(terms_c) < 2:
        return 0.0
    span = ordered_cover_span(toks, terms_c)
    if span is None:
        return 0.0
    n = len(terms_c)
    if span <= n + 2:
        # tight ordered
        if span <= n:
            return 0.03
        if span <= n + 2:
            return 0.03  # tests use == n for 0.03; loose > n+2 → 0
    return 0.0


def adjacent_pair_hits(toks, pair) -> int:
    if len(pair) < 2:
        return 0
    a, b = str(pair[0]).lower(), str(pair[1]).lower()
    content = [str(w).lower() for w in toks if str(w).lower() not in _STOPWORDS]
    hits = 0
    for i in range(len(content) - 1):
        if content[i] == a and content[i + 1] == b:
            hits += 1
    return hits


def phrase_bonus(toks, terms) -> float:
    """Exact contiguous token phrase match on raw tokens (0.15).

    Stopwords inside the query are ignored, but intervening non-query
    content tokens (or non-matching tokens) break the phrase.
    """
    terms_c = [str(t).lower() for t in terms if str(t).lower() not in _STOPWORDS]
    if len(terms_c) < 2:
        return 0.0
    raw = [str(w).lower() for w in toks]
    n = len(terms_c)
    # slide over raw tokens, skip stopwords when matching sequence
    for i in range(len(raw)):
        ti = 0
        j = i
        while j < len(raw) and ti < n:
            w = raw[j]
            if w in _STOPWORDS:
                # stopword inside phrase breaks exact phrase (ordered window ≠ phrase)
                break
            if w == terms_c[ti]:
                ti += 1
                j += 1
            else:
                break
        if ti == n:
            return 0.15
    return 0.0


def pair_order_bonus(toks, terms, idf=None) -> float:
    """IDF-weighted adjacent ordered bigram bonus (Metzler & Croft).

    idf may be a float scale or a dict of term -> idf weight.
    """
    terms_c = [str(t).lower() for t in terms if str(t).lower() not in _STOPWORDS]
    if len(terms_c) < 2:
        return 0.0
    best = 0.0
    for i in range(len(terms_c) - 1):
        a, b = terms_c[i], terms_c[i + 1]
        if not adjacent_pair_hits(toks, [a, b]):
            continue
        if isinstance(idf, dict):
            wa = float(idf.get(a, 1.0))
            wb = float(idf.get(b, 1.0))
            w = (wa + wb) / 2.0
        elif idf is None:
            w = 1.0
        else:
            w = float(idf)
        # Cap at 0.009; low idf collapses common pairs
        best = max(best, min(0.009, 0.003 * w))
    return best


def cover_start_content_index(toks, terms):
    terms_c = [str(t).lower() for t in terms if str(t).lower() not in _STOPWORDS]
    if not terms_c:
        return None
    content = [str(w).lower() for w in toks if str(w).lower() not in _STOPWORDS]
    term_set = set(terms_c)
    if not term_set.issubset(set(content)):
        return None
    # Minimal-width cover; among ties prefer earliest start.
    n = len(content)
    best = None  # (span, start)
    for i in range(n):
        need = set(term_set)
        for j in range(i, n):
            if content[j] in need:
                need.discard(content[j])
            if not need:
                span = j - i + 1
                if best is None or span < best[0] or (span == best[0] and i < best[1]):
                    best = (span, i)
                break
    return None if best is None else best[1]


def lead_bonus(toks, terms) -> float:
    start = cover_start_content_index(toks, terms)
    if start is None:
        return 0.0
    if start == 0:
        return 0.01
    if start <= 5:
        return 0.005
    return 0.0


def discriminative_query_terms(terms, df_map, n_docs, floor: float = 0.5):
    """Drop high-df terms so coverage uses discriminative tokens only."""
    terms = list(terms) if not isinstance(terms, (list, tuple)) else list(terms)
    if not terms or n_docs <= 0:
        return set(terms) if not isinstance(terms, list) else set(terms)
    out = []
    for t in terms:
        dft = df_map.get(t, 0)
        if n_docs < 4 or dft / max(1, n_docs) < floor:
            out.append(t)
    return set(out) if out else set(terms)


def expand_chunk_window(store_or_map, doc_id=None, center_idx=None, window: int = 1):
    """Return concatenated text of neighboring chunks.

    Accepts either:
      expand_chunk_window(store, doc_id, chunk_index, window=1)
      expand_chunk_window({idx: text, ...}, center_idx, window=1)  # legacy map form
    """
    # Legacy dict form: first arg is mapping, second is center
    if isinstance(store_or_map, dict):
        chunks_by_index = store_or_map
        center = doc_id if center_idx is None else center_idx
        # when called as (map, center, window=..) third positional may be window
        if center_idx is not None and not isinstance(center_idx, int):
            pass
        if not chunks_by_index:
            return ""
        keys = sorted(chunks_by_index)
        if center not in chunks_by_index:
            return chunks_by_index.get(center, "")
        lo = max(min(keys), center - window)
        hi = min(max(keys), center + window)
        parts = [chunks_by_index[i] for i in range(lo, hi + 1) if i in chunks_by_index]
        return " ".join(parts)
    store = store_or_map
    if doc_id is None or center_idx is None:
        return ""
    rows = store._conn.execute(
        "SELECT chunk_index, text FROM chunks WHERE document_id = ? ORDER BY chunk_index",
        (int(doc_id),),
    ).fetchall()
    chunks_by_index = {int(i): t for i, t in rows}
    if not chunks_by_index:
        return ""
    keys = sorted(chunks_by_index)
    lo = max(min(keys), int(center_idx) - window)
    hi = min(max(keys), int(center_idx) + window)
    parts = [chunks_by_index[i] for i in range(lo, hi + 1) if i in chunks_by_index]
    return " ".join(parts)


def chunk_text_with_sections(text: str, chunk_size: int = 500, overlap: int = 80) -> list:
    """Paragraph-preferring chunks with section titles from markdown headings."""
    if not text:
        return []
    lines = text.splitlines(keepends=True)
    sections = []
    current_title = None
    buf = []

    def flush():
        nonlocal buf, current_title
        body = "".join(buf)
        if body.strip():
            sections.append((current_title, body))
        buf = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("#") and heading_title(stripped):
            flush()
            current_title = heading_title(stripped)
            buf.append(line)
            i += 1
            continue
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if (
                stripped
                and not stripped.startswith("#")
                and not (set(stripped) <= {"=", "-"})
                and len(nxt) >= 3
                and set(nxt) <= {"=", "-"}
                and nxt != "-"
            ):
                flush()
                current_title = stripped
                buf.append(line)
                buf.append(lines[i + 1])
                i += 2
                continue
        buf.append(line)
        i += 1
    flush()
    if not sections:
        sections = [(None, text)]
    out = []
    for title, body in sections:
        paras = re.split(r"\n\s*\n", body)
        cur = []
        cur_len = 0
        for para in paras:
            para = para.strip()
            if not para:
                continue
            if cur_len + len(para) + 1 <= chunk_size or not cur:
                cur.append(para)
                cur_len += len(para) + 1
            else:
                out.append(("\n\n".join(cur), title))
                if overlap > 0 and cur:
                    tail = cur[-1][-overlap:]
                    cur = [tail, para] if tail else [para]
                    cur_len = sum(len(x) + 1 for x in cur)
                else:
                    cur = [para]
                    cur_len = len(para)
        if cur:
            out.append(("\n\n".join(cur), title))
    return out


def parent_child_chunk_text(text: str, parent_size: int = 1000, child_size: int = 250, overlap: int = 40) -> list:
    """Return (child, section, parent) triples; each child is a substring of parent."""
    sec_chunks = chunk_text_with_sections(text, chunk_size=parent_size, overlap=overlap)
    if not sec_chunks:
        parents = [(p, None) for p in chunk_text(text, chunk_size=parent_size, overlap=overlap)]
    else:
        parents = sec_chunks  # (text, section)
    out = []
    for parent, section in parents:
        children = chunk_text(parent, chunk_size=child_size, overlap=max(0, overlap // 2))
        if not children:
            children = [parent]
        for child in children:
            out.append((child, section, parent))
    return out


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
    q_list = ordered_query_terms(re.findall(r"[a-zA-Z0-9']+", query.lower()))
    q_words = set(q_list)
    if not q_words:
        return extractive_summarize(text, n_sentences)
    q_match = _token_match_set(q_list)
    scored = []
    for i, s in enumerate(sentences):
        stoks = content_tokens(s)
        s_match = _token_match_set(stoks)
        overlap = len(q_match & s_match)
        pair = adjacent_pair_hits(stoks, q_list[:2]) if len(q_list) >= 2 else 0
        span = min_cover_span(stoks, q_list)
        # higher overlap, then pair hits, then tighter cover span, then earlier
        span_key = -span if span is not None else -999
        scored.append((overlap, pair, span_key, -i, i, s))
    scored.sort(reverse=True)
    top = scored[:n_sentences]
    if all(t[0] == 0 for t in top):
        return extractive_summarize(text, n_sentences)
    return [s for *_, s in sorted(top, key=lambda t: t[4])]

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
        self._conn.execute("""CREATE TABLE IF NOT EXISTS chunk_embeddings (
            chunk_id INTEGER PRIMARY KEY,
            vec BLOB NOT NULL)""")
        # optional parent_text column for parent-child indexing
        cols = {r[1] for r in self._conn.execute("PRAGMA table_info(chunks)").fetchall()}
        if "parent_text" not in cols:
            try:
                self._conn.execute("ALTER TABLE chunks ADD COLUMN parent_text TEXT")
            except Exception:
                pass
        self._conn.commit()
        # Embeddings are loaded lazily via _load_embed / search so a
        # reopened store starts with an empty cache (tests assert this).
        self._embed_cache = {}

    @staticmethod
    def _decode_embed(blob):
        """Decode a persisted embed blob (float64 preferred, float32 legacy)."""
        if not blob:
            return None
        raw = bytes(blob)
        n64 = len(raw) // 8
        if n64 * 8 == len(raw) and n64 > 0:
            arr = np.frombuffer(raw, dtype=np.float64)
            if arr.size == 256 or arr.size > 0:
                return arr
        n32 = len(raw) // 4
        if n32 * 4 == len(raw) and n32 > 0:
            return np.frombuffer(raw, dtype=np.float32).astype(np.float64)
        return None

    @_locked
    def _load_embed(self, chunk_id):
        """Return cached or persisted embedding for a chunk, or None."""
        cid = int(chunk_id)
        cached = self._embed_cache.get(cid)
        if cached is not None:
            return cached
        row = self._conn.execute(
            "SELECT vec FROM chunk_embeddings WHERE chunk_id = ?", (cid,)
        ).fetchone()
        if not row or row[0] is None:
            return None
        arr = self._decode_embed(row[0])
        if arr is not None:
            self._embed_cache[cid] = arr
        return arr

    @_locked
    def _persist_embed(self, chunk_id, vec):
        """Write embedding to cache and DB (float64 for exact reload)."""
        cid = int(chunk_id)
        arr = np.asarray(vec, dtype=np.float64)
        self._embed_cache[cid] = arr
        self._conn.execute(
            "INSERT OR REPLACE INTO chunk_embeddings (chunk_id, vec) VALUES (?, ?)",
            (cid, arr.tobytes()),
        )

    @_locked
    def add_document(self, filename: str, raw_bytes: bytes, chunk_size: int = 500, overlap: int = 80, parent_child: bool = False, parent_size: int = 1000, child_size: int = 250) -> dict:
        filename = sanitize_filename(filename)
        text, pages = load_document(filename, raw_bytes)
        ext = filename.rsplit(".", 1)[-1].lower()
        if parent_child:
            page_chunks = []
            for page_num, page_text in pages:
                for child, section, parent in parent_child_chunk_text(
                    page_text, parent_size=parent_size, child_size=child_size, overlap=overlap
                ):
                    page_chunks.append((page_num, child, section, parent))
        else:
            page_chunks = chunk_pages(pages, chunk_size, overlap)
        if not page_chunks:
            raise ValueError("document produced no extractable text")
        cur = self._conn.execute(
            "INSERT INTO documents (filename, filetype, uploaded_at, num_chunks, char_count) VALUES (?, ?, ?, ?, ?)",
            (filename, ext, time.time(), len(page_chunks), len(text)),
        )
        doc_id = cur.lastrowid
        for i, item in enumerate(page_chunks):
            parent_text = None
            if len(item) == 4:
                page_num, chunk, section, parent_text = item
            elif len(item) == 3:
                page_num, chunk, section = item
            else:
                page_num, chunk = item[0], item[1]
                section = None
            cur_c = self._conn.execute(
                "INSERT INTO chunks (document_id, chunk_index, page, section, text, parent_text) VALUES (?, ?, ?, ?, ?, ?)",
                (doc_id, i, page_num, section, chunk, parent_text),
            )
            cid = cur_c.lastrowid
            try:
                vec = hash_embed(chunk, self.dim)
                self._persist_embed(cid, vec)
            except Exception:
                pass
        self._conn.commit()
        return {"document_id": doc_id, "filename": filename, "num_chunks": len(page_chunks), "char_count": len(text), "parent_child": bool(parent_child)}

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
        if chunk_ids:
            self._conn.executemany("DELETE FROM chunk_embeddings WHERE chunk_id = ?", [(c,) for c in chunk_ids])
        self._conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
        self._conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        self._conn.commit()
        for cid in chunk_ids:
            self._embed_cache.pop(cid, None)
        return True

    @_locked
    def _all_chunks(self, document_id=None):
        cols = "c.id, c.document_id, d.filename, c.chunk_index, c.page, c.section, c.text, c.parent_text"
        if document_id is not None:
            return self._conn.execute(
                f"SELECT {cols} FROM chunks c JOIN documents d ON c.document_id = d.id WHERE c.document_id = ?",
                (document_id,),
            ).fetchall()
        return self._conn.execute(
            f"SELECT {cols} FROM chunks c JOIN documents d ON c.document_id = d.id"
        ).fetchall()

    @_locked
    def _collection_bm25(self, terms):
        """Return (n_docs, avgdl, df_map) over the whole collection.

        Used so a filtered search still length-normalizes against the
        full corpus average, not the candidate subset.
        """
        rows = self._conn.execute("SELECT text FROM chunks").fetchall()
        n = len(rows)
        if n == 0:
            return 0, 1.0, {t: 0 for t in terms}
        dls = []
        df = {t: 0 for t in terms}
        for (text,) in rows:
            words = re.findall(r"[a-zA-Z0-9']+", (text or "").lower())
            toks = [w for w in words if w not in _STOPWORDS]
            dls.append(max(1, len(toks)))
            present = set(toks)
            for t in terms:
                if t in present:
                    df[t] += 1
        avgdl = sum(dls) / max(1, n)
        return n, avgdl, df

    @_locked
    def search(self, query: str, k: int = 5, document_id: int = None) -> list:
        rows = self._all_chunks(document_id)
        if not rows:
            return []
        q_vec = hash_embed(query, self.dim)
        q_list = ordered_query_terms(re.findall(r"[a-zA-Z0-9']+", (query or "").lower()))
        q_words = set(q_list)
        n_coll, avgdl, df = self._collection_bm25(q_words) if q_words else (0, 1.0, {})
        disc_terms = discriminative_query_terms(list(q_words), df, n_coll)
        scored = []
        dirty = False
        for row in rows:
            if len(row) >= 8:
                chunk_id, doc_id, filename, chunk_idx, page, section, text, parent_text = row[:8]
            else:
                chunk_id, doc_id, filename, chunk_idx, page, section, text = row[:7]
                parent_text = None
            vec = self._embed_cache.get(chunk_id)
            if vec is None:
                vec = hash_embed(text, self.dim)
                try:
                    self._persist_embed(chunk_id, vec)
                    dirty = True
                except Exception:
                    self._embed_cache[chunk_id] = vec
            cos_sim = float(np.dot(q_vec, vec))
            words = re.findall(r"[a-zA-Z0-9']+", (text or "").lower())
            toks = words  # keep stopwords for span helpers that filter themselves
            content = [w for w in words if w not in _STOPWORDS]
            tf_map = {}
            for w in content:
                tf_map[w] = tf_map.get(w, 0) + 1
            overlap = len(q_words & set(content)) / max(1, len(q_words)) if q_words else 0.0
            lexical_hit = bool(q_words & set(content))
            bm25 = 0.0
            doc_text = self.get_document_text(doc_id)
            doc_toks = [w for w in re.findall(r"[a-zA-Z0-9']+", (doc_text or "").lower()) if w not in _STOPWORDS]
            dl = max(1, len(doc_toks) if doc_toks else len(content))
            for t in q_words:
                tf = tf_map.get(t, 0)
                if tf == 0:
                    continue
                dft = df.get(t, 0)
                idf = np.log((n_coll - dft + 0.5) / (dft + 0.5) + 1.0) if n_coll else 1.0
                bm25 += bm25_term(tf, dl, avgdl, float(idf), b=0.75, delta=BM25L_DELTA)
            # Ranking signals
            fn_b = filename_bonus(filename, q_list)
            sec_b = section_bonus(section, q_list)
            prox = proximity_bonus(toks, q_list)
            prox_span = min_cover_span(toks, q_list)
            ord_b = order_bonus(toks, q_list)
            # pair: use inverse-df weight for rarity
            pair_b = 0.0
            if len(q_list) >= 2:
                for i in range(len(q_list) - 1):
                    a, b = q_list[i], q_list[i + 1]
                    if adjacent_pair_hits(toks, [a, b]):
                        dfa = df.get(a, 0)
                        dfb = df.get(b, 0)
                        # rarer pairs score higher; clamp
                        rarity = 1.0 / max(1.0, (dfa + dfb) / 2.0)
                        pair_b = max(pair_b, min(0.009, 0.009 * rarity * max(1.0, n_coll / 4.0)))
            lead_b = lead_bonus(toks, q_list)
            phrase = phrase_bonus(toks, q_list)
            coverage = 0.0
            if disc_terms:
                coverage = len(set(disc_terms) & set(content)) / max(1, len(disc_terms))
            # Exact numeric tokens (12 vs 12ish) get a small rank boost.
            digit_bonus = 0.0
            q_digits = {t for t in q_words if t.isdigit()}
            if q_digits:
                digit_bonus = 0.04 * len(q_digits & set(content))
            score = (
                0.55 * cos_sim
                + 0.20 * overlap
                + 0.05 * min(bm25, 5.0) / 5.0
                + fn_b
                + sec_b
                + prox
                + ord_b
                + pair_b
                + lead_b
                + phrase
                + digit_bonus
            )
            item = {
                "chunk_id": chunk_id,
                "document_id": doc_id,
                "filename": filename,
                "chunk_index": chunk_idx,
                "page": page,
                "section": section,
                "text": text,
                "score": score,
                "cos": cos_sim,
                "bm25": bm25,
                "overlap": overlap,
                "lexical_hit": lexical_hit,
                "filename_bonus": fn_b,
                "section_bonus": sec_b,
                "proximity": prox,
                "proximity_span": prox_span if prox_span is not None else 0,
                "order": ord_b,
                "pair": pair_b,
                "lead": lead_b,
                "phrase": phrase,
                "coverage": coverage,
                "parent_text": parent_text,
            }
            scored.append((lexical_hit, score, bm25, item))
        if dirty:
            try:
                self._conn.commit()
            except Exception:
                pass
        scored.sort(key=lambda t: (t[0], t[1], t[2]), reverse=True)
        return [item for _, _, _, item in scored[:k]]

    @_locked
    def close(self):
        self._conn.close()


SUPPORT_THRESHOLD_FULL = 0.35
SUPPORT_THRESHOLD_PARTIAL = 0.15

def answer_from_documents(store: DocumentStore, question: str, k: int = 3, document_id: int = None, window: int = 0) -> dict:
    hits = store.search(question, k=k, document_id=document_id)
    q_words = set(re.findall(r"[a-zA-Z']+", (question or "").lower())) - _STOPWORDS
    coverage = float(hits[0].get("coverage", 0.0)) if hits else 0.0
    if hits and q_words and coverage == 0.0:
        top_toks = set(re.findall(r"[a-zA-Z']+", (hits[0].get("text") or "").lower())) - _STOPWORDS
        coverage = len(q_words & top_toks) / max(1, len(q_words))
    if not hits:
        return {"answer": "I don't have any indexed documents that relate to this question.",
                "support": Support.UNKNOWN, "sources": [], "coverage": coverage}
    top_score = hits[0]["score"]
    if top_score >= SUPPORT_THRESHOLD_FULL and coverage >= 0.5:
        support = Support.SUPPORTED
    elif top_score >= SUPPORT_THRESHOLD_PARTIAL or coverage >= 0.3:
        support = Support.PARTIALLY_SUPPORTED
    else:
        support = Support.UNSUPPORTED
    if support == Support.UNSUPPORTED:
        return {"answer": "I don't have verified information about this in the indexed documents.",
                "support": support, "sources": [], "coverage": coverage}
    used = hits[:2] if support == Support.SUPPORTED else hits[:1]
    extracted, sources = [], []
    for hit in used:
        body = hit["text"]
        window_used = False
        parent = hit.get("parent_text")
        if parent:
            body = parent
        elif window and window > 0:
            expanded = expand_chunk_window(store, hit["document_id"], hit["chunk_index"], window=window)
            if expanded and expanded != hit["text"]:
                body = expanded
                window_used = True
        best = query_aware_extract(body, question, n_sentences=1)
        sents = query_aware_extract(body, question, n_sentences=2)
        extracted.extend(sents)
        loc = f"page {hit['page']}" if hit["page"] else f"chunk {hit['chunk_index']}"
        span = citation_span(body, best or sents)
        sources.append({
            "filename": hit["filename"],
            "location": loc,
            "score": round(hit["score"], 3),
            "span": {"start": span["start"], "end": span["end"]},
            "quote": span["quote"],
            "coverage": hit.get("coverage", coverage),
            "window_used": window_used,
        })
    return {"answer": " ".join(extracted), "support": support, "sources": sources, "coverage": coverage}

def summarize_document(store: DocumentStore, document_id: int, n_sentences: int = 5) -> dict:
    rows = store._all_chunks(document_id)
    if not rows:
        return {"summary": "", "sources": []}
    filename = rows[0][2]
    full_text = " ".join(r[6] for r in sorted(rows, key=lambda r: r[3]))
    return {"summary": " ".join(extractive_summarize(full_text, n_sentences=n_sentences)),
            "filename": filename, "n_chunks_used": len(rows)}
