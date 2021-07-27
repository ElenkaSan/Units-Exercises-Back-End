"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
photo_url = "https://www.freeiconspng.com/uploads/computer-user-icon-21.png"

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
   __tablename__ = 'users' 

   id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

   first_name = db.Column(db.String(50),
                     nullable=False)

   last_name = db.Column(db.String(50),
                     nullable=False)

   image_url = db.Column(db.Text, 
                     default=photo_url,
                     nullable=False)

   about_yourself = db.Column(db.Text, 
                     nullable=False)

   @property
   def full_name(self):
       return f"{self.first_name} {self.last_name}"

   def greet(self):
       return f"Hello. My name is {self.first_name} {self.last_name}. I can say about myself that {self.about_yourself}"
    
