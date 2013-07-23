
from twitter_helper import usertimeline
from pymongo import MongoClient, DESCENDING, ASCENDING
import json
from config import db_name
from sentiment import sentiment

def get_user_timeline_tweets(screen_name, max_id=None, since_id=None):
    client = MongoClient()
    db = client[db_name]
    tweets = db.tweet_user
    new_tweets = True
    while new_tweets:
        stream = usertimeline(screen_name, max_id=max_id, since_id=since_id)
        for line in stream:
            if line == '[]':
                print 'no tweets'
                new_tweets = False
                break
            new_tweets = json.loads(line)
            for t in new_tweets:
                sent = sentiment(t['text'])
                t['sentiment'] = sent
                t['screen_name_lower'] = screen_name.lower()
                _ = tweets.insert(t)
                max_id = t['id'] - 1
                print '%d/t%s' % (max_id, t['text'])


def update_sentiment():
    client = MongoClient()
    db = client[db_name]
    tweets = db.tweet_user
    tt = tweets.find({})
    for tweet in tt:
        sent = sentiment(tweet['text'])
        print 'sentiment\t%.2f\t%s' % (sent, tweet['text'])
        tweets.update({'_id': tweet['_id']}, {'$set':  {'sentiment': sent}},
                      upsert=False, multi=False)


def update_user_timeline(screen_name):
    client = MongoClient()
    db = client[db_name]
    tweets = db.tweet_user

    newest = None
    oldest = None

    if 'tweet_user' in db.collection_names():
        try:
            for tweet in tweets.find({"screen_name_lower":
                                screen_name.lower()}).sort('id', DESCENDING).limit(1):
                if tweet is not None:
                    newest = tweet['id'] + 1

            for tweet in tweets.find({"screen_name_lower":
                                screen_name.lower()}).sort('id', ASCENDING).limit(1):
                if tweet is not None:
                    oldest = tweet['id'] - 1
        except:
            pass

    # get newest
    if newest is not None:
        get_user_timeline_tweets(screen_name, since_id=newest)
    get_user_timeline_tweets(screen_name, max_id=oldest)


def get_user_timeline(screen_name):
    update_sentiment()
    update_user_timeline(screen_name)
#    client = MongoClient()
#    db = client[db_name]
#    tweets = db.tweet_user
    

if __name__ == '__main__':
    get_user_timeline('AlexSuse')
