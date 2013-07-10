#!/usr/bin/env python
"""
get weather statuses from the places we're interested in and store them in the
database
@author: Chris Hausler
"""
import urllib
import json
from config import places, db_name
from pymongo import MongoClient
import time

kelvin = 273.15
pause = 600  # time between requests in seconds
client = MongoClient()
db = client[db_name]
weather = db.weather
url = "http://api.openweathermap.org/data/2.5/weather?"

while True:
    for l in places:
        params = urllib.urlencode({'q': '%s,%s' % (l, places[l]['country'])})
        response = urllib.urlopen(url + params).read()
        response = json.loads(response)
        post_id = weather.insert(response)
        print '%13s\t%10s\t%.1f degrees' % (l, response['weather'][0]['main'],
                                    response['main']['temp'] - kelvin)
    time.sleep(pause)
