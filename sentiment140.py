import requests
from pprint import pprint
import json
import sys

SENTIMENT = {
    0: 'negative',
    2: 'neutral',
    4: 'positive'
}

class Sentiment140:
    def __init__(self,appid):
        self.host = 'http://www.sentiment140.com/api/bulkClassifyJson?appid=' + appid

    def get_sentiment(self,sentiment_object):
        return sentiment_object[0]["sentiment"]

    def make_request(self, tweets):
        body = {'data': tweets}
        response = requests.post(self.host, data=json.dumps(body))
        data = response.json()['data']
        for tweet in data:
            tweet['sentiment'] = SENTIMENT[tweet['polarity']]
        return data

    def get_mood_of_tweets(self, tweets):
        items = []
        for tweet in tweets:
            items.append({"text": tweet["text"], "query": "dogecoin", "id": tweet["id"]})

        return self.make_request(items)
