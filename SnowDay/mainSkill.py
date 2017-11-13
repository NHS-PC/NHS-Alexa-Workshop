from flask import Flask
from flask_ask import Ask, statement, question
import processor

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def greeting():
    msg = "Welcome to the Snow Day Calculator, powered by the Dark Sky API. What is your zip code?"
    return question(msg)

@ask.intent("PredictIntent")
def predict(prediction):
    snow_day = processor.predict(str(prediction))
    msg = "There is a {} percent chance of a snow day in your town. Would you like to ask again?".format(snow_day)
    return question(msg)

@ask.intent("HelpIntent")
def help():
    msg = "This snow day prediction application uses the Dark Sky API to get weather data based on a location. The weather datat collected is then compared to the weather" \
          "in the past, and then classified as either being conditions for a snow day or not. The percent chance is calculated using a Support Vector Machine, with the" \
          "Sci-kit Learn library in Python. To make a prediction, simply say your zip code when prompted, and a percentage will be returned. Would you like to try?"
    return question(msg)

@ask.intent("YesIntent")
def yes():
    return question("What is your zip code?")

@ask.intent("NoIntent")
def no():
    return statement("Goodbye!")
