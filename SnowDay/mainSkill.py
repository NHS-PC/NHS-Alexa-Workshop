from flask import Flask
from flask_ask import Ask, statement, question
import json
import numpy as np
import urllib

import pandas as pd
from sklearn import svm

from config import API_KEY
from data.weatherData import X_Data, Y_Data

app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def greeting():
    msg = "Welcome to the Snow Day Calculator, powered by the Dark Sky API. What is your zip code?"
    return question(msg)


@ask.intent("PredictIntent", convert={'prediction': str})
# Prompt the user to enter their ZIP
def predict(prediction):
    zipurl = "http://api.zipasaur.us/zip/" + str(prediction)
    zippage = urllib.urlopen(zipurl)
    cityresult = json.loads(zippage.read())
    if cityresult is None:
        return question("Sorry, the zip code {} is not valid. Would you like to try again?".format(prediction))

    city = cityresult['city']
    state = cityresult['state_full']
    lat = cityresult['lat']
    long = cityresult['lng']

    # Train the classifier

    lines = 0

    for i in X_Data:
        lines = lines + 1

    X = np.zeros((lines, 6))

    line = 0
    for row in X:
        X[line, 0] = X_Data[line][0]
        X[line, 1] = X_Data[line][1]
        X[line, 2] = X_Data[line][2]
        X[line, 3] = X_Data[line][3]
        X[line, 4] = X_Data[line][4]
        X[line, 5] = X_Data[line][5]
        line = line + 1

    # fitting the data to the tree

    y = np.array(Y_Data).reshape(line, )

    clf = svm.SVC(probability=True, kernel='linear', tol=0.001, C=0.95, class_weight='balanced')

    clf.fit(X, y)

    coordinates = prediction

    # Get the Latitude and Longitude based off of the zipcode, to be used for user input

    url = "https://api.darksky.net/forecast/" + API_KEY + "/" + lat + "," + str(long)

    # API Request
    page = urllib.urlopen(url)

    result = json.loads(page.read())

    # Get city name

    cityurl = "http://api.zipasaur.us/zip/" + str(coordinates)
    citypage = urllib.urlopen(cityurl)
    cityresult = json.loads(citypage.read())
    city = cityresult['city']
    state = cityresult['state_full']

    # Functions to get features from the API call

    # Get section of America, southern states are more prone to snow days!
    latCar = round(float(lat))
    cat = 0

    if latCar < 35:
        cat = 2
    elif latCar >= 35 and latCar <= 40:
        cat = 1
    else:
        cat = 0

    # Get the current time
    time = result['currently']['time']

    # Get the chance of precipitation NEED TO CHANGE THIS
    total = 0
    count = 0
    for i in range(0, 12):
        n = result['hourly']['data'][i]['precipProbability']
        total += n
        count += 1
    prob = round(total / count, 2)

    # Average Temp over 12 hours, return 1 if temp average temp is under 32 degrees
    temperature = result['daily']['data'][0]['temperatureMin']
    tempc = result['hourly']['data'][0]['temperature']
    temp = 0
    if (temperature > 32):
        temp = 0
    elif temperature <= 32:
        temp = 1

    # Get current wind speed, return 0 if not blizzard and 1 if blizzard
    speed = (result['currently']['windSpeed'] + result['currently']['windGust']) / 2

    # Get the type of precipitation (if snow, return 1. if not, return 0.25. This is the attenuation factor.)
    type = 0
    for i in range(1, 6):
        try:
            pretype = result['hourly']['data'][i]['precipType']
            if (pretype == "snow"):
                type = 1
            elif pretype == "rain":
                type = 2
            elif type == "sleet":
                type = 3
            else:
                pass
        except:
            pass

    # Get the estimated accumulation of snow (BIGGEST FACTOR)
    accumulation = 0
    try:
        accumulation = result['daily']['data'][0]['precipAccumulation']
    except:
        pass

    # Get a weather summary from Dark Sky
    summary = (result['currently']['summary'])

    # Daily summary
    summaryd = (result['daily']['data'][0]['summary'])

    storm_distance = result['currently']['nearestStormDistance']

    # Make a prediction based on the given data. Weigh each feature by a certain amount.

    # DATA: TYPE, ACCUMULATION, CHANCE, TEMP, SPEED, CATEGORY, STORM_DISTANCE (organized in order of importance)

    features = [type, accumulation, prob, temp, round(speed, 0), cat]

    # Prediction index
    arr = np.asarray(features).ravel()

    array = [arr]

    #   prediction1 = clf.predict(array)
    ans = clf.predict_proba(array)
    finalPrediction = (ans.item((0, 1)) * 100)

    print coordinates
    print finalPrediction

    #    # Override the print function IF something occurs
    try:
        if finalPrediction < 25:
            if type != 1:
                return question(
                    "There is a small chance of a snow day in {}, {}, because it isn't supposed to snow today. The forecast calls for {}. Would you like to ask again?".format(
                        city, state, summary))

            if temp == 0:
                return question(
                    "There is a small chance of a snow day in {}, {}, because it isn't cold enough. Right now, it is about {} degrees outside, with a low of {} degrees for the day. Would you like to ask again?".format(
                        city, state, tempc, temperature))

            if accumulation <= 1 and cat <= 1:
                return question(
                    "There is a small chance of a snow day in {}, {}, because the forecast calls for {}, and less than an inch of snowfall at most. Would you like to ask again?".format(
                        city, state, summary))

        message = summary.encode('utf-8')

        if finalPrediction > 75:
            return question(
                "There is a {} percent chance of a snow day in {}, {}. The forecast calls for {}, meaning there is a very good chance of a snow day. Would you like to ask again?".format(
                    finalPrediction, city, state, summaryd) + message)

        return question(
            "There is a {} percent chance of a snow day in {}, {}. Would you like to ask again?".format(finalPrediction,
                                                                                                        city,
                                                                                                        state) + message)
    except:
        return question("Sorry, I couldn't find any weather data for this zip code. Would you like to try again?")


@ask.intent("HelpIntent")
def help():
    msg = "This snow day prediction application uses the Dark Sky API to get weather data based on a location. The weather data collected is then compared to weather" \
          "in the past, and then classified as either being conditions for a snow day or not. The percent chance is calculated using a Support Vector Machine, with the" \
          "Sci-kit Learn library in Python. To make a prediction, simply say your zip code when prompted, and a percentage will be returned. Would you like to try?"
    return question(msg)


@ask.intent("YesIntent")
def yes():
    return question("What is your zip code?")


@ask.intent("NoIntent")
def no():
    return statement("Goodbye!")


if __name__ == "__main__":
    app.run(debug=True)
