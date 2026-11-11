import os
import sqlite3

def get_db(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection

def init_db(database_path):
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    db = get_db(database_path)
    db.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT,
            designation TEXT,
            salary REAL DEFAULT 0
        )
    """)
    db.commit()
    db.close()
