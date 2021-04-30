from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "anything"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Shows home page"""
    return render_template('surveyPage.html', survey=survey)

@app.route('/cancel')
def cancel_page():
    """Shows home page"""
    return render_template('cancel.html')

@app.route('/start', methods=["POST"])
def survey_page():
    """Redirect to questions page"""
    session['Responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:ask>')
def questions_page(ask):
    """The questions page""" 
    question = survey.questions[ask]
    responses = session.get('Responses')

    if responses is None:
        return redirect('/')

    if len(responses) == len(survey.questions):
        return redirect('/thanks')
        
    if len(responses) != ask:
        flash(f'An invalid question {ask}, please answer the current question!')
        return redirect(f'/questions/{len(responses)}')

    return render_template('questions.html', next_question=ask, question=question)


@app.route('/answer', methods=["POST"])
def answer_page():
    """Store the questions and redirect to next one""" 
    choice = request.form['answer']  
    responses = session['Responses']
    responses.append(choice)
    session['Responses'] = responses
 
    if len(responses) == len(survey.questions):
        flash('Well done!')
        return redirect('/thanks')
    else:
        flash('You are notfinished the servey!')
        return redirect(f'/questions/{len(responses)}')

@app.route('/thanks')
def thanks_page():
    """Finish surver "Thank you" page"""
    return render_template('thanks.html')