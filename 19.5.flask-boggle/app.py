
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'veryHard'
app.debug = True

toolbar = DebugToolbarExtension(app)
game = Boggle()


@app.route('/')
def home_page():
    """Home page"""
    return render_template('home.html')

@app.route('/start')
def game_page():
    """Game page with timer and words"""
    session['board'] = game.make_board()
    return render_template('index.html')


@app.route('/check-valid-word')
def checking():
    """Checking world in the list"""
    word = request.args['word']
    board = session['board']
    response = game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route('/score', methods=['POST'])
def posting_score():
    """Can see score but if result reaches more then update for higher score. 
    Update number of games """
    score = request.json['score']
    bestScore = session.get('bestScore', 0)
    session['bestScore'] = max(score, bestScore)
    total_games = session.get('games', 0)
    session['games'] = total_games + 1
    return jsonify({'score': session['bestScore'], 'games': session['games']})