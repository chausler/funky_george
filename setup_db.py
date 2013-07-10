#!/usr/bin/env python
"""
load some config values into the database
@author: Chris Hausler
"""
from config import db_name
from pymongo import MongoClient

client = MongoClient()
db = client[db_name]
# required twitter authentication data
db.config.insert({'name': 'access_token_key',
                                   'value': ''})
db.config.insert({'name': 'access_token_secret',
                                   'value': ''})
db.config.insert({'name': 'consumer_key',
                                   'value': ''})
db.config.insert({'name': 'consumer_secret',
                                   'value': ''})
