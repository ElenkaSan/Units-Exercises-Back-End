from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_greet(self):
        user = User(first_name="Test", last_name="Person", about_yourself="happy lol")
        self.assertEquals(user.greet(), "Hello. My name is Test Person. I can say about myself that happy lol")

