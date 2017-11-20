import json
import numpy as np
import urllib

import pandas as pd
from sklearn import svm

from config import API_KEY
from data.weatherData import X_Data, Y_Data

# Train the classifier

lines = 0

for i in X_Data:
    lines = lines+1

X = np.zeros((lines,7))

line = 0
col = 0
for row in X:
    X[line,0] = X_Data[line][0]
    X[line,1] = X_Data[line][1]
    X[line,2] = X_Data[line][2]
    X[line, 3] = X_Data[line][3]
    X[line, 4] = X_Data[line][4]
    X[line, 5] = X_Data[line][5]
    line = line+1

# fitting the data to the tree

y = np.array(Y_Data)

clf = svm.SVC(probability=True, kernel='linear', tol=0.001, C=0.95, class_weight='balanced')

clf.fit(X, y)


# Prompt the user to enter their ZIP

def predict(zip):
    zipurl = "http://api.zipasaur.us/zip/" + str(zip)
    zippage = urllib.urlopen(zipurl)
    cityresult = json.loads(zippage.read())
    if cityresult is None:
        return ("Sorry, the zip code {} is not valid. Would you like to try again?".format(zip))
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

    coordinates = zip

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
    print features

    #    # Override the print function IF something occurs

    if finalPrediction < 25:
        if type != 1:
            return "There is a small chance of a snow day in {}, {}, because it isn't supposed to snow today. The forecast calls for {}. Would you like to ask again?".format(
                    city, state, summary)

        if temp == 0:
            return "There is a small chance of a snow day in {}, {}, because it isn't cold enough. Right now, it is about {} degrees outside, with a low of {} degrees for the day. Would you like to ask again?".format(
                    city, state, tempc, temperature)

        if accumulation <= 1 and cat <= 1:
            return "There is a small chance of a snow day in {}, {}, because the forecast calls for {}, and less than an inch of snowfall at most. Would you like to ask again?".format(
                    city, state, summary)

    message = summary.encode('utf-8')

    return "There is a {} percent chance of a snow day in {}, {}. Would you like to ask again?".format(finalPrediction, city,state) + message

def timePredict(data):
    answer = clf.predict_proba(data)
    final1 = str(answer.item((0, 1))*100)
    return final1

print predict("02490")