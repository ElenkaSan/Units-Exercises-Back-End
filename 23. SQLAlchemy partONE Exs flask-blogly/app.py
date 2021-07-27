"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "myBrain"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
# toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect("/users")

@app.route('/users')
def list_users():
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users/list.html', users=users)

@app.route('/users/new',  methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':
        return render_template('users/addUser.html')

    elif request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"] or None
        about_yourself = request.form["about_yourself"]
    
        new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url, about_yourself=about_yourself)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")

@app.route("/users/<int:user_id>")
def user_page(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_page_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/editUser.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    user.about_yourself = request.form["about_yourself"]

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")
