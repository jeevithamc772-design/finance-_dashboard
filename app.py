import streamlit as st
import sqlite3
import pandas as pd

# =========================
# INCOME TRACKER
# =========================

st.title("Income Tracker")

source = st.text_input("Income Source")

frequency = st.selectbox(
    "Frequency",
    ["Daily", "Weekly", "Monthly", "Yearly"]
)

amount = st.number_input(
    "Income Amount",
    min_value=0.0
)


if st.button("Save Income"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO income(source, amount, frequency)
    VALUES (?, ?, ?)
    """,
    (source, amount, frequency)
)

    conn.commit()
    conn.close()

    st.success("Income Saved Successfully")

# Display Income Records

st.subheader("Saved Incomes")

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM income")

data = cursor.fetchall()

conn.close()

income_df = pd.DataFrame(
    data,
    columns=["ID", "Source", "Amount", "Frequency"]
)

st.dataframe(income_df)

#delete income
st.subheader("Delete Income")

income_id = st.number_input(
    "Enter Income ID to Delete",
    min_value=1,
    step=1,
    key="delete_income"
)

if st.button("Delete Income"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM income WHERE id = ?",
        (income_id,)
    )

    conn.commit()
    conn.close()

    st.success("Income Deleted Successfully")

#update income

st.subheader("Update Income")

update_income_id = st.number_input(
    "Income ID",
    min_value=1,
    step=1,
    key="update_income_id"
)

new_source = st.text_input(
    "New Source",
    key="new_source"
)

new_frequency = st.selectbox(
    "New Frequency",
    ["Daily", "Weekly", "Monthly", "Yearly"],
    key="update_frequency"
)

new_amount = st.number_input(
    "Additional Amount",
    min_value=0.0,
    key="new_amount"
)

if st.button("Update Income"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
    """
    UPDATE income
    SET source=?,
        frequency=?,
        amount = ?
    WHERE id=?
    """,
    (
        new_source,
        new_frequency,
        new_amount,
        update_income_id
    )
)
    conn.commit()
    conn.close()

    st.success("Income Updated Successfully")

# Calculate Total Income

total_income = sum(row[2] for row in data)

# =========================
# EXPENSE TRACKER
# =========================

st.title("Expense Tracker")

category = st.text_input("Expense Category")

expense_type = st.selectbox(
    "Expense Type",
    ["Fixed", "Variable"]
)

expense_date = st.date_input(
    "Expense Date"
)

expense_amount = st.number_input(
    "Expense Amount",
    min_value=0.0
)

if st.button("Save Expense"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO expense(category, amount, type, date)
    VALUES (?, ?, ?, ?)
    """,
    (
        category,
        expense_amount,
        expense_type,
        str(expense_date)
    )
)

    conn.commit()
    conn.close()

    st.success("Expense Saved Successfully")

# Display Expense Records

st.subheader("Saved Expenses")

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM expense")

expenses = cursor.fetchall()

expense_summary = {}

for row in expenses:
    category = row[1]
    amount = row[2]

    if category in expense_summary:
        expense_summary[category] += amount
    else:
        expense_summary[category] = amount

conn.close()

expense_df = pd.DataFrame(
    expenses,
    columns=[
        "ID",
        "Category",
        "Amount",
        "Type",
        "Date"
    ]
)


expense_chart_df = pd.DataFrame(
    {
        "Amount": list(expense_summary.values())
    },
    index=list(expense_summary.keys())
)
st.dataframe(expense_df)

#delete expense
st.subheader("Delete Expense")

expense_id = st.number_input(
    "Enter Expense ID to Delete",
    min_value=1,
    step=1,
    key="delete_expense"
)

if st.button("Delete Expense"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expense WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    st.success("Expense Deleted Successfully")

#update expence
 # =========================
# UPDATE EXPENSE
# =========================

st.subheader("Update Expense")

update_expense_id = st.number_input(
    "Expense ID",
    min_value=1,
    step=1,
    key="update_expense_id"
)

new_category = st.text_input(
    "New Category",
    key="new_category"
)

new_type = st.selectbox(
    "New Expense Type",
    ["Fixed", "Variable"],
    key="new_type"
)

new_date = st.date_input(
    "New Expense Date",
    key="new_date"
)

new_expense_amount = st.number_input(
    "New Expense Amount",
    min_value=0.0,
    key="new_expense_amount"
)

if st.button("Update Expense"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE expense
        SET category=?,
            type=?,
            date=?,
            amount=?
        WHERE id=?
        """,
        (
            new_category,
            new_type,
            str(new_date),
            new_expense_amount,
            update_expense_id
        )
    )

    conn.commit()
    conn.close()

    st.success("Expense Updated Successfully")

# Calculate Total Expense

total_expense = sum(row[2] for row in expenses)

# =========================
# SAVINGS DASHBOARD
# =========================

savings = total_income - total_expense

chart_data = pd.DataFrame(
    {
        "Amount": [
            total_income,
            total_expense,
            savings
        ]
    },
    index=[
        "Income",
        "Expense",
        "Savings"
    ]
)


st.subheader("Monthly Expense Tracking")

selected_month = st.selectbox(
    "Select Month",
    [
        "01","02","03","04","05","06",
        "07","08","09","10","11","12"
    ]
)

selected_year = st.text_input(
    "Enter Year",
    value="2026"
)


monthly_expenses = []

for row in expenses:

    expense_date = row[4]

    if expense_date.startswith(
        f"{selected_year}-{selected_month}"
    ):
        monthly_expenses.append(row)


monthly_df = pd.DataFrame(
    monthly_expenses,
    columns=[
        "ID",
        "Category",
        "Amount",
        "Type",
        "Date"
    ]
)

st.dataframe(monthly_df)


monthly_total = 0

for row in monthly_expenses:
    monthly_total += row[2]

st.metric(
    "Monthly Expense",
    f"₹ {monthly_total:,.2f}"
)
# =========================
# LOAN MANAGEMENT
# =========================

st.title("Loan Management")

loan_type = st.selectbox(
    "Loan Type",
    ["Home", "Personal", "Car"]
)

total_loan_amount = st.number_input(
    "Total Loan Amount",
    min_value=0.0,
    key="loan_amount"
)

emi_amount = st.number_input(
    "EMI Amount",
    min_value=0.0,
    key="emi_amount"
)

interest_rate = st.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    key="interest_rate"
)

tenure = st.number_input(
    "Tenure (Months)",
    min_value=1,
    step=1,
    key="tenure"
)

if st.button("Save Loan"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO loan(
            loan_type,
            total_amount,
            emi_amount,
            interest_rate,
            tenure,
            remaining_balance
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            loan_type,
            total_loan_amount,
            emi_amount,
            interest_rate,
            tenure,
            total_loan_amount
        )
    )

    conn.commit()
    conn.close()

    st.success("Loan Saved Successfully")


#display loans
st.subheader("Saved Loans")

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM loan")

loans = cursor.fetchall()

conn.close()

loan_df = pd.DataFrame(
    loans,
    columns=[
        "ID",
        "Loan Type",
        "Total Amount",
        "EMI Amount",
        "Interest Rate",
        "Tenure",
        "Remaining Balance"
    ]
)

st.dataframe(loan_df)


# =========================
# PAY EMI
# =========================

st.subheader("Pay EMI")

loan_id = st.number_input(
    "Loan ID",
    min_value=1,
    step=1,
    key="loan_id"
)

emi_paid = st.number_input(
    "EMI Paid",
    min_value=0.0,
    key="emi_paid"
)

if st.button("Pay EMI"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
    """
    UPDATE loan
    SET remaining_balance =
        CASE
            WHEN remaining_balance - ? < 0
            THEN 0
            ELSE remaining_balance - ?
        END
    WHERE id = ?
    """,
    (
        emi_paid,
        emi_paid,
        loan_id
    )
)

    conn.commit()
    conn.close()

    st.success("EMI Payment Recorded")


# =========================
# SAVINGS MANAGEMENT
# =========================

st.title("Savings Management")

savings_type = st.selectbox(
    "Savings Type",
    ["Short-Term", "Long-Term"]
)

purpose = st.text_input(
    "Purpose"
)

target_amount = st.number_input(
    "Target Amount",
    min_value=0.0,
    key="target_amount"
)

timeline = st.text_input(
    "Timeline",
    placeholder="e.g. 6 Months, 1 Year"
)

if st.button("Save Savings Goal"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO savings(
            savings_type,
            purpose,
            target_amount,
            timeline
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            savings_type,
            purpose,
            target_amount,
            timeline
        )
    )

    conn.commit()
    conn.close()

    st.success("Savings Goal Saved Successfully")

#display savings amount

st.subheader("Saved Savings Goals")

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM savings")

savings_data = cursor.fetchall()

conn.close()

savings_df = pd.DataFrame(
    savings_data,
    columns=[
        "ID",
        "Savings Type",
        "Purpose",
        "Target Amount",
        "Timeline"
    ]
)

st.dataframe(savings_df)



# =========================
# INVESTMENT TRACKING
# =========================

st.title("Investment Tracking")

investment_type = st.selectbox(
    "Investment Type",
    ["Stocks", "Mutual Funds", "Fixed Deposits"]
)

invested_amount = st.number_input(
    "Invested Amount",
    min_value=0.0,
    key="invested_amount"
)

current_value = st.number_input(
    "Current Value",
    min_value=0.0,
    key="current_value"
)

returns = current_value - invested_amount

if st.button("Save Investment"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO investment(
            investment_type,
            invested_amount,
            current_value,
            returns
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            investment_type,
            invested_amount,
            current_value,
            returns
        )
    )

    conn.commit()
    conn.close()

    st.success("Investment Saved Successfully")

    #display investement

st.subheader("Saved Investments")

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM investment")

investments = cursor.fetchall()

conn.close()

investment_df = pd.DataFrame(
    investments,
    columns=[
        "ID",
        "Investment Type",
        "Invested Amount",
        "Current Value",
        "Returns"
    ]
)

st.dataframe(investment_df)

# =========================
# MONTHLY PAYMENT TRACKER
# =========================

st.title("Monthly Payment Tracker")

payment_type = st.selectbox(
    "Payment Type",
    ["EMI", "Subscription", "Bill"]
)

description = st.text_input(
    "Description"
)

amount = st.number_input(
    "Amount",
    min_value=0.0,
    key="payment_amount"
)

due_date = st.date_input(
    "Due Date",
    key="due_date"
)

status = st.selectbox(
    "Status",
    ["Pending", "Paid"]
)

if st.button("Save Payment"):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO payment(
            payment_type,
            description,
            amount,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payment_type,
            description,
            amount,
            str(due_date),
            status
        )
    )

    conn.commit()
    conn.close()

    st.success("Payment Saved Successfully")

# display payments
st.subheader("Saved Payments")

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM payment")

payments = cursor.fetchall()

conn.close()

payment_df = pd.DataFrame(
    payments,
    columns=[
        "ID",
        "Payment Type",
        "Description",
        "Amount",
        "Due Date",
        "Status"
    ]
)

st.dataframe(payment_df)



#financial summery

st.subheader("Financial Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Income", f"₹ {total_income:,.2f}")

with col2:
    st.metric("Total Expense", f"₹ {total_expense:,.2f}")

with col3:
    st.metric("Savings", f"₹ {savings:,.2f}")
st.subheader("Financial Overview")

st.bar_chart(chart_data)

st.subheader("Expense Category Analysis")

st.bar_chart(expense_chart_df)

