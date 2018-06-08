import json
import numpy as np
import urllib

from sklearn import svm

from config import API_KEY
from data.weatherData import X_Data, Y_Data
# Prompt the user to enter their ZIP

def predict(zip):
    site = "https://maps.googleapis.com/maps/api/geocode/json?address="+str(zip)
    data = urllib.urlopen(site)
    moredata = json.loads(data.read())

    lat = moredata['results'][0]['geometry']['location']['lat']
    long = moredata['results'][0]['geometry']['location']['lng']
    name = moredata['results'][0]['formatted_address']
    name = name[:-11]

    # Train the classifier

    X = np.array(X_Data)
    y = np.array(Y_Data).reshape(len(X), )

    # fitting the data to the SVM
    clf = svm.SVC(probability=True, kernel='linear', tol=0.001, C=0.95, class_weight='balanced')

    clf.fit(X, y)

    # Get the Latitude and Longitude based off of the zipcode, to be used for user input

    url = "https://api.darksky.net/forecast/" + API_KEY + "/" + str(lat) + "," + str(long)

    # API Request
    page = urllib.urlopen(url)
    result = json.loads(page.read())

    # Get section of America, southern states are more prone to snow days!
    latCar = round(float(lat))

    if latCar < 35:
        cat = 2
    elif latCar >= 35 and latCar <= 40:
        cat = 1
    else:
        cat = 0

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
    if (temperature > 40):
        temp = 0
    elif temperature <= 40:
        temp = 1

    # Get the type of precipitation (if snow, return 1. if not, return 0.25. This is the attenuation factor.)
    type = 0
    for i in range(1, 6):
        try:
            pretype = result['hourly']['data'][i]['precipType']
            if (pretype == "snow"):
                type = 1
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
    summary = result['currently']['summary']

    # Make a prediction based on the given data. Weigh each feature by a certain amount.

    # DATA: TYPE, ACCUMULATION, CHANCE, TEMP, CATEGORY (organized in order of importance)

    features = [type, accumulation, prob, temp, cat]

    array = [np.asarray(features).ravel()]

    #   prediction1 = clf.predict(array)
    ans = clf.predict_proba(array)
    finalPrediction = (ans.item((0, 1)) * 100)

    print features
    print finalPrediction
    #    # Override the print function IF something occurs

    if  finalPrediction < 25:
        if type != 1:
            return "There's less than a 25% chance of snow in {}. The weather calls for {}.".format(name,summary)

    return "There is a {} percent chance of a snow day in {}.".format(finalPrediction, name)

print predict("02494")