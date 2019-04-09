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
sql_create_users_table = """CREATE TABLE users (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT NOT NULL UNIQUE,
                             password TEXT NOT NULL,
                             email TEXT,
                             role TEXT CHECK( role IN ('admin','user') ) NOT NULL DEFAULT 'user'
                         );"""

sql_create_accounts_table = """CREATE TABLE accounts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                name TEXT NOT NULL,
                                balance REAL 
                            );"""

sql_create_txn_table = """CREATE TABLE transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            type TEXT CHECK( type IN ( 'expense','income' ) ) NOT NULL,
                            title TEXT NOT NULL,
                            description TEXT,
                            account_id INTEGER NOT NULL,
                            FOREIGN KEY (account_id) REFERENCES accounts(id)
                       );"""

cur.execute(sql_create_users_table)
cur.execute("INSERT INTO users (name,password,email,role) VALUES('admin', 'admin', 'admin@email.com', 'admin');")
conn.commit()

cur.execute(sql_create_accounts_table)
cur.execute("INSERT INTO accounts (name,balance) VALUES('Cash', '322.50');")
cur.execute("INSERT INTO accounts (name,balance) VALUES('DBS Savings', '1250.86');")
conn.commit()

cur.execute(sql_create_txn_table)
cur.execute("INSERT INTO transactions (type,title,description,account_id) VALUES('expense', 'Food', 'Lunch', 1);")
cur.execute("INSERT INTO transactions (type,title,description,account_id) VALUES('income', 'Salary', 'March 19', 2);")
conn.commit()

conn.close()
