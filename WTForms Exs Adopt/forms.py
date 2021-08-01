"""Forms for our demo Flask app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, Length, URL, NumberRange

class PetForm(FlaskForm):
    name = StringField('Name', validators = [InputRequired(message = 'Name is required')])
    species = SelectField('Species', choices = [('cat','cat'), ('dog', 'dog'), ('porcupine', 'porcupine')])
    photo_url = StringField('Photo URL', validators = [Optional(), URL()]) 
    age = IntegerField('Age', validators = [Optional(), NumberRange(min = 0, max = 30, message = 'Age must be between 0 and 30') ]) 
    notes = TextAreaField('Comments', validators = [Optional(), Length(min=10)])
    available = SelectField('Available', choices = [('YES','YES'), ('no', 'no')])

class EditPetForm(FlaskForm):
    photo_url = StringField('Photo URL', validators = [Optional(), URL(require_tld = False)]) 
    notes = TextAreaField('Comments', validators = [Optional(), Length(min=10)])
    available = SelectField('Available', choices = [('YES','YES'), ('no', 'no')])