"""User model tests."""
# run these tests like:
# python -m unittest test_user_model.py

import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
# Now we can import app
from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.test1 = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1",
            image_url = None
        )
        self.test1_id = 1010
        self.test1.id = self.test1_id 

        self.test2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2",
            image_url = None
        )
        self.test2_id = 2020
        self.test2.id = self.test2_id 

        db.session.commit()
        self.client = app.test_client()

    def teardown(self):
        """Will clean up after each test run"""
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    def test_user_follow_model(self):
        self.test1.following.append(self.test2) # checks that user1 following user2
        db.session.commit()
        # check if user1 is following then user2 
        self.assertEqual(len(self.test1.following), 1) #following list = 1
        self.assertEqual(len(self.test2.following), 0) #following list = 0
       
        # check if user1 is being followed then user2 
        self.assertEqual(len(self.test1.followers), 0) #followed list = 0
        self.assertEqual(len(self.test2.followers), 1) #followed list = 1

        # check following one user
        self.assertEqual(self.test1.following[0].id, self.test2.id)
        # check one follower
        self.assertEqual(self.test2.followers[0].id, self.test1.id)
        

    def test_is_following(self):
        self.test1.following.append(self.test2)
        db.session.commit()
       
        self.assertTrue(self.test1.is_following(self.test2)) #testing if user1 is following user2
        self.assertFalse(self.test2.is_following(self.test1)) #not following 

    def test_is_followed_by(self):
        self.test1.following.append(self.test2)
        db.session.commit()

        self.assertTrue(self.test2.is_followed_by(self.test1)) #being followed
        self.assertFalse(self.test1.is_followed_by(self.test2)) #not being followed



    def test_valid_signup(self):
        user_test = User.query.filter_by(username=self.test1.username).first() #find user1 from DB
        
        # confirm user is available, matches created user, created email, not correct password:
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, "testuser1")
        self.assertEqual(user_test.email, "test1@test.com")
        self.assertNotEqual(user_test.password, "qwertyuiop")
        self.assertTrue(user_test.password.startswith("$2b$")) #cheking bcrypt strings should start with $2b$

    def test_invalid_signup(self):
        invalid_username_other = User.signup("lollol", None, "PASSWORD", None)
        user_id = 10102020
        invalid_username_other.id = user_id
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_invalid_email_signup(self):
        wrong_email = User.signup("testuser", None, "PASSWORD", None)
        user_id = 10102020
        wrong_email.id = user_id
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError):
            User.signup("testuser", "testuser@test.com", None, None)
        with self.assertRaises(ValueError):
            User.signup("testuser", "testuser@test.com", "", None)



    def test_valid_authentication(self):
        user = User.query.get(self.test1_id) #Get user info from DB
        create1 = User.authenticate(self.test1.username, "HASHED_PASSWORD1")
        self.assertIsNotNone(create1) #confirm user exists (checking with not none)
        self.assertEqual(user, create1)  #test if user id created equals original user id

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "HASHED_PASSWORD1"))

    def test_invalid_password(self):
        self.assertFalse(User.authenticate(self.test1.username, "PASSWORD"))
