import json
import urllib
import pandas as pd
import numpy as np
import time
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from os import system
from sklearn import svm
import os
import sys


# Load CSV data of all zipcodes
csvdata = pd.read_csv(r'zipcodes.csv', skipinitialspace=True, delimiter=",")
number= []
zip = csvdata["ZIP"]
lat = csvdata["LAT"]
long = csvdata["LNG"]
for x in zip:
    if str(x).__len__() == 3:
        a = "00"+str(x)
        number.append(a)
    if str(x).__len__() == 4:
        a = "0"+str(x)
        number.append(a)
    elif str(x).__len__() == 5:
        a = str(x)
        number.append(a)

# Load weather data



# Prompt the user to enter their ZIP
coordinates = raw_input("What is your ZIP Code?")

#Get the Latitude and Longitude based off of the zipcode, to be used for user input
def getLat(zipcode):
    return str(lat[number.index(zipcode)])

def getLong(zipcode):
    return str(long[number.index(zipcode)])

# URL
url = "https://api.darksky.net/forecast/7087ce0f218cc2c9ec3244a25f8f2f59/"+getLat(coordinates)+","+getLong(coordinates)
print url
# API Request
page = urllib.urlopen(url)

result = json.loads(page.read())

# Functions to get features from the API call

# Get section of America, southern states are more prone to snow days!
def latCar():
    latitude = round(float(getLat(coordinates)))

    if latitude<35:
        return 2
    elif latitude>=35 and latitude<=40:
        return 1
    else:
        return 0

# Get the current time
def getTime():
    return result['currently']['time']

# Get the chance of precipitation
def getPrecipChance():
    count = 0
    total = 0
    for i in range(0,12):
        n = result['hourly']['data'][i]['precipProbability']
        total+=n
        count+=1
    return round(total/count,2)

# Average Temp over 12 hours, return 1 if temp average temp is under 32 degrees
def getTemp():
    temp = 0
    total = 0
    for i in range(0,12):
        temp+=int(result['hourly']['data'][i]['temperature'])
        total+=1
    if(temp/total >=32):
        return 0
    else:
        return 1

# Get current wind speed, return 0 if not blizzard and 1 if blizzard
def getSpeed():
    speed = (result['currently']['windSpeed'] + result['currently']['windGust']) / 2
    if(speed<=20):
        return 0
    else:
        return 1
# Get the type of precipitation (if snow, return 1. if not, return 0.25. This is the attenuation factor.)
def getType():
    for i in range(1,12):
        try:
            pretype = result['hourly']['data'][i]['precipType']
            if(pretype == "snow"):
                return 1
            else:
                pass
        except:
            pass
    return 0

# Get the estimated accumulation of snow (BIGGEST FACTOR)
def getAccumulation():
    for i in range(0,12):
        try:
            return result['daily']['data'][i]['precipAccumulation']
        except:
            pass
    return 0

# Get a weather summary from Dark Sky
def getSummary():
    return (result['daily']['summary'])

# Make a prediction based on the given data. Weigh each feature by a certain amount.

# DATA: ACCUMULATION, CHANCE, TEMP, SPEED, TIME (organized in order of importance)
# Features are all scaled to a range of 0-100, then they have weights applied to them in order of importance

features = [getType(),getAccumulation(),getPrecipChance(), getTemp(), getSpeed(), latCar()]

weights = np.asarray([1,1,1,1,1,1])
weights.shape = (features.__len__(),1)

#Dot multiplication for features. If the precipitation type is not snow, then decrease the likelihood of a snow day
new_nums = features*weights.transpose()*(getType())

# Prediction index
prediction = np.zeros((1, 6))

with open("current.day") as data_file:
    data = json.load(data_file)

    prediction[0, 0] = data['daily']['data'][1]['temperatureMin']
    prediction[0, 1] = getPrecipChance()
    prediction[0, 2] = data['daily']['data'][1]['precipIntensity']
    if 'precipAccumulation' in data ['daily']['data'][1]:
        prediction[0, 3] = getAccumulation()
    else:
        prediction[0, 3] = 0
    prediction[0, 4] = getType()
    prediction[0, 5] = getTemp()

def predict(n):
    X_Train = [[1,20,80,1,15,1],[1,15,60,1,15,0],[0,0.16,25,0,10,1],[1,0.015,0.02,0,0,2],[0,0.013,0.1,0,0,1],[1,1,10,30,15,2],
               [1,12,90,1,20,2],[1,8,85,1,15,1]]
    Y_Train = [[1],[1],[0],[0],[0],[0],[1],[1]]

    clf = svm.SVC(probability=True, kernel='linear', tol=0.001, C=0.95, class_weight='balanced')
    # fitting the data to the tree
    clf.fit(X_Train, Y_Train)
    # predicting the gender based on a prediction
    prediction = clf.predict(n)

    # Visualize tree
    dotfile = open("dtree.dot", 'w')
    tree.export_graphviz(clf, out_file=dotfile)
    dotfile.close()
    system("dot -Tpdf dtree.dot -o dtree.pdf")
    system("xdg-open dtree.pdf")

    # print the predicted gender
    print n
    print(prediction)
    print clf.predict_proba([[1,20,80,1,15,1]])


predict([features])
