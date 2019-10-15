from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    # override table name to users for postgresql
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(20))
    role = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    accounts = db.relationship('Account', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_account(self, account):
        self.accounts.append(account)

    def get_num_accounts(self):
        return self.accounts.filter(User.id == self.id).count()

    def __repr__(self):
        return '<User {}>'.format(self.username)


# Flask-Login session management
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def __repr__(self):
        return '<Account {}, {}>'.format(self.name, self.balance)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    type_id = db.Column(db.Integer, db.ForeignKey('transaction_type.id'), nullable=False)
    amount = db.Column(db.Float)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
 
    def __repr__(self):
        return '<Transaction #{} - Acc: {}, {}>'.format(self.type_id, self.account_id, self.title)


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return '<User Role: {}>'.format(self.name)
    

class TransactionType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return '<Transaction Type: {}>'.format(self.name)
    
