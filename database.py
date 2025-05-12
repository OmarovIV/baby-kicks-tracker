import sqlite3

def get_connection():
    return sqlite3.connect("baby_kicks.db")

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            kicks TEXT,
            comment TEXT,
            pregnancy_weeks TEXT,
            added_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_record(date, time, kicks, comment, pregnancy_weeks, added_at):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO kicks
        (date, time, kicks, comment, pregnancy_weeks, added_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, time, kicks, comment, pregnancy_weeks, added_at))
    conn.commit()
    conn.close()

def get_all_records():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM kicks ORDER BY date DESC, time DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_records_between_dates(start, end):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM kicks
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC, time DESC
    """, (start, end))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_records_by_date(date_str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM kicks WHERE date = ?", (date_str,))
    rows = cur.fetchall()
    conn.close()
    return rows

def record_exists(date, time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM kicks WHERE date = ? AND time = ?",
        (date, time)
    )
    exists = cur.fetchone()[0] > 0
    conn.close()
    return exists

def delete_record(record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM kicks WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
