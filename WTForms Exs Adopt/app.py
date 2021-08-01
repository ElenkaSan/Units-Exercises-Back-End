from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Pet
from forms import PetForm, EditPetForm 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    pets = Pet.query.order_by(Pet.name).all()
    return render_template("home.html", pets = pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Renders pet form (GET) or handles pet form submission (POST)"""
    form = PetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data
        
        new_pet = Pet(name = name, species = species, photo_url = photo_url, age = age, notes = notes, available = available)
        db.session.add(new_pet)
        db.session.commit()
        
        flash(f"Created new pet: name is {name}, species is {species}")
        return redirect('/')
    else:
        return render_template('addPet.html', form = form)


@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj = pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash(f"You made pet update!")
        return redirect('/')

    else:
        return render_template('editPet.html', form = form, pet = pet)


@app.route('/<int:pet_id>/delete', methods=['POST'])
def delete_user(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    db.session.delete(pet)
    db.session.commit()
    flash(f"You delete pet {pet.name}!")
    return redirect('/')