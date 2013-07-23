#!/usr/bin/env python
"""
This grabs all tweets marked with a location in the config file and stores them
in the database

Stolen from the Data Science Course @coursera and modified
@author: Chris Hausler
"""
import json
from config import languages, places, db_name
from utils import locate_tweet
from pymongo import MongoClient
from twitter_helper import locationstream


def fetchlocationstream():
    """
    Handles the request to the twitter statuses stream and storing tweets into
    the mongodb
    """
    client = MongoClient()
    db = client[db_name]
    tweets = db.tweet_stream
    stream = locationstream(places)

    for line in stream:
        line = json.loads(line)
        if line['lang'] in languages:
            tweet = locate_tweet(places, line)
            if tweet is not None:
                _ = tweets.insert(tweet)
                print '%12s\t%s\t%s' % (tweet['place'], tweet['created_at'],
                                  tweet['text'])

if __name__ == '__main__':
    fetchlocationstream()
