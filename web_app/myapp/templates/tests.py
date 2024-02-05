from datetime import datetime, timedelta
import unittest
from myapp import app, db
from myapp.model import Writer, Student, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'database://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = Writer(username='name')
        u = Student(username='name')
        u.set_password('password')
        self.assertFalse(u.check_password('wrongpassword'))
        self.assertTrue(u.check_password('correctpassword'))

