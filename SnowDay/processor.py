import json
import urllib
import pandas as pd

request = "https://api.darksky.net/forecast/7087ce0f218cc2c9ec3244a25f8f2f59/42.299490,-71.232519"
page = urllib.urlopen(request)

result = json.loads(page.read())

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

def getTime():
    return result['currently']['time']


def getPrecipChance():
    return result['currently']['precipProbability']

# Average Temp over 12 hours
def getTemp():
    temp = 0
    total = 0
    for i in range(0,12):
        temp+=int(result['hourly']['data'][i]['temperature'])
        total+=1
    return temp/total

def getSpeed():
    return (result['currently']['windSpeed'] + result['currently']['windGust']) / 2


def getType():
    for i in range(1,12):
        try:
            return result['hourly']['data'][i]['precipType'] + " in {} hours".format(i)
        except:
            pass
    return "No precip"


def getAccumulation():
    for i in range(0,12):
        try:
            return result['daily']['data'][i]['precipAccumulation'], " in {} hours".format(i)
        except:
            pass

def getSummary():
    return (result['daily']['summary'])

def getLat(zipcode):
    return str(lat[number.index(zipcode)])

def getLong(zipcode):

    return str(long[number.index(zipcode)])

dataThing = result['hourly']['data'][1]['temperature']

print getType()
print getAccumulation()