#!/usr/bin/env python
"""
This grabs all tweets marked with a location in the config file and stores them
in the database

Stolen from the Data Science Course @coursera and modified
@author: Chris Hausler
"""

import oauth2 as oauth
import urllib2 as urllib
import json
from config import languages, places, db_name
import numpy as np
from pymongo import MongoClient

client = MongoClient()
db = client[db_name]

# load twitter authentication details
access_token_key = db.config.find_one({'name': 'access_token_key'})['value']
access_token_secret = db.config.find_one(
                                    {'name': 'access_token_secret'})['value']
consumer_key = db.config.find_one({'name': 'consumer_key'})['value']
consumer_secret = db.config.find_one({'name': 'consumer_secret'})['value']


_debug = 0
oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"
http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


def twitterreq(url, method, parameters):
    """
    Construct, sign, and open a twitter request
    using the hard-coded credentials above.
    """
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def locate(coords):
    """
    Use the GPS coords to place the tweet into one of our cities.
    We use a slightly looser bounding box than in the actual twitter request
    @param coords: the coordinates to search
    @return: The city name if found or else None
    """
    for l in places:
        box = np.array(places[l]['loose_box'])
        if (coords[0] > box[0] and coords[1] > box[1]
            and coords[0] < box[2] and coords[1] < box[3]):
            return l
    return None


def fetchsamples():
    """
    Handles the request to the twitter statuses stream and storing tweets into
    the mongodb
    """
    client = MongoClient()
    db = client[db_name]
    tweets = db.tweets

    url_stream = "https://stream.twitter.com/1/statuses/filter.json"
    locations = []
    for place in places:
        locations += places[place]['coords']
    locations = ",".join(['%.3f' % c for c in locations])

    parameters = {'locations': locations}
    response = twitterreq(url_stream, "GET", parameters)

    for line in response:
        line = json.loads(line)
        if line['lang'] in languages:
            if (line['coordinates'] is not None
                            and str(line['coordinates']['type']) == 'Point'):
                place = locate(line['coordinates']['coordinates'])
                if place is not None:
                    line['place'] = place
                    post_id = tweets.insert(line)
                    print '%12s\t%s\t%s' % (place, line['created_at'],
                                          line['text'])

if __name__ == '__main__':
    fetchsamples()
