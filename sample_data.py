import sqlite3
from datetime import datetime

conn = sqlite3.connect("database.db")
c = conn.cursor()

sample_data = [
    ('income', 5000, 'Salary', datetime.now().strftime('%Y-%m-%d')),
    ('expense', 1500, 'Food', datetime.now().strftime('%Y-%m-%d')),
    ('expense', 800, 'Transport', datetime.now().strftime('%Y-%m-%d')),
]

c.executemany("INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)", sample_data)

conn.commit()
conn.close()
print("✅ Sample transactions added!")
