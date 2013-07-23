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
                'value': '1580422783-Vb9t2wcyA0SxxDRRolT95RhH9SOa544xKzSgaTh'})
db.config.insert({'name': 'access_token_secret',
                'value': 'yRztjyIS1k6H3SiKcN8XgvllR8mqedNI20EJmzt444'})
db.config.insert({'name': 'consumer_key',
                'value': 'AsW1u6F6JrxqPE5ZREWRiQ'})
db.config.insert({'name': 'consumer_secret',
                 'value': 'OIgNF22tnaJjonfNsMt1sJAgltrbEDlvOlVjGEHMs'})
