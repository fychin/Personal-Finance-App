import sqlite3
import json
from flask import Flask, g, jsonify, make_response, render_template
from flask_httpauth import HTTPBasicAuth 

DATABASE = './personalfinance.db'

app = Flask(__name__)
auth = HTTPBasicAuth()

def make_dicts(cursor, row):
    """Dictionary row factory for query results"""
    return dict((cursor.description[idx][0], value)
            for idx, value in enumerate(row))


def get_db():
    """Connect to sqlite db"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts 
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close db connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# User Authentication
@auth.get_password
def get_password(username):
    cur = get_db().cursor()
    cur.execute("SELECT password FROM users WHERE name=?", (username,))
    password = cur.fetchone()['password']
    return password
 

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# Render Templates
@app.route('/')
@auth.login_required
def home():
    cur = get_db().cursor()
    cur.execute("SELECT name FROM users")
    user = cur.fetchone()['name']
    return render_template('index.html', data=user)
    

# RESTful API
@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return jsonify(rows)


@app.route('/accounts', methods=['GET'])
def get_accounts():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM accounts")
    rows = cur.fetchall()
    return jsonify(rows) 


@app.route('/transactions', methods=['GET'])
def get_transactions():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True)
