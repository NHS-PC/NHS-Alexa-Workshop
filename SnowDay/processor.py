import json
import urllib
import pandas as pd
import numpy as np
from sklearn import svm
import base64

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

# Train the classifier

X_Data = ([[1,20,80,1,15,1],[1,15,60,1,15,0],[0,0.16,25,0,10,1],[1,0.015,0.02,0,0,2],[0,0.013,0.1,0,0,1],[1,1,10,30,15,2],
               [1,12,90,1,20,2],[1,8,85,1,15,1],[0,.012,0,1,5,2]])

Y_Data = ([[1],[1],[0],[0],[0],[0],[1],[1],[0]])

lines = 0

for i in X_Data:
    lines = lines+1

X = np.zeros((lines,6))

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
    coordinates = zip

    #Get the Latitude and Longitude based off of the zipcode, to be used for user input
    def getLat(zipcode):
        return str(lat[number.index(zipcode)])

    def getLong(zipcode):
        return str(long[number.index(zipcode)])

    # URL
    url = "https://api.darksky.net/forecast/"+base64.b32decode("G4YDQN3DMUYGMMRRHBRWGMTDHFSWGMZSGQ2GCMRVMY4GMMTGGU4Q====")+"/"+str(lat[number.index(coordinates)])+","+str(long[number.index(coordinates)])

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

    # Get the chance of precipitation
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
    if(temperature>=32):
        temp = 1
    elif temperature<32:
        temp = 0

    # Get current wind speed, return 0 if not blizzard and 1 if blizzard
    speed = (result['currently']['windSpeed'] + result['currently']['windGust']) / 2

    # Get the type of precipitation (if snow, return 1. if not, return 0.25. This is the attenuation factor.)
    type = 0
    for i in range(1,12):
        try:
            pretype = result['hourly']['data'][i]['precipType']
            if(pretype == "snow"):
                type = 1
            else:
                pass
        except:
            pass


    # Get the estimated accumulation of snow (BIGGEST FACTOR)
    accumulation = 0
    for i in range(0,12):
        try:
            accumulation = result['daily']['data'][i]['precipAccumulation']
        except:
            pass

    # Get a weather summary from Dark Sky
    summary = (result['hourly']['summary'])

    a = coordinates

    # Make a prediction based on the given data. Weigh each feature by a certain amount.

    # DATA: ACCUMULATION, CHANCE, TEMP, SPEED, TIME (organized in order of importance)
    # Features are all scaled to a range of 0-100, then they have weights applied to them in order of importance

    features = [type,accumulation,prob,temp, round(speed,0), cat]

    # Prediction index
    arr = np.asarray(features).ravel()

    array = [arr]

    prediction1 = clf.predict(array)
    resultArr1 = clf.predict_proba(array)
    final1 = str(resultArr1.item((0, 1)) * 100)

#    # Override the print function IF something occurs
#    if temp >=32:
#        return "There is a zero percent chance of a snow day, because it is {} degrees outside.".format(temp)

#    if type != 1:
#        return "There is a zero percent chance of a snow day, because it will {} instead.".format(pretype)

#    if accumulation <= 2:
#        return "There is a zero percent chance of a snow day, because it only snow {} inches".format(accumulation)

    message = summary.encode('utf-8')

    return "There is a {} percent chance of a snow day. ".format(final1) + message

inp = raw_input("What is your zip code?")
print predict(inp)