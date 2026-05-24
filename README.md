# Personal Finance Dashboard

## Overview

Personal Finance Dashboard is a beginner-friendly finance management application built using Python, Streamlit, and SQLite.

Currently, the project includes the Income Management module, which allows users to:

* Enter income amounts
* Save income records
* Store data in SQLite database
* View saved income records

---

## Technologies Used

* Python
* Streamlit
* SQLite

---

## Project Structure

```text
finance_dashboard/
│
├── app.py
├── database.py
├── finance.db
└── README.md
```

---

## Features Implemented

### Income Tracker

* User can enter income amount
* User can save income using a button
* Income is stored in SQLite database
* Saved incomes are displayed on the screen

---

## Database Setup

### Create Database

Run:

```bash
python database.py
```

Output:

```text
Database created successfully
```

This creates:

```text
finance.db
```

---

## Running the Application

### Install Streamlit

```bash
pip install streamlit
```

### Run Streamlit Application

```bash
streamlit run app.py
```

After running, Streamlit will provide a URL similar to:

```text
http://localhost:8501
```

Open it in a browser.

---

## Current Workflow

```text
User Input
    ↓
Streamlit Form
    ↓
Python Logic
    ↓
SQLite Database
    ↓
Display Saved Records
```

---

## CRUD Progress

### Create (Completed)

* Save income records into database

### Read (Completed)

* Display saved income records

### Update

* Not implemented yet

### Delete

* Not implemented yet

---

## Sample Output

```text
Income Tracker

Enter Income

30000

Income Saved Successfully

Saved Incomes

(1, 30000.0)
(2, 25000.0)
```


##Commands you've used so far

Create database:

python database.py

Run application:

streamlit run app.py

Stop Streamlit server:

Ctrl + C

---

## Author

Jeevitha M C
MCA Graduate
