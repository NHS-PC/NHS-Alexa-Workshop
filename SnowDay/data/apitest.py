import json
import urllib

site = "https://maps.googleapis.com/maps/api/geocode/json?address=02494"
data = urllib.urlopen(site)
moredata = json.loads(data.read())

lat = moredata['results'][0]['geometry']['location']['lat']
long = moredata['results'][0]['geometry']['location']['lng']
name = moredata['results'][0]['address_components'][1]['long_name']
state = moredata['results'][0]['address_components'][4]['long_name']


print lat, long, name, state




