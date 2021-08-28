"""Message View tests."""
# run these tests like:
#    FLASK_ENV=production python -m unittest test_user_views.py

import os
from unittest import TestCase
from models import db, connect_db, User, Message, Follows, Likes
from app import app, CURR_USER_KEY, g

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

class UserViewTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.test1 = User.signup(
            email="test1@test.com",
            username="testusername1",
            password="HASHED_PASSWORD1",
            image_url = None
        )
        self.test1_id = 1010
        self.test1.id = self.test1_id 

        self.test2 = User.signup(
            email="test2@test.com",
            username="testusername2",
            password="HASHED_PASSWORD2",
            image_url = None
        )
        self.test2_id = 2020
        self.test2.id = self.test2_id 

        self.test3 = User.signup(
            email="test3@test.com",
            username="testusername3",
            password="HASHED_PASSWORD3",
            image_url = None
        )
        self.test3_id = 3030
        self.test3.id = self.test3_id 

        db.session.commit()

        #Making followers and test message likes:
        follow1 = self.test1.following.append(self.test3)
        follow2 = self.test2.following.append(self.test1)
        follow3 = self.test3.following.append(self.test2)

        db.session.add_all([follow1,follow2,follow3])
        db.session.commit()

        msg1 = Message(id=1111, text='happy me', user_id=self.test2.id)
        msg2 = Message(id=2222, text='be greatfull', user_id=self.test1.id)
        db.session.add_all([msg1, msg2])
        db.session.commit()

        like1 = Likes(user_id=self.test1_id, message_id=1111)
        db.session.add(like1)
        db.session.commit()
        
    def teardown(self):
        """Will clean up after each test run"""
        # resp = super().tearDown()
        db.session.rollback()
        # return resp

    def test_signup(self):
        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>I'm here first time</h1>", html)
            self.assertIn("<h1>I have one account</h1>", html)


    def test_login_get_request(self):
        with self.client as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="join-message">Happy to see you again</h1>', html)


    def test_show_users_route(self):
        with self.client as client:
            resp = client.get("/users")

            self.assertIn("@testusername1", str(resp.data))
            self.assertIn("@testusername2", str(resp.data))
            self.assertIn("@test3dad", str(resp.data))

    def test_show_user_detail(self):
        with self.client as client:
            resp = client.get(f"/users/{self.test1_id}")
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testusername1", str(resp.data))

    def test_user_following_route(self):
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.test1.id

            resp = client.get(f"/users/{self.test1_id}/followers")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testusername1", str(resp.data))

        with self.client as client:
            res = client.get(f"users/{self.test1_id}/followers") # user not in session
            self.assertLessEqual(res.status_code, 302)
            self.assertIn("@testusername1", str(res.data))

    def test_user_followers_route(self):
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.test2.id
            resp = client.get(f'users/{self.test2_id}/followers')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testusername2", str(resp.data))


    def test_being_follow_user(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test1.id
            resp = client.post(f'users/follow/{self.test1.id}')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'http://localhost/users/{self.test1_id}/following')
    
    def test_unauthorized_following_page_access(self):
         with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test1.id
            resp = client.get(f"/users/{self.test1_id}/following", follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("@test3dad", str(resp.data))
            self.assertIn("Access unauthorized", str(resp.data))

    def test_show_add_like(self):
        # msg2 = Message(id=2222, text='be greatfull', user_id=self.test1.id)
        # db.session.add(msg2)
        # db.session.commit()
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.test1_id

            res = client.post("/messages/2222/like", follow_redirects=True)
            self.assertEqual(res.status_code, 200)

    def test_show_remove_like(self):
        msg = Message.query.filter(Message.text=="Enjoing life").one()
        self.assertIsNotNone(msg)
        self.assertNotEqual(msg.user_id, self.test2_id)

        like = Likes.query.filter(
            Likes.user_id==self.test1_id and Likes.message_id==msg.id).one()
        self.assertIsNotNone(like)

        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.test2_id

            resp = client.post(f"/messages/{msg.id}/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200) 

            likes = Likes.query.filter(Likes.message_id==msg.id).all()
            self.assertEqual(len(likes), 0) #can see 0 likes, was deleted
    
    def test_logout_route(self):
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.test2.id

            resp = client.get("/logout")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/')
            