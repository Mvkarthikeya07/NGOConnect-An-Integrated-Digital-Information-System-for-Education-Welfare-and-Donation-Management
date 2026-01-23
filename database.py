import sqlite3

def connect_db():
    return sqlite3.connect("ngo.db")

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS beneficiaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        education TEXT,
        support_type TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        contact TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor TEXT,
        amount INTEGER,
        purpose TEXT
    )
    """)

    conn.commit()
    conn.close()
