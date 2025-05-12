import sqlite3
from datetime import datetime

DB_PATH = "baby_kicks.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    """
    Ensure the main table exists, and add missing columns if needed.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # create base table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kicks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        kicks TEXT,
        comment TEXT
    )
    """)

    # get existing columns
    cursor.execute("PRAGMA table_info(kicks)")
    existing = {row[1] for row in cursor.fetchall()}

    # add pregnancy_weeks column if missing
    if "pregnancy_weeks" not in existing:
        cursor.execute("ALTER TABLE kicks ADD COLUMN pregnancy_weeks TEXT")

    # add added_at column if missing
    if "added_at" not in existing:
        cursor.execute("ALTER TABLE kicks ADD COLUMN added_at TEXT")

    conn.commit()
    conn.close()

def insert_record(date, time, kicks, comment, pregnancy_weeks, added_at=None):
    """
    Insert a new record with all fields.
    """
    if added_at is None:
        added_at = datetime.now().isoformat(timespec='seconds')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO kicks
      (date, time, kicks, comment, pregnancy_weeks, added_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, time, kicks, comment, pregnancy_weeks, added_at))
    conn.commit()
    conn.close()

def record_exists(date, time):
    """
    Check if a record for given date+time already exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM kicks WHERE date = ? AND time = ? LIMIT 1",
        (date, time)
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def get_all_records():
    """
    Return all records ordered by date/time desc.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, time, kicks, comment, pregnancy_weeks, added_at
          FROM kicks
         ORDER BY date DESC, time DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_records_between_dates(start_date, end_date):
    """
    Return records where date is between start_date and end_date inclusive.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, time, kicks, comment, pregnancy_weeks, added_at
          FROM kicks
         WHERE date BETWEEN ? AND ?
      ORDER BY date ASC, time ASC
    """, (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_record(record_id):
    """
    Delete record by its primary key.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kicks WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def update_record(record_id, date, time, kicks, comment, pregnancy_weeks):
    """
    Update an existing kick record’s fields.
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        """
        UPDATE kicks
           SET date             = ?,
               time             = ?,
               kicks            = ?,
               comment          = ?,
               pregnancy_weeks  = ?
         WHERE id = ?
        """,
        (date, time, kicks, comment, pregnancy_weeks, record_id)
    )
    conn.commit()
    conn.close()
