# model.py
from config import DB_PATH, CURRENCY  # ✅ Added config import

import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np
from datetime import datetime, timedelta

# Optional: test prints for confirmation
print(f"Database path is: {DB_PATH}")
print(f"Currency symbol is: {CURRENCY}")

def fetch_transactions():
    """Fetch all transactions from SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT id, type, amount, category, date FROM transactions", conn
        )
    except Exception as e:
        print("Error fetching transactions:", e)
        df = pd.DataFrame(columns=['id', 'type', 'amount', 'category', 'date'])
    finally:
        conn.close()
    return df

def preprocess_data(df):
    """Prepare data for ML: encode categorical, convert date to ordinal"""
    if df.empty:
        return pd.DataFrame(), pd.Series(), None

    # Convert date to datetime safely
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Only use expense transactions for prediction
    df_expense = df[df['type'] == 'expense'].copy()
    df_expense = df_expense.dropna(subset=['date'])  # Remove invalid/missing dates
    if df_expense.empty:
        return pd.DataFrame(), pd.Series(), None

    # Encode category
    le = LabelEncoder()
    df_expense['category_encoded'] = le.fit_transform(df_expense['category'])

    # Convert date to ordinal safely
    X = pd.DataFrame({
        'date_ordinal': df_expense['date'].map(lambda x: x.toordinal()),
        'category_encoded': df_expense['category_encoded']
    })
    y = df_expense['amount']

    return X, y, le

def train_model():
    """Train linear regression model on past expenses"""
    df = fetch_transactions()
    X, y, le = preprocess_data(df)
    if X.empty or y.empty or le is None:
        print("No expense data available for training.")
        return None, None
    model = LinearRegression()
    model.fit(X, y)
    return model, le

def predict_future_expense(future_date_str, category, model, le):
    """Predict expense amount for a given future date and category"""
    if model is None or le is None:
        return 0

    future_date = datetime.strptime(future_date_str, '%Y-%m-%d')
    date_ord = pd.DataFrame(
        [[future_date.toordinal(), le.transform([category])[0]]],
        columns=['date_ordinal', 'category_encoded']
    )
    prediction = model.predict(date_ord)
    return max(prediction[0], 0)  # Ensure prediction is not negative

if __name__ == "__main__":
    # Example usage
    model, le = train_model()
    if model is not None:
        future_day = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        example_category = 'Food'  # Replace with actual category from your DB
        predicted = predict_future_expense(future_day, example_category, model, le)
        print(f"Predicted expense for {example_category} on {future_day}: {CURRENCY}{predicted:.2f}")
    else:
        print("No model trained due to lack of expense data.")
