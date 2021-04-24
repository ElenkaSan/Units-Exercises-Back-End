from flask import Flask, request, render_template
from stories import story
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "sayStory"
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Shows home page"""
    return render_template("home.html")

@app.route('/form')
def show_form():
    prompts = story.prompts
    return render_template("form.html", prompts=prompts) 

@app.route('/story')
def story_say():
    text =  story.generate(request.args)
    return render_template("story.html", text=text)
