from app import app, db
from app.models import User, Account, Transaction, UserRole, TransactionType
from flask.cli import with_appcontext

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Account': Account}

@app.cli.command(with_appcontext=True)
def seed():
    """Seed database with admin user, initial accounts"""
    # Create roles
    user_role = UserRole(role='User')
    admin_role = UserRole(role='Admin')
    db.session.add_all([user_role, admin_role])
    db.session.commit()
    
    # Create admin user
    admin_user = User(username='admin', role=2, email='fyang.chin@gmail.com')
    admin_user.set_password('admin')
    db.session.add(admin_user)

    # Create accounts
    cash_acc = Account(name='Cash', balance=263.02)
    bank_acc = Account(name='Bank', balance=4521.66)
    admin_user.add_account(cash_acc)
    admin_user.add_account(bank_acc)
    db.session.commit()

    print('database seeded...')
