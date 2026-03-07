"""
Database — SQLite storage for conversations, messages, and persistent memory.
Zero setup, single file, works offline.
"""

from __future__ import annotations

import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path


def _now() -> str:
    return datetime.now(UTC).isoformat()


class Database:
    """SQLite database for conversations, messages, and memory."""

    def __init__(self, db_path: str = "data/chat.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL DEFAULT 'New Chat',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'general',
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_messages_conv
                ON messages(conversation_id);
            CREATE INDEX IF NOT EXISTS idx_messages_timestamp
                ON messages(timestamp);
            CREATE INDEX IF NOT EXISTS idx_memory_category
                ON memory(category);
        """)
        conn.commit()
        conn.close()

    # ─── Conversations ────────────────────────────────────────────

    def create_conversation(self, title: str = "New Chat") -> dict:
        conv_id = str(uuid.uuid4())
        now = _now()
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (conv_id, title, now, now),
        )
        conn.commit()
        conn.close()
        return {"id": conv_id, "title": title, "created_at": now, "updated_at": now}

    def list_conversations(self) -> list[dict]:
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM conversations ORDER BY updated_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_conversation(self, conv_id: str) -> dict | None:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def rename_conversation(self, conv_id: str, title: str) -> bool:
        conn = self._get_conn()
        result = conn.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, _now(), conv_id),
        )
        conn.commit()
        conn.close()
        return result.rowcount > 0

    def delete_conversation(self, conv_id: str) -> bool:
        conn = self._get_conn()
        result = conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
        conn.commit()
        conn.close()
        return result.rowcount > 0

    def auto_title_conversation(self, conv_id: str, first_message: str) -> str:
        """Generate a title from the first user message (first 50 chars)."""
        title = first_message.strip()[:50]
        if len(first_message.strip()) > 50:
            title += "..."
        self.rename_conversation(conv_id, title)
        return title

    # ─── Messages ─────────────────────────────────────────────────

    def add_message(self, conv_id: str, role: str, content: str) -> dict:
        now = _now()
        conn = self._get_conn()
        cursor = conn.execute(
            "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (conv_id, role, content, now),
        )
        # Update conversation's updated_at
        conn.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (now, conv_id),
        )
        conn.commit()
        msg_id = cursor.lastrowid
        conn.close()
        return {
            "id": msg_id,
            "conversation_id": conv_id,
            "role": role,
            "content": content,
            "timestamp": now,
        }

    def get_messages(self, conv_id: str) -> list[dict]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
            (conv_id,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_recent_messages(self, conv_id: str, limit: int = 20) -> list[dict]:
        """Get last N messages for context window."""
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT ?",
            (conv_id, limit),
        ).fetchall()
        conn.close()
        # Reverse to get chronological order
        return [dict(r) for r in reversed(rows)]

    def get_message_count(self, conv_id: str) -> int:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT COUNT(*) as count FROM messages WHERE conversation_id = ?",
            (conv_id,),
        ).fetchone()
        conn.close()
        return row["count"] if row else 0

    # ─── Memory (persistent facts across conversations) ───────────

    def add_memory(self, key: str, value: str, category: str = "general") -> dict:
        now = _now()
        conn = self._get_conn()
        cursor = conn.execute(
            "INSERT INTO memory (key, value, category, created_at) VALUES (?, ?, ?, ?)",
            (key, value, category, now),
        )
        conn.commit()
        mem_id = cursor.lastrowid
        conn.close()
        return {
            "id": mem_id,
            "key": key,
            "value": value,
            "category": category,
            "created_at": now,
        }

    def get_all_memory(self) -> list[dict]:
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM memory ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_memory_by_category(self, category: str) -> list[dict]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM memory WHERE category = ? ORDER BY created_at DESC",
            (category,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def delete_memory(self, mem_id: int) -> bool:
        conn = self._get_conn()
        result = conn.execute("DELETE FROM memory WHERE id = ?", (mem_id,))
        conn.commit()
        conn.close()
        return result.rowcount > 0

    def get_memory_context(self) -> str:
        """Get all memory formatted as context string for the LLM."""
        memories = self.get_all_memory()
        if not memories:
            return ""
        lines = []
        for m in memories[:50]:  # Limit to 50 most recent facts
            lines.append(f"- {m['key']}: {m['value']}")
        return "\n".join(lines)

    # ─── Stats ────────────────────────────────────────────────────

    def get_stats(self) -> dict:
        conn = self._get_conn()
        convs = conn.execute("SELECT COUNT(*) as c FROM conversations").fetchone()
        msgs = conn.execute("SELECT COUNT(*) as c FROM messages").fetchone()
        mems = conn.execute("SELECT COUNT(*) as c FROM memory").fetchone()
        conn.close()
        return {
            "conversations": convs["c"],
            "messages": msgs["c"],
            "memory_facts": mems["c"],
        }
