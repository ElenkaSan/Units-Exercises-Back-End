from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    # TODO -- write tests for every view function / feature!
    def test_game_page(self):
        with app.test_client() as client:
            # can now make requests to flask via `client`
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Boogle Game</h1>', html)
            self.assertIsNone(session.get('bestScore'))
            self.assertIsNone(session.get('games'))

    def test_check_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as guess_session:
                guess_session['board'] = [[s,k,y,y,s],
                                [s,k,y,y,s],
                                [s,k,y,y,s],
                                [s,k,y,y,s],
                                [s,k,y,y,s]]
                guess_session['score'] = 0
        resp1 = client.get('/check-valid-word?word=sky')
        self.assertEqual(resp1.json['result'], 'ok')
        self.assertEqual(resp1.status_code, 200)
        resp2 = client.get('/check-valid-word?word=funny')
        self.assertEqual(resp2.json['result'], 'not-on-board')
        resp3 = client.get('/check-valid-word?word=jewqz')
        self.assertEqual(resp3.json['result'], 'not-word')


    def test_update_basics(self):
        with app.test_client() as client:
            resp = client.post('/score', data={'score', 15})
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4>You score: <span>15</span></h4>', html)
            self.assertEqual(session['bestScore'], 15)
            self.assertEqual(session['games'], 1)
