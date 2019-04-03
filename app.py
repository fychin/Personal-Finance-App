import sqlite3
import json
from flask import Flask, g, jsonify

DATABASE = './personalfinance.db'

app = Flask(__name__)

def make_dicts(cursor, row):
    """Dictionary row factory for query results
    """
    return dict((cursor.description[idx][0], value)
            for idx, value in enumerate(row))


def get_db():
    """Connect to sqlite db
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts 
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close db connection
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/accounts')
def get_accounts():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM accounts")
    rows = cur.fetchall()
    return jsonify(rows) 


@app.route('/transactions')
def get_txns():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    return jsonify(rows)


