import sqlite3
import os

DB_PATH = "autoops/data/autoops.db"

def get_conn():
    os.makedirs("autoops/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # state table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS state (
        service TEXT PRIMARY KEY,
        status TEXT,
        fail_count INTEGER,
        restart_attempts INTEGER,
        recovery_pending INTEGER,
        reputation REAL,
        last_event TEXT,
        updated_at REAL
    )
    """)

    # tasks queue
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT,
        action TEXT,
        status TEXT,
        created_at REAL
    )
    """)

    # events log
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT,
        event TEXT,
        decision TEXT,
        created_at REAL
    )
    """)

    conn.commit()
    conn.close()
