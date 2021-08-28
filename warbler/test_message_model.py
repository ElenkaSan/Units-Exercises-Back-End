"""Msg model tests."""
# run these tests like:
# python -m unittest test_message_model.py

import os
from unittest import TestCase
from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app
# python -m unittest test_message_model.py

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.test = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1",
            image_url = None
        )

        self.test_id = 1010
        self.test.id = self.test_id

        self.test1 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2",
            image_url = None
        )

        self.test1_id = 2020
        self.test1.id = self.test1_id

        db.session.commit()

        self.test = User.query.get(self.test_id)
        self.test1 = User.query.get(self.test1_id)
        self.client = app.test_client()

    def teardown(self):
        """Will clean up after each test run"""
        db.session.rollback()

    def test_msg_model(self):
        """Does basic model work?"""

        msg = Message(
            text="happy me",
            user_id=self.test_id
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.test.messages), 1) #check length of list == 1
        self.assertEqual(self.test.messages[0].text, "happy me") #show msg text
        self.assertIn(msg, self.test.messages) #test if there is data in msgs

    def test_create_new_msg(self):
        msg = Message(text='happy me', user_id=self.test.id)
        db.session.commit()

        self.test.messages.append(msg) 
        self.assertIn(msg, self.test.messages) #test if data exists in messages

    def test_like_msg(self):
        # create new messages for both users
        msg1 = Message(
               text='happy me', 
               user_id=self.test.id
        )
        msg2 = Message(
               text='please be relax', 
               user_id=self.test1.id
        )
        db.session.commit()


        self.test1.likes.append(msg1) 
        self.test.likes.append(msg2) 
        self.assertIn(msg1, self.test1.likes) 
        self.assertIn(msg2, self.test.likes) 

        self.test1.likes.remove(msg1)
        self.test.likes.remove(msg2) 
        self.assertNotIn(msg1, self.test1.likes)
        self.assertNotIn(msg2, self.test.likes)
