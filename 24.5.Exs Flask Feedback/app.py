from dataclasses import dataclass
from importlib.resources import contents
from turtle import pos
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, FeedbackForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "haha"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def redirect_to_register():
    return redirect('/register')

@app.route('/feedback')
def feedback_page():
    form = FeedbackForm()
    posts = Feedback.query.all()
    return render_template('feedback.html', form=form, posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        user = User.query.filter_by(username=new_user.username).first()

        flash('Welcome! Successfully Created Your Account!', "success")
        return render_template('username.html', user=user)

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "warning")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/users/<username>')
def secret_page(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.filter_by(username = username).first()
        posts = Feedback.query.filter_by(username = username).all()

        return render_template('username.html', user = user, posts = posts)
    

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    form = FeedbackForm()
    all_feedbacks = Feedback.query.all()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback Created!', 'success')

        user = session['username']
        return redirect(f'/users/{user}')

    return render_template("addFeedback.html", form=form, feedbacks=all_feedbacks)

@app.route('/feedback/<feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj = feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback Updated!', 'success')

        return redirect(f'/users/{feedback.username}')
   
    return render_template('editFeedback.html', form = form, feedback = feedback)


@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback"""
    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username== session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", "success")

        user = session['username']
        return redirect(f'/users/{user}')
    flash("You don't have permission to do that!", "danger")
    return redirect('/feedback')
