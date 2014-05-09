from twython import Twython, TwythonError
from tipdoge import TipdogeApi
from tweetfactory import TweetFactory
from sentiment140 import Sentiment140
import ConfigParser, os
import time
import logging


logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

config = ConfigParser.ConfigParser()
config.read('config.cfg')
APP_KEY = config.get('Tweet', 'consumer_key')
APP_SECRET = config.get('Tweet', 'consumer_secret')
OAUTH_TOKEN = config.get('Tweet', 'access_key')
OAUTH_TOKEN_SECRET = config.get('Tweet', 'access_secret')
TIPDOGE_API_KEY =  config.get('Tweet', 'tipdoge_api_key')
SENTIMENT140_API_KEY =  config.get('Tweet', 'sentiment140_api_key')

#initialize all API objects
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
tipdoge = TipdogeApi(TIPDOGE_API_KEY)
sentiment140 = Sentiment140(SENTIMENT140_API_KEY)
tweet_factory = TweetFactory("tweet-template.txt")

tweet_text=tweet_factory.build_tweet()
logging.info(tweet_text)


while True:
    try:
        #search for tweets about dogecoin
        search_results = twitter.search(q='dogecoin', count=50)
    except TwythonError as e:
        print e

    #request the mood for the tweets we just found
    tweet_moods = sentiment140.get_mood_of_tweets(search_results['statuses'])

    print tweet_moods

    for tweet in search_results['statuses']:
        if tweet["text"].startswith('RT'):
            continue #tweet is a RT - skip

        #get the tweet mood for the current tweet
        tweet_mood = sentiment140.get_sentiment(filter(lambda x: x["id"] == tweet["id"], tweet_moods))

        logging.info('New Tweet with Mood "%s" from @%s Date: %s' % (tweet_mood, tweet['user']['screen_name'].encode('utf-8'), tweet['created_at']))
        logging.info(tweet['text'].encode('utf-8'))

        amount_tipped_to_user = tipdoge.getAmountTippedToUser(tweet['user']['id'])
        if amount_tipped_to_user["amount"] is None and tweet_mood == "positive":
            logging.info("new user found who likes to have some coins: @" + str(tweet['user']['screen_name']))
            tweet_text= "@" + tweet['user']["screen_name"] + " " + tweet_factory.build_tweet()
            logging.info(tweet_text)
            twitter.update_status(status=tweet_text.encode('UTF-8'),in_reply_to_status_id=str(tweet["id"]).encode('UTF-8'))
            time.sleep(120)

        logging.info('')

    time.sleep(60)