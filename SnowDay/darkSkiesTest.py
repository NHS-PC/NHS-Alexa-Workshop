import json
import urllib
import processor

from bs4 import BeautifulSoup

a = raw_input("What is your zip code?")

latlong = processor.getLat(a)+","+processor.getLong(a)

request = "https://api.darksky.net/forecast/7087ce0f218cc2c9ec3244a25f8f2f59/"+latlong
page = urllib.urlopen(request)

result = json.loads(page.read())

print result['currently']['nearestStormDistance']

processor.predict()


