import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create transactions table
c.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("Database and 'transactions' table created successfully!")
