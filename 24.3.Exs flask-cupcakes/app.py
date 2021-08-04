"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template, redirect, flash, session
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'sweety'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/api/cupcakes')
def list_cupcake():
    """Returns JSON w/ all cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake_data(cupcake_id):
    """Return for a single cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""
    
    cupcake = Cupcake(
        flavor=request.json['flavor'],
        rating=request.json['rating'],
        size=request.json['size'],
        image=request.json['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_todo(cupcake_id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message='Deleted')
