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

    # Load CSV data of all zipcodes
    csvdata = pd.read_csv(r'zipcodes.csv', skipinitialspace=True, delimiter=",")
    number = []
    zip = csvdata["ZIP"]
    lat = csvdata["LAT"]
    long = csvdata["LNG"]
    for x in zip:
        if str(x).__len__() == 3:
            a = "00" + str(x)
            number.append(a)
        if str(x).__len__() == 4:
            a = "0" + str(x)
            number.append(a)
        elif str(x).__len__() == 5:
            a = str(x)
            number.append(a)
    # Train the classifier

    lines = 0

    for i in X_Data:
        lines = lines + 1

    X = np.zeros((lines, 7))

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

    y = np.array(Y_Data).reshape(line,)

    clf = svm.SVC(probability=True, kernel='linear', tol=0.001, C=0.95, class_weight='balanced')

    clf.fit(X, y)

    coordinates = prediction

    #Get the Latitude and Longitude based off of the zipcode, to be used for user input
    def getLat(zipcode):
        return str(lat[number.index(zipcode)])

    def getLong(zipcode):
        return str(long[number.index(zipcode)])

    try:
        index = lat[number.index(coordinates)]
    except:
        return question("Sorry, the zip code {} is not valid. Would you like to try again?".format(coordinates))
    url = "https://api.darksky.net/forecast/"+API_KEY+"/"+str(lat[number.index(coordinates)])+","+str(long[number.index(coordinates)])

    # API Request
    page = urllib.urlopen(url)

    result = json.loads(page.read())

# Functions to get features from the API call

# Get section of America, southern states are more prone to snow days!
    latCar = round(float(getLat(coordinates)))
    cat = 0

    if latCar<35:
        cat = 2
    elif latCar>=35 and latCar<=40:
        cat = 1
    else:
        cat = 0

    # Get the current time
    time = result['currently']['time']

    # Get the chance of precipitation NEED TO CHANGE THIS
    total = 0
    count = 0
    for i in range(0,12):
        n = result['hourly']['data'][i]['precipProbability']
        total+=n
        count+=1
    prob = round(total/count,2)

    # Average Temp over 12 hours, return 1 if temp average temp is under 32 degrees
    temperature = result['daily']['data'][0]['temperatureMin']
    temp = 0
    if(temperature>32):
        temp = 0
    elif temperature<=32:
        temp = 1

    # Get current wind speed, return 0 if not blizzard and 1 if blizzard
    speed = (result['currently']['windSpeed'] + result['currently']['windGust']) / 2

    # Get the type of precipitation (if snow, return 1. if not, return 0.25. This is the attenuation factor.)
    type = 0
    for i in range(1,6):
        try:
            pretype = result['hourly']['data'][i]['precipType']
            if(pretype == "snow"):
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

    storm_distance = result['currently']['nearestStormDistance']

    # Make a prediction based on the given data. Weigh each feature by a certain amount.

    # DATA: TYPE, ACCUMULATION, CHANCE, TEMP, SPEED, CATEGORY, STORM_DISTANCE (organized in order of importance)

    features = [type,accumulation,prob,temp, round(speed,0), cat, storm_distance]

    # Prediction index
    arr = np.asarray(features).ravel()

    array = [arr]

#   prediction1 = clf.predict(array)
    ans = clf.predict_proba(array)
    finalPrediction = str(ans.item((0, 1)) * 100)

    print coordinates
    print finalPrediction

#    # Override the print function IF something occurs
    try:
        if temp == 0:
            return question("There is a small chance of a snow day, because it is too hot. Right now, it is about {} degrees outside. Would you like to ask again?".format(temperature))

        if type !=1:
            return question("There is a small chance of a snow day, because it isn't supposed to snow today. The forecast calls for {}. Would you like to ask again?".format(summary))

        if accumulation <= 1 and cat<=1:
            return question("There is a small chance of a snow day, because the forecast calls for {}, and less than an inch of snowfall at most. Would you like to ask again?".format(summary))

        message = summary.encode('utf-8')

        return question("There is a {} percent chance of a snow day. Would you like to ask again?".format(finalPrediction) + message)
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
