from flask import Flask
from flask_ask import Ask, statement, question
import json
import numpy as np
import urllib
from sklearn import svm

from config import API_KEY
from data.weatherData import X_Data, Y_Data

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def greeting():
    msg = "Welcome to the Snow Day Calculator. What is your zip code?"
    return question(msg)

@ask.intent("PredictIntent", convert={'prediction': str})

# Prompt the user to enter their ZIP
def predict(prediction):
    site = "https://maps.googleapis.com/maps/api/geocode/json?address=" + str(prediction)
    data = urllib.urlopen(site)
    moredata = json.loads(data.read())

    print site
    print moredata['status']

    if moredata is None:
        return question("Sorry, that zip code is not valid. Would you like to try again?")

    if moredata['status'] == "ZERO_RESULTS":
        return question("Sorry, that zip code is not valid. Would you like to try again?")

    lat = moredata['results'][0]['geometry']['location']['lat']
    long = moredata['results'][0]['geometry']['location']['lng']
    name = moredata['results'][0]['formatted_address']
    name = name[:-11]

    # Train the classifier

    lines = 0

    for i in X_Data:
        lines = lines + 1

    X = np.zeros((lines, 5))

    line = 0
    for row in X:
        X[line, 0] = X_Data[line][0]
        X[line, 1] = X_Data[line][1]
        X[line, 2] = X_Data[line][2]
        X[line, 3] = X_Data[line][3]
        X[line, 4] = X_Data[line][4]
        line = line + 1

    # fitting the data to the tree

    y = np.array(Y_Data).reshape(line,)

    clf = svm.SVC(probability=True, kernel='linear', tol=0.001, C=0.95, class_weight='balanced')

    clf.fit(X, y)

    coordinates = prediction

    #Get the Latitude and Longitude based off of the zipcode, to be used for user input

    url = "https://api.darksky.net/forecast/"+API_KEY+"/"+str(lat)+","+str(long)

    # API Request
    page = urllib.urlopen(url)

    result = json.loads(page.read())

# Functions to get features from the API call

# Get section of America, southern states are more prone to snow days!
    latCar = round(float(lat))
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
    prob = result['daily']['data'][1]['precipProbability']

    # Average Temp over 12 hours, return 1 if temp average temp is under 32 degrees
    temperature = result['daily']['data'][1]['temperatureMin']
    temp = 0
    if(temperature>32):
        temp = 0
    elif temperature<=32:
        temp = 1

    # Get the type of precipitation (if snow, return 1. if not, return 0.25. This is the attenuation factor.)
    type = 0
    try:
        pretype = result['daily']['data'][1]['precipType']
        if(pretype == "snow"):
            type = 1
        else:
            pass
    except:
        pass


    # Get the estimated accumulation of snow (BIGGEST FACTOR)
    accumulation = 0
    try:
        accumulation = result['daily']['data'][1]['precipAccumulation']
    except:
        pass

    # Get a weather summary from Dark Sky
    summary = (result['currently']['summary'])

    # Daily summary
    summaryd = (result['daily']['data'][1]['summary'])

    storm_distance = result['currently']['nearestStormDistance']

    if "Snow" in summaryd:
        type = 1
    elif "snow" in summaryd:
        type = 1

    # Make a prediction based on the given data. Weigh each feature by a certain amount.

    # DATA: TYPE, ACCUMULATION, CHANCE, TEMP, SPEED, CATEGORY, STORM_DISTANCE (organized in order of importance)

    features = [type,accumulation,prob,temp, cat]

    # Prediction index
    arr = np.asarray(features).ravel()

    array = [arr]

#   prediction1 = clf.predict(array)
    ans = clf.predict_proba(array)
    finalPrediction = round(ans.item((0, 1)) * 100,1)
    print features

#    # Override the print function IF something occurs
    try:
        if temperature >= 40:
            return question(
                "There is a small chance of a snow day tomorrow in {}, {}, because it won't be cold enough. Tomorrow, the temperature will hit a low of {} degrees for the day, which is too warm for it to snow. Would you like to ask again?".format(name, temperature))

        if finalPrediction < 25:
            if type !=1:
                return question("There is a small chance of a snow day tomorrow in {}, {}, because it isn't supposed to snow. The forecast calls for {}. Would you like to ask again?".format(name,summaryd))

            if temp == 0:
                return question("There is a small chance of a snow day tomorrow in {}, {}, because it won't be cold enough. Tomorrow, the temperature will hit a low of {} degrees for the day, which is too warm for it to snow. Would you like to ask again?".format(name,temperature))

            if accumulation <= 1 and cat<=1:
                return question("There is a small chance of a snow day tomorrow in {}, because the forecast calls for {}, and less than an inch of snowfall over the next 24 hours. Would you like to ask again?".format(name,summaryd))

        if finalPrediction > 75:
            return question("There is a {} percent chance of a snow day tomorrow in {}. The forecast calls for {}, meaning there is a very good chance of a snow day. Would you like to ask again?".format(finalPrediction, name, summaryd))

        return question("There is a {} percent chance of a snow day tomorrow in {}, {}. The forecast calls for {}. Would you like to ask again?".format(finalPrediction,name,summaryd))
    except:
        return question("Sorry, I couldn't find any weather data for this zip code. Would you like to try again?")
@ask.intent("HelpIntent")
def help():
    msg = "To make a prediction, simply say your zip code when prompted, and the likelihood of a snow day will be returned. Would you like to try?"
    return question(msg)

@ask.intent("YesIntent")
def yes():
    return question("What is your zip code?")

@ask.intent("NoIntent")
def no():
    return statement("Goodbye!")

if __name__ == "__main__":
    app.run(debug=True)
