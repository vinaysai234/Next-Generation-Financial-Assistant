# ai_assistant.py
import sqlite3
import pandas as pd
from config import DB_PATH, CURRENCY

def fetch_transactions():
    """Fetch all transactions from SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT type, amount, category, date FROM transactions", conn)
    except Exception as e:
        print("Error fetching transactions:", e)
        df = pd.DataFrame(columns=['type', 'amount', 'category', 'date'])
    finally:
        conn.close()
    return df

def generate_tips():
    """Generate smart saving/spending tips"""
    df = fetch_transactions()
    if df.empty:
        return ["No transactions available. Start adding transactions to get personalized tips!"]

    tips = []

    # Total income and expense
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()
    
    if total_income > 0:
        savings_ratio = (total_income - total_expense) / total_income
        if savings_ratio < 0.2:
            tips.append(f"Your savings ratio is low. Try to save at least 20% of your income ({CURRENCY}{int(total_income * 0.2)}).")
        else:
            tips.append("Good job! Your savings ratio is healthy.")

    # Most expensive category
    expenses = df[df['type'] == 'expense']
    if not expenses.empty:
        expense_by_category = expenses.groupby('category')['amount'].sum()
        max_category = expense_by_category.idxmax()
        tips.append(f"You're spending the most on {max_category}. Consider reviewing this category.")

    # Least income source
    incomes = df[df['type'] == 'income']
    if not incomes.empty:
        income_by_category = incomes.groupby('category')['amount'].sum()
        min_category = income_by_category.idxmin()
        tips.append(f"Your least income is from {min_category}. Explore ways to boost this source.")

    # Suggest cutting small unnecessary expenses
    small_expenses = expenses[expenses['amount'] < 500]
    if not small_expenses.empty:
        tips.append(f"You have multiple small expenses under {CURRENCY}500. Cutting a few can increase your savings.")

    return tips

if __name__ == "__main__":
    tips = generate_tips()
    print("\n💡 AI Assistant Tips:")
    for idx, tip in enumerate(tips, 1):
        print(f"{idx}. {tip}")
