#!/usr/bin/env python
"""
various utility functions
@author: Chris Hausler
"""

import numpy as np


def locate_tweet(places, tweet):
    """
    If the tweet has coordinates and they are in one of the target places,
    update the tweet with the place field and return, otherwise return None
    """
    if (tweet['coordinates'] is not None
                            and str(tweet['coordinates']['type']) == 'Point'):
        place = locate(places, tweet['coordinates']['coordinates'])
        if place is not None:
            tweet['place'] = place
            return tweet
    return None



def locate(places, coords):
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
