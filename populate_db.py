# populate_db.py
import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = 'database.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Sample categories
income_categories = ['Salary', 'Freelance', 'Investments']
expense_categories = ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping']

# Insert 20 random transactions
for i in range(20):
    if random.choice([True, False]):
        t_type = 'income'
        category = random.choice(income_categories)
        amount = round(random.uniform(500, 5000), 2)
    else:
        t_type = 'expense'
        category = random.choice(expense_categories)
        amount = round(random.uniform(100, 2000), 2)
    
    date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO transactions (type, amount, category, date)
        VALUES (?, ?, ?, ?)
    ''', (t_type, amount, category, date))

conn.commit()
conn.close()
print("Sample transactions inserted into database.db")
