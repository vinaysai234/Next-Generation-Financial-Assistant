import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
c = conn.cursor()

sample_data = [
    ('income', 5000, 'Salary', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ('expense', 150, 'Food', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ('expense', 200, 'Transport', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ('income', 2000, 'Freelance', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ('expense', 300, 'Entertainment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
]

c.executemany('INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)', sample_data)

conn.commit()
conn.close()
print("Sample transactions added successfully!")

