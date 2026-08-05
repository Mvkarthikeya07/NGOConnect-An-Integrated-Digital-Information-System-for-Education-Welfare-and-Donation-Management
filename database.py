import hashlib
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "ngo.db"


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_tables():
    with connect_db() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS beneficiaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            education TEXT,
            support_type TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT,
            contact TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor TEXT NOT NULL,
            amount INTEGER,
            purpose TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()

    ensure_default_user()


def ensure_default_user():
    if not get_user_by_username("user"):
        create_user("user", "user123")


def get_user_by_username(username):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()


def create_user(username, password):
    username = username.strip()
    if not username or not password:
        return False

    try:
        with connect_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password))
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def validate_user(username, password):
    user = get_user_by_username(username.strip())
    if not user:
        return False

    return user["password_hash"] == hash_password(password)


def update_user_password(username, new_password):
    username = username.strip()
    if not username or not new_password:
        return False

    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (hash_password(new_password), username)
        )
        conn.commit()
        return cur.rowcount > 0
