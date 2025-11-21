import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'tasks.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    status TEXT DEFAULT 'pending',
    created_at TEXT
);
"""

def init_db(path=DB_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.executescript(SCHEMA)
        conn.commit()
        print(f"Initialized DB at {path}")
    finally:
        conn.close()


if __name__ == '__main__':
    init_db()
