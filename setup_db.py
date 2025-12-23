# setup_db.py
import sqlite3

DB_PATH = 'database.db'  # Path to your SQLite database

# Connect to SQLite (creates file if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,           -- 'income' or 'expense'
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL            -- Format: 'YYYY-MM-DD HH:MM:SS'
)
''')

conn.commit()
conn.close()
print("Database setup complete. 'transactions' table is ready.")
