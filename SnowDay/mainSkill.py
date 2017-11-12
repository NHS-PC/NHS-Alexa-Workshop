from flask import Flask
from flask_ask import Ask, statement, question
import processor

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def greeting():
    msg = "Welcome to the Snow Day Calculator. What is your zip code?"
    return question(msg)

@ask.intent("PredictIntent")
def predict(prediction):
    return True


