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
            memo        TEXT,
            remind_at   TEXT,
            paid        INTEGER DEFAULT 0,
            reminded    INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()

def add_record(lender, borrower, amount, memo, remind_at):
    conn = get_connection()
    conn.execute("""
        INSERT INTO ledger (lender, borrower, amount, memo, remind_at)
        VALUES (?, ?, ?, ?, ?)
    """, (lender, borrower, amount, memo, remind_at))
    conn.commit()
    conn.close()

def get_all_records():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ledger ORDER BY created_at DESC").fetchall()
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

# リマインド対象のレコードを取得
def get_pending_reminders(now):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM ledger
        WHERE paid = 0
        AND remind_at IS NOT NULL
        AND remind_at <= ?
        AND reminded = 0
    """, (now,)).fetchall()
    conn.close()
    return rows

# リマインド済みにする
def mark_reminded(id):
    conn = get_connection()
    conn.execute("UPDATE ledger SET reminded = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB初期化完了")





