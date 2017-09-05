from flask import Flask
from flask_ask import Ask, statement, question
# Basic Flask Ask Tool, gives the user a random fact about the NHS Programming Club.

import random

app = Flask(__name__)
ask = Ask(app, "/")

facts = ["a","b","c","d"]

@ask.launch
def start_skill():
    message = "Hello there, would you like to know a fact about the NHS Programming Club?"
    return question(message)

@ask.intent("NoIntent")
def noResponse():
    msg = "Ok, okay. Sorry to bother you."
    return statement(msg)

