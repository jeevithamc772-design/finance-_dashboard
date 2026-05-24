import streamlit as st
import sqlite3

st.title("Income Tracker")

source = st.text_input("Income Source")

amount = st.number_input("Income Amount")

if st.button("Save Income"):

    conn = sqlite3.connect("finance.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO income(source, amount) VALUES (?, ?)",
        (source, amount)
    )

    conn.commit()
    conn.close()

    st.success("Income Saved Successfully")

st.subheader("Saved Incomes")

conn = sqlite3.connect("finance.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM income")

data = cursor.fetchall()

conn.close()

for row in data:
    st.write(row)