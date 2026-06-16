import sqlite3

DB_PATH = "reminder.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ledger (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lender      TEXT NOT NULL,
            borrower    TEXT NOT NULL,
            amount      INTEGER NOT NULL,
            content     TEXT,
            paid        INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key     TEXT PRIMARY KEY,
            value   TEXT NOT NULL
        )
    """)
    # 既存テーブルに不足カラムがあれば追加
    existing = {row[1] for row in conn.execute("PRAGMA table_info(ledger)")}
    migrations = {
        "content": "ALTER TABLE ledger ADD COLUMN content TEXT",
    }
    for col, sql in migrations.items():
        if col not in existing:
            conn.execute(sql)
    conn.commit()
    conn.close()

def add_record(lender, borrower, amount, content):
    conn = get_connection()
    conn.execute("""
        INSERT INTO ledger (lender, borrower, amount, content)
        VALUES (?, ?, ?, ?)
    """, (lender, borrower, amount, content))
    conn.commit()
    conn.close()

def get_all_records():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ledger ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows

def get_unpaid_records():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ledger WHERE paid = 0 ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows

def mark_paid(id):
    conn = get_connection()
    conn.execute("UPDATE ledger SET paid = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def delete_record(id):
    conn = get_connection()
    conn.execute("DELETE FROM ledger WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def get_setting(key):
    conn = get_connection()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else None

def save_setting(key, value):
    conn = get_connection()
    conn.execute("""
        INSERT INTO settings (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (key, value))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB初期化完了")
