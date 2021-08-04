"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

photo = "https://tinyurl.com/demo-cupcake"

def connect_db(app):
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
   __tablename__ = 'cupcakes' 

   id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

   flavor = db.Column(db.Text,
                     nullable=False)

   size = db.Column(db.Text,
                     nullable=False)
                     
   rating = db.Column(db.Float, 
                     nullable=False)

   image = db.Column(db.Text, 
                     default=photo,
                     nullable=False)


   def serialize(self):
        """Returns a dict representation of cupcakes which we can turn into JSON"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'rating': self.rating,
            'size': self.size,
            'image': self.image,
        }