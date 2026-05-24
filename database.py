import sqlite3

conn = sqlite3.connect("finance.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL
)
""")

conn.commit()
conn.close()

print("Database created successfully")