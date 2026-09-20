"""
Conversation context and short-term/conversation storage.
"""
import time
import sqlite3
import threading
import json


def _locked(method):
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    wrapper.__name__ = method.__name__
    wrapper.__doc__ = method.__doc__
    return wrapper


class ConversationStore:
    def __init__(self, db_path: str = "orbit_conversations.db"):
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_conv_id ON messages(conversation_id)")
        self._conn.commit()

    @_locked
    def add_message(self, conversation_id: str, role: str, content: str) -> int:
        cur = self._conn.execute(
            "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (conversation_id, role, content, time.time()),
        )
        self._conn.commit()
        return cur.lastrowid

    @_locked
    def get_recent(self, conversation_id: str, limit: int = 10) -> list:
        cur = self._conn.execute(
            "SELECT role, content, created_at FROM messages WHERE conversation_id = ? "
            "ORDER BY id DESC LIMIT ?",
            (conversation_id, limit),
        )
        rows = cur.fetchall()
        rows.reverse()
        return [{"role": r, "content": c, "created_at": t} for r, c, t in rows]

    @_locked
    def list_conversations(self) -> list:
        cur = self._conn.execute(
            "SELECT conversation_id, COUNT(*), MIN(created_at), MAX(created_at) "
            "FROM messages GROUP BY conversation_id ORDER BY MAX(created_at) DESC"
        )
        return [{"conversation_id": r[0], "n_messages": r[1], "started_at": r[2], "last_at": r[3]}
                for r in cur.fetchall()]

    @_locked
    def search(self, query: str, conversation_id: str = None) -> list:
        like = f"%{query}%"
        if conversation_id:
            cur = self._conn.execute(
                "SELECT conversation_id, role, content, created_at FROM messages "
                "WHERE conversation_id = ? AND content LIKE ? ORDER BY id", (conversation_id, like))
        else:
            cur = self._conn.execute(
                "SELECT conversation_id, role, content, created_at FROM messages "
                "WHERE content LIKE ? ORDER BY id", (like,))
        return [{"conversation_id": r[0], "role": r[1], "content": r[2], "created_at": r[3]}
                for r in cur.fetchall()]

    @_locked
    def delete_conversation(self, conversation_id: str) -> int:
        cur = self._conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
        self._conn.commit()
        return cur.rowcount

    @_locked
    def export_conversation(self, conversation_id: str, fmt: str = "json") -> str:
        messages = self.get_recent(conversation_id, limit=10_000)
        if fmt == "json":
            return json.dumps(messages, indent=2)
        if fmt == "txt":
            return "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        if fmt in ("md", "markdown"):
            lines = [f"# Conversation: {conversation_id}\n"]
            for m in messages:
                lines.append(f"**{m['role']}**: {m['content']}\n")
            return "\n".join(lines)
        raise ValueError(f"unsupported export format: {fmt!r} (use json, txt, or md)")

    @_locked
    def close(self):
        self._conn.close()


DEFAULT_SYSTEM_MESSAGE = (
    "You are ORBIT, a small local research-prototype assistant. Be direct and "
    "honest about your limitations."
)


def build_context(tokenizer, current_message: str, conversation_id: str = None,
                   conversation_store: ConversationStore = None, memory_hits: list = None,
                   document_hits: list = None, system_message: str = DEFAULT_SYSTEM_MESSAGE,
                   max_tokens: int = 256, recent_turn_limit: int = 20) -> dict:
    def count_tokens(text):
        return len(tokenizer.encode(text, add_bos=False, add_eos=False))

    included = {"system": False, "memory": [], "documents": [], "conversation_turns": 0}

    sys_block = f"[system]\n{system_message}"
    current_block = f"[current message]\nuser: {current_message}"
    sys_tokens = count_tokens(sys_block)
    current_tokens = count_tokens(current_block)

    parts = []
    parts.append(sys_block)
    included["system"] = True
    budget = max(0, max_tokens - sys_tokens - current_tokens)

    if memory_hits:
        for hit in memory_hits:
            line = f"- {hit['text']}" if isinstance(hit, dict) else f"- {hit}"
            t = count_tokens(line)
            if t <= budget:
                if not any(p.startswith("[memory]") for p in parts):
                    header_t = count_tokens("[memory]")
                    if header_t <= budget:
                        parts.append("[memory]")
                        budget -= header_t
                parts.append(line)
                budget -= t
                included["memory"].append(line)
            else:
                break

    if document_hits:
        for hit in document_hits:
            loc = hit.get("location") or (f"page {hit['page']}" if hit.get("page") else "")
            cite = f"[{hit.get('filename', 'unknown')}{', ' + loc if loc else ''}]"
            block = f"- {hit['text']} {cite}"
            t = count_tokens(block)
            if t <= budget:
                if not any(p.startswith("[documents]") for p in parts):
                    header_t = count_tokens("[documents]")
                    if header_t <= budget:
                        parts.append("[documents]")
                        budget -= header_t
                parts.append(block)
                budget -= t
                included["documents"].append(cite)
            else:
                break

    conv_block_lines = []
    if conversation_id and conversation_store:
        recent = conversation_store.get_recent(conversation_id, limit=recent_turn_limit)
        kept = []
        for turn in reversed(recent):
            line = f"{turn['role']}: {turn['content']}"
            t = count_tokens(line)
            if t <= budget:
                kept.append(line)
                budget -= t
            else:
                break
        conv_block_lines = list(reversed(kept))
    if conv_block_lines:
        parts.append("[recent conversation]")
        parts.extend(conv_block_lines)
        included["conversation_turns"] = len(conv_block_lines)

    parts.append(current_block)
    prompt = "\n".join(parts)
    return {"prompt": prompt, "token_count": count_tokens(prompt), "included": included}
