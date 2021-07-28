"""Blogly application."""
from importlib.resources import contents
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "myBrain"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/postsPage.html', posts=posts)

@app.route('/users')
def list_users():
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users/list.html', users=users)

@app.route('/users/new',  methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':
        return render_template('users/addUser.html')

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None
        about_yourself = request.form['about_yourself']
    
        new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url, about_yourself=about_yourself)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')

@app.route('/users/<int:user_id>')
def user_page(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template('users/details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_page_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/editUser.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    user.about_yourself = request.form['about_yourself']

    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=['POST', 'GET'])
def posts_new(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        return render_template('posts/addPost.html', user=user)
    
    elif request.method == 'POST':
        user = User.query.get_or_404(user_id)
        title=request.form['title']
        content=request.form['content']
                    
        new_post = Post(title=title, content=content, user=user)

        db.session.add(new_post)
        db.session.commit()
      
        return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_page(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)
    return render_template('posts/postDetails.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)
    return render_template('posts/editPost.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def posts_destroy(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
