import json
import urllib
import pandas as pd
import numpy
import time

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
    if int(getLat(coordinates))<35:
        return 2
    elif int(getLat(coordinates))>=35 and int(getLat(coordinates))<=40:
        return 1
    else:
        return 0

# Get the current time
def getTime():
    return result['currently']['time']

# Get the chance of precipitation
def getPrecipChance():
    return result['currently']['precipProbability']

# Average Temp over 12 hours
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
    return 0.25

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

# Activation function, how to weigh accumulation in the main percent chance equation
def accfn(n):
    percent = getAccumulation()
    if percent<=1:
        return 0
    elif percent>1 and percent<=12:
        return 3.5*percent
    elif percent>12 and percent<=94:
        return .27*((n+17)**1.5)
    else:
        return (100*(n**1.5))/((n+2)*(n**1.5))

# Make a prediction based on the given data. Weigh each feature by a certain amount.

# DATA: ACCUMULATION, CHANCE, TEMP, SPEED, TIME (organized in order of importance)

features = [getType(),getAccumulation(),getPrecipChance(), getTemp(), getSpeed(), getTime()]

weights = numpy.asarray([1,1,1,1,1,1])
weights.shape = (features.__len__(),1)

#Dot multiplication for features. If the precipitation type is not snow, then decrease the likelihood of a snow day
new_nums = features*weights.transpose().dot(getType())

print features, "Features"
time.sleep(1)
print weights, "Weights"
time.sleep(1)
print new_nums, "Multiplied"

print accfn(95)

