from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message = 'Username is required')])
    password = PasswordField("Password", validators=[InputRequired(message = 'Password is required')])
    email = StringField("Email", validators=[InputRequired(message = 'Email is required')])
    first_name = StringField("Your first name", validators=[InputRequired(message= 'First name is required')])
    last_name = StringField("Your last name", validators=[InputRequired(message= 'Last name is required')])


class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message = 'Title is required.')])
    content = StringField("Feedback Text", validators=[InputRequired(message = 'Content is required.')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(message = 'Username is required')])
    password = PasswordField('Password', validators = [InputRequired(message = 'Password is required')])