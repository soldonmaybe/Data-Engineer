# def keys
bearer_token = r'AAAAAAAAAAAAAAAAAAAAAELuegEAAAAAcCUcFpnbVW4pt95lMZZ3xrNuTLQ%3DPxnK3Zs5gOMwRXpDBmwqZNxEhrfta0r7cgRK6smPaJd9w265T8'
api_key = 'csMXTrxkWJvnRMvy7SmkBrNwa'
api_secret = '80jU1i6jLvBC0tFqJZhNHuYgjwTyqGGKzKRp50yRzdJiic1H7K'
access_token = '223026744-WEMrzubOKlh9MvxuuFR7NLE5qQaJW1prhujcPuzK'
access_secret = 'ZLhjdWTEGbe2Gb1ZQAtCAItT35f18HkOyerJaJPx7ouU0'

# import dependencies
from confluent_kafka import Producer
from faker import Faker
import json
import time
import logging
import random
import tweepy

# def tweepy
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_secret)
auth = tweepy.OAuth1UserHandler (api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)
search = ['valorant league', 'valorant franchising']

# def logging
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# def producer
p=Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer has been initiated...')

# def receipt
def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)
        
# def stream tweet
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        if tweet.referenced_tweets == None:
            # print(tweet.text)
            p.poll(1)
            p.produce('twt_streaming', tweet.text, callback=receipt)
            p.flush()
            time.sleep(0.2)
    def on_connect(self):
        print('Connected')

# def instance
stream = MyStream(bearer_token= bearer_token)

for term in search:
    stream.add_rules(tweepy.StreamRule(term))

stream.filter(tweet_fields=["referenced_tweets"])
