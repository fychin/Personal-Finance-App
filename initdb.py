import os
import sqlite3

db_file = './personalfinance.db'

# Remove pre-existing .db file
if os.path.exists(db_file):
    os.remove(db_file)

# Create database
conn = sqlite3.connect(db_file)
cur = conn.cursor()

# Initialize database
sql_create_accounts_table = """CREATE TABLE accounts (
                                id INTEGER PRIMARY KEY, 
                                name TEXT NOT NULL,
                                balance REAL 
                            );"""

sql_create_txn_table = """CREATE TABLE transactions (
                            id INTEGER PRIMARY KEY,
                            type INTEGER NOT NULL,
                            title TEXT NOT NULL,
                            description TEXT,
                            account_id INTEGER NOT NULL,
                            FOREIGN KEY (account_id) REFERENCES accounts(id)
                       );"""

cur.execute(sql_create_accounts_table)
conn.commit()
cur.execute("INSERT INTO accounts VALUES(1, 'Cash', '322.50');")
cur.execute("INSERT INTO accounts VALUES(2, 'DBS Savings', '1250.86');")
conn.commit()

cur.execute(sql_create_txn_table)
conn.commit()
cur.execute("INSERT INTO transactions VALUES('1', '0', 'Food', 'Lunch', '1');")
cur.execute("INSERT INTO transactions VALUES('2', '1', 'Salary', 'March 19', '2');")
conn.commit()

conn.close()
