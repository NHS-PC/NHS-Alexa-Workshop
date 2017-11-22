from datetime import datetime
from SnowDay.config import API_KEY
import urllib
import json

# Enter in the following format: first 3 letters of month SPACE day COMMA SPACE year SPACE time:00AM/PM
def timetravel(day, time, zip):

    print "Finding weather information for {} at {}.".format(day, time)

    zipurl = "http://api.zipasaur.us/zip/" + str(zip)
    zippage = urllib.urlopen(zipurl)
    cityresult = json.loads(zippage.read())
    if cityresult is None:
        return ("Sorry, the zip code {} is not valid. Would you like to try again?".format(zip))
    city = cityresult['city']
    state = cityresult['state_full']
    lat = cityresult['lat']
    long = cityresult['lng']

    coordinates = zip

    date = day+" "+time
    datentime = datetime.strptime(date, '%b %d, %Y %I:%M%p')

    dateurl = datentime.isoformat('T')
    url = "https://api.darksky.net/forecast/" + API_KEY + "/" + lat + "," + str(long)+","+ dateurl + "?exclude=currently,hourly,minutely,alerts,flags"

    print url
    page = urllib.urlopen(url)

    result = json.loads(page.read())
    print result

    return result

def timePredict(data):
    result = data
    latCar = round(float(44.0165))
    cat = 0

    if latCar < 35:
        cat = 2
    elif latCar >= 35 and latCar <= 40:
        cat = 1
    else:
        cat = 0

    n = result['daily']['data'][0]['precipProbability']
    prob = n

    temperature = result['daily']['data'][0]['temperatureMin']
    temp = 0
    if (temperature >= 32):
        temp = 0
    elif temperature < 32:
        temp = 1

    speed = (result['daily']['data'][0]['windSpeed'])

    type = 0
    try:
        pretype = result['daily']['data'][0]['precipType']
        if "snow" in pretype:
            type = 1
        else:
            pass
    except:
        pass

    accumulation = 0
    try:
        accumulation = result['daily']['data'][0]['precipAccumulation']
    except:
        pass

    summary = (result['daily']['data'][0]['summary'])

    features = [type,accumulation,prob,temp,cat]

    print summary
    print "Type: ", type
    print "Accumulation: ",accumulation
    print "Probability of Precip: ",prob
    print "Temp: ",temp
    print "Windspeed: ",speed
    print "Lat Car: ", cat
    print features

timeData = timetravel("Mar 14, 2017","9:00AM", "01841")

timePredict(timeData)