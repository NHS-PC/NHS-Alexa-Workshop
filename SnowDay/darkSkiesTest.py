import json
import urllib
from bs4 import BeautifulSoup

request = "https://api.darksky.net/forecast/7087ce0f218cc2c9ec3244a25f8f2f59/51.5030032,-0.1277004"
page = urllib.urlopen(request)

result = json.loads(page.read())

print result['hourly']['data']['temperature']

