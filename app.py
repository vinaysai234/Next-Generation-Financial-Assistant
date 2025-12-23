from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import pandas as pd
from config import DB_PATH, CURRENCY  # ✅ your config import

print(f"Database path is: {DB_PATH}")
print(f"Currency symbol is: {CURRENCY}")

app = Flask(__name__)

# In-memory transactions storage
transactions = []

# Helper functions
def calculate_income():
    return sum(t['amount'] for t in transactions if t['type'] == 'income')

def calculate_expense():
    return sum(t['amount'] for t in transactions if t['type'] == 'expense')

def calculate_tax():
    """Calculates total tax for all income transactions."""
    total_tax = 0
    for t in transactions:
        if t['type'] == 'income' and t['amount'] > 1200000:
            total_tax += (t['amount'] - 1200000) * 0.2
    return total_tax

def calculate_balance():
    return calculate_income() - calculate_expense() - calculate_tax()

# ✅ Home - Add Transaction
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        t_type = request.form['type']
        amount = float(request.form['amount'])
        category = request.form['category']

        # ✅ Tax logic applied during income entry
        tax = 0
        if t_type.lower() == "income":
            if amount > 1200000:
                tax = (amount - 1200000) * 0.2
            else:
                tax = 0

        transactions.append({
            'id': len(transactions) + 1,
            'type': t_type,
            'amount': amount,
            'category': category,
            'tax': tax,
            'date': datetime.now()
        })

        return redirect(url_for('dashboard'))

    return render_template(
        'index.html',
        transactions=transactions,
        income=calculate_income(),
        expense=calculate_expense(),
        tax=calculate_tax(),
        balance=calculate_balance(),
        currency=CURRENCY
    )

# ✅ Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template(
        'dashboard.html',
        transactions=transactions,
        income=calculate_income(),
        expense=calculate_expense(),
        tax=calculate_tax(),
        balance=calculate_balance(),
        currency=CURRENCY
    )

# ✅ Delete Transaction
@app.route('/delete_transaction/<int:tid>')
def delete_transaction(tid):
    global transactions
    transactions = [t for t in transactions if t['id'] != tid]
    # Reassign IDs after deletion
    for i, t in enumerate(transactions):
        t['id'] = i + 1
    return redirect(request.referrer or url_for('dashboard'))

# ✅ Reports
@app.route('/reports')
def reports():
    return render_template(
        'reports.html',
        transactions=transactions,
        income=calculate_income(),
        expense=calculate_expense(),
        tax=calculate_tax(),
        balance=calculate_balance(),
        currency=CURRENCY
    )

# ✅ Analytics
@app.route('/analytics')
def analytics():
    return render_template(
        'analytics.html',
        transactions=transactions,
        income=calculate_income(),
        expense=calculate_expense(),
        tax=calculate_tax(),
        balance=calculate_balance(),
        currency=CURRENCY
    )

# ✅ Settings
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    username = "User"
    if request.method == 'POST':
        username = request.form.get('username', 'User')
    return render_template('settings.html', username=username, currency=CURRENCY)

# ✅ Handle 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('oops.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
