import unittest
from app import app, db
from app.models import User, Account

class UserAccountModelCase(unittest.TestCase):
    def setUp(self):
        # use in-memory db for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='testUser')
        u.set_password('testpassword')
        self.assertFalse(u.check_password('differentpassword'))
        self.assertTrue(u.check_password('testpassword'))

    def test_create_accounts(self):
        # create 2 users
        u1 = User(username='testUser1')
        u2 = User(username='testUser2')
        db.session.add_all([u1, u2])
        db.session.commit()

        # create accounts for different users
        u1acc1 = Account(name='Cash', balance=2000.02)
        u1acc2 = Account(name='Savings')
        u1acc3 = Account(name='Stocks', balance=8231.49)
        u1.add_account(u1acc1)
        u1.add_account(u1acc2)
        u1.add_account(u1acc3)
        u2acc1 = Account(name='Bonds', balance=344.51)
        u2.add_account(u2acc1)
        db.session.commit()
        self.assertTrue(u1.get_num_accounts() == 3)
        self.assertTrue(u2.get_num_accounts() == 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)