import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

# Income Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    amount REAL,
    frequency TEXT
)
""")

# Expense Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount REAL,
    type TEXT,
    date TEXT
)
""")

# Loan Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS loan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_type TEXT,
    total_amount REAL,
    emi_amount REAL,
    interest_rate REAL,
    tenure INTEGER,
    remaining_balance REAL
)
""")
#savings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS savings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    savings_type TEXT,
    purpose TEXT,
    target_amount REAL,
    timeline TEXT
)
""")
#investment table
cursor.execute("""
CREATE TABLE IF NOT EXISTS investment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investment_type TEXT,
    invested_amount REAL,
    current_value REAL,
    returns REAL
)
""")
#payment table
cursor.execute("""
CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_type TEXT,
    description TEXT,
    amount REAL,
    due_date TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")