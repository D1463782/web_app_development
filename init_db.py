import sqlite3
import os

def init_db():
    os.makedirs('instance', exist_ok=True)
    db_path = os.path.join('instance', 'database.db')
    with sqlite3.connect(db_path) as conn:
        with open(os.path.join('database', 'schema.sql'), 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
