"""Message View tests."""
# run these tests like:
#    FLASK_ENV=production python -m unittest test_message_views.py

import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser_id = 1212
        self.testuser.id = self.testuser_id
        db.session.commit()

        self.testuser_msg = Message(
                            text="be Cat", 
                            user_id=self.testuser.id)
        db.session.add(self.testuser_msg)
        db.session.commit()
        self.MSG = "MSG" #adding to session

    def test_add_message(self):
        """Can use add a message?"""
        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            resp = c.post("/messages/new", data={"text": "Hello"})
            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")
    
    
    def test_see_msg_authorized_users(self):
        msg = Message(
            id=1234,
            text="test users message",
            user_id=self.testuser.id
        )
        db.session.add(msg)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser.id

            msg = Message.query.get(1234)
            resp = client.get(f'/messages/{msg.id}')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(msg.text, str(resp.data))


    def test_see_invalid_msg(self):
        """Show messages from unauthorized user"""
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser.id
                session[self.MSG] = self.testuser_msg.id

            resp = client.get(f"/messages/{self.testuser_msg.id}") #get msg from view route
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200) #confirmation stats code and data
            self.assertIn(f'<p class="single-message">{self.testuser_msg.text}</p>', html)


    def test_msg_delete(self):
        """Show deleted messages route from authorzied user"""
        unauthorized = User.signup(username="unauthorizedUser",
                        email="test1test@test.com",
                        password="PASSWORD",
                        image_url=None)
        unauthorized.id = 3232

        #The authorized user msg:
        msg = Message(
            id=1234,
            text="test users message",
            user_id=self.testuser.id
        )
        db.session.add_all([unauthorized, msg])
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = unauthorized.id
            
            resp = client.post("/messages/1234/delete", follow_redirects=True) #This user is trying to delete authorized user msg
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))
            #Cheking if the msg was deleted, and show that msg contains data
            msg = Message.query.get(1234)
            self.assertIsNotNone(msg)

    def test_unauthorized_msg_delete(self):
        """Show unauthorized user delete msg"""
        with self.client as client: #Here user isn't in session
            resp = client.post(f"/messages/1234/delete")
            self.assertEqual(resp.status_code, 404)
            self.assertIn("Access unauthorized", str(resp.data))
