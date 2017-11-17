from datetime import datetime
from SnowDay.config import API_KEY
import urllib
import json
import numpy as np
from SnowDay.processor import clf, number, lat, long

# Enter in the following format: first 3 letters of month SPACE day COMMA SPACE year SPACE time:00AM/PM
def timetravel(day, time, zip):

    print "Finding weather information for {} at {}.".format(day, time)

    coordinates = zip

    #Get the Latitude and Longitude based off of the zipcode, to be used for user input
    def getLat(zipcode):
        return str(lat[number.index(zipcode)])

    def getLong(zipcode):
        return str(long[number.index(zipcode)])

    date = day+" "+time
    dt = datetime.strptime(date, '%b %d, %Y %I:%M%p')

    dateurl = dt.isoformat('T')
    url = "https://api.darksky.net/forecast/"+API_KEY+"/"+str(lat[number.index(coordinates)])+","+str(long[number.index(coordinates)]) +","+ dateurl + "?exclude=currently,hourly,minutely,alerts,flags"

    print url
    page = urllib.urlopen(url)

    result = json.loads(page.read())
    print result

    return result

timeData = timetravel("Jan 3, 2014","1:00AM", "02492")

def timePredict(data):
    result = data

    # Functions to get features from the API call

    # Get section of America, southern states are more prone to snow days!
    latCar = round(float(44.0165))
    cat = 0

    if latCar < 35:
        cat = 2
    elif latCar >= 35 and latCar <= 40:
        cat = 1
    else:
        cat = 0

    # Get the current time
    # time = result['daily']['time']

    # Get the chance of precipitation NEED TO CHANGE THIS
    n = result['daily']['data'][0]['precipProbability']
    prob = n

    # Average Temp over 12 hours, return 1 if temp average temp is under 32 degrees
    temperature = result['daily']['data'][0]['temperatureMin']
    temp = 0
    if (temperature >= 32):
        temp = 0
    elif temperature < 32:
        temp = 1

    # Get current wind speed, return 0 if not blizzard and 1 if blizzard
    speed = (result['daily']['data'][0]['windSpeed'])

    # Get the type of precipitation (if snow, return 1. if not, return 0.25. This is the attenuation factor.)
    type = 0
    pretype = result['daily']['data'][0]['precipType']
    if "snow" in pretype:
        type = 1
    else:
        pass

    # Get the estimated accumulation of snow (BIGGEST FACTOR)
    accumulation = 0
    try:
        accumulation = result['daily']['data'][0]['precipAccumulation']
    except:
        pass

    # Get a weather summary from Dark Sky
    summary = (result['daily']['data'][0]['summary'])

    # storm_distance = result['daily']['data'][0]['nearestStormDistance']
    # print storm_distance

    # Make a prediction based on the given data. Weigh each feature by a certain amount.

    # DATA: ACCUMULATION, CHANCE, TEMP, SPEED, TIME (organized in order of importance)
    # Features are all scaled to a range of 0-100, then they have weights applied to them in order of importance

    features = [type, accumulation, prob, temp, round(speed, 0), cat]

    # Prediction index
    arr = np.asarray(features).ravel()

    array = [arr]

    #   prediction1 = clf.predict(array)
    answer = clf.predict_proba(array)
    final1 = str(answer.item((0, 1)) * 100)

    print array

    #    # Override the print function IF something occurs
    if temp == 0:
        return "There is a zero percent chance of a snow day, because it is {} degrees outside.".format(temperature)

    if type != 1:
        return "There is a zero percent chance of a snow day, because it will {} instead.".format(pretype)

    if accumulation <= 2:
        return "There is a zero percent chance of a snow day, because it will only snow {} inches".format(accumulation)

    message = summary.encode('utf-8')

    return "There is a {} percent chance of a snow day. ".format(final1) + message

print timePredict(timeData)