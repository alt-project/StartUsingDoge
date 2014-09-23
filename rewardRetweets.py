from twython import Twython, TwythonError
from tipdoge import TipdogeApi
from tweetfactory import TweetFactory
from sentiment140 import Sentiment140
import ConfigParser, os,sys
import time
import logging, json
import random
import datetime

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

config = ConfigParser.ConfigParser()
config.read('config.cfg')
APP_KEY = config.get('Tweet', 'consumer_key')
APP_SECRET = config.get('Tweet', 'consumer_secret')
OAUTH_TOKEN = config.get('Tweet', 'access_key')
OAUTH_TOKEN_SECRET = config.get('Tweet', 'access_secret')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

if len(sys.argv) > 1:
  tweet_ids = [int(sys.argv[1])]
else:
  tweet_ids = [int(f.replace(".json","")) for f in os.listdir('db')]

tweet_ids = list(reversed(tweet_ids))

print "rewarding tweets:", tweet_ids

from math import sqrt


from dateutil.parser import parse

import pprint
pp = pprint.PrettyPrinter(indent=4)

while True:

  for orig_tweet_id in tweet_ids:
    store = 'db/%s.json' % orig_tweet_id
    if os.path.exists(store):
      memo = json.loads(open(store).read())
    else:
      memo = {}
    
    orig_tweet = twitter.show_status(id=orig_tweet_id)
    tweet_age = max((datetime.datetime.now() - parse(orig_tweet['created_at']).replace(tzinfo=None)).days, 1)

    try:
        #get retweets to a specific tweet.
        search_results = twitter.get_retweets(id=orig_tweet_id, count=100)
    except TwythonError as e:
        print e
        search_results = []
    print len(search_results)
    
    for tweet in search_results:
        logging.info("retweeted by @" + str(tweet['user']['screen_name']) + " " + str(tweet[u'user'][u'followers_count']))
        age = (datetime.datetime.now() - parse(tweet['user']['created_at']).replace(tzinfo=None)).days
        freq = tweet[u'user'][u'statuses_count'] / (age or 1)

        if memo.has_key(tweet['user']['screen_name']):
            logging.info('already rewarded.')
            continue
        else:
            reward = min(max(int(tweet[u'user'][u'followers_count'] * 0.5), 20), 9 * int(sqrt(tweet[u'user'][u'followers_count'])))
            if freq > 25:
              reward = reward / 3 
            if freq > 50:
              reward = reward / 2 
            if age > 50:
              reward += 2 ** random.randint(2,6)
            if age > 300:
              reward += 15
            reward = reward / tweet_age
            reward = max(reward, 10)
            tweet_text= "@tipdoge tip @" + tweet[u'user'][u"screen_name"] + " %s - thanks! see tipdoge.info for instructions on how to use your Dogecoin!" % reward

            logging.info(tweet_text)
            try:
              twitter.update_status(status=tweet_text.encode('UTF-8'), in_reply_to_status_id=str(tweet["id"]).encode('UTF-8'))
            except TwythonError, e:
              print e
            memo[tweet['user']['screen_name']] = 1
            open(store,'w').write(json.dumps(memo))
            time.sleep(10)

    time.sleep(100)
