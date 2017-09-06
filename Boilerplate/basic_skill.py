from flask import Flask
from flask_ask import Ask, statement, question
# Basic Flask Ask Tool, gives the user a random fact about the NHS Programming Club.

#Import statements that we use for our apps generally go at the top, for organization.
import random

#Declaring Flask variables and import statement functions.
app = Flask(__name__)
ask = Ask(app, "/")

#List that we'll use to store out facts.
facts = ["a","b","c","d"]

#Basic skill instances. First, we declare a startup message.
@ask.launch
def start_skill():
    message = "Hello there, would you like to know a fact about the NHS Programming Club?"
    return question(message)

#No intent, for if our user says no.
@ask.intent("NoIntent")
def noResponse():
    msg = "Ok, okay. Sorry to bother you."
    return statement(msg)

#If our user wants a fact, select a random instance from our list and return it as a question, to keep the session open.
@ask.intent("YesIntent")
def pickFact():
    fact = random.choice(facts)
    return question(fact+" Would you like another fact?")

#If our user needs help, they can ask our program for help and it will provide a help message.
@ask.intent("HelpIntent")
def help():
    msg = "This is a help message. Your help message should contain instructions that helps the user of your skill better understand how to navigate your skill."
    return statement(msg)

#This is a flask statement, to check if we are running the code. If the code is in fact running on 'main', then run the app with a debugger log.
if __name__ == '__main__':
    app.run(debug=True)

