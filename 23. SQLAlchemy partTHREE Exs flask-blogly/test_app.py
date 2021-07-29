from unittest import TestCase
from app import app
from models import db, User, Post, Tag
from flask import Flask   
# from models import models

app = Flask(__name__)    
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTests(TestCase):

      def setUp(self):
        """Add sample user."""
        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url = "http:www/google.com", about_yourself="Happy me")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

      def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

      def test_redirection(self):
            with app.test_client() as client:
                  resp = client.get('/')
                  self.assertEqual(resp.status_code, 200)
                  self.assertEqual(resp.location, 'posts/postsPage.html')
      
      # def test_home(self):
      #       client = app.test_client()
      #       result = client.get('/')
      #       self.assertEqual(result.status_code, 200)

      def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

      def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

      def test_add_user(self):
        with app.test_client() as client:
            d = {'first_name': 'Alen', 'last_name': 'Strange', 'image_url': 'http:www/google.com', 'about_yourself': 'Happy funny dog'}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertNotEqual(resp.status_code, 200)
            self.assertIn("<h1>Alen Strange</h1>", html)

      def test_list_userss(self):
            '''Checks users page'''
            with app.test_client() as client:
                  res = client.get('/users')
                  html = res.get_data(as_text = True)
                  self.assertEqual(res.status_code, 200)
                  self.assertIn('<button class="btn"><a href="/users/new">Add New User</a></button>', html)

      def test_create_edit_user(self):
            '''Checks redirects and creation of new and edit user'''
            with app.test_client() as client:
                  res1 = client.post('/users/new', follow_redirects = True, data = {'first_name': 'Alen', 'last_name': 'Strange', 'image_url': 'http:www/google.com', 'about_yourself': 'Happy funny dog'})
                  html = res1.get_data(as_text = True)
                  self.assertEqual(res1.status_code, 200)
                  self.assertIn('<li class="list-group-item list-group-item-info">Alen Strange</li>', html)

                  res2 = client.post('/users/<int:user_id>/edit', follow_redirects = True, data = {'first_name': 'Alen', 'last_name': 'Gold', 'image_url': 'http:www/google.com', 'about_yourself': 'Sad not funny dog'})
                  html = res2.get_data(as_text = True)
                  self.assertEqual(res2.status_code, 200)
                  self.assertIn('<li class="list-group-item list-group-item-info">Alen Gold</li>', html)

      # def test_edit_user(self):
      #       res = self.client.post('/users/<int:user_id>/edit', follow_redirects = True, data = {'first_name': 'Alen', 'last_name': 'Silver', 'image_url': 'http:www/google.com', 'about_yourself': 'Sad not funny dog'})
      #       html = res.get_data(as_text = True)
      #       self.assertEqual(res.status_code, 200)
      #       self.assertIn('<li class="list-group-item list-group-item-info">Alen Strange</li>', html)
    