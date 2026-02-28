import sqlite3
from datetime import datetime
from typing import Optional

DB_NAME = "leads.db"


def init_db() -> None:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            telegram TEXT,
            message TEXT,
            telegram_user_id INTEGER NOT NULL,
            telegram_username TEXT
        );
    """)
    conn.commit()
    conn.close()


def save_lead(
    name: str,
    phone: str,
    email: str,
    telegram: Optional[str],
    message: Optional[str],
    user_id: int,
    username: Optional[str],
) -> str:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO leads (created_at, name, phone, email, telegram, message, telegram_user_id, telegram_username)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (created_at, name, phone, email, telegram or "", message or "", user_id, username or "")
    )
    conn.commit()
    conn.close()

    return created_at
