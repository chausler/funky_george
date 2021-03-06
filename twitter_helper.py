#!/usr/bin/env python
"""
Utils for sending requests to twitter
Stolen from the Data Science Course @coursera and modified
@author: Chris Hausler
"""

import oauth2 as oauth
import urllib2 as urllib
from config import db_name
from pymongo import MongoClient

client = MongoClient()
db = client[db_name]

# load twitter authentication details
access_token_key = db.config.find_one({'name': 'access_token_key'})['value']
access_token_secret = db.config.find_one(
                                    {'name': 'access_token_secret'})['value']
consumer_key = db.config.find_one({'name': 'consumer_key'})['value']
consumer_secret = db.config.find_one({'name': 'consumer_secret'})['value']

client.close()

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


def locationstream(places):
    url_stream = "https://stream.twitter.com/1/statuses/filter.json"
    locations = []
    for place in places:
        locations += places[place]['coords']
    locations = ",".join(['%.3f' % c for c in locations])

    parameters = {'locations': locations}
    response = twitterreq(url_stream, "GET", parameters)
    return response


def usertimeline(screen_name, since_id=None, max_id=None):

    url_stream = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    parameters = {'screen_name': screen_name}
    if since_id is not None:
        parameters['since_id'] = since_id
    if max_id is not None:
        parameters['max_id'] = max_id

    response = twitterreq(url_stream, "GET", parameters)
    return response
