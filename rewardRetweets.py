from twython import Twython, TwythonError
from tipdoge import TipdogeApi
from tweetfactory import TweetFactory
from sentiment140 import Sentiment140
import ConfigParser, os
import time
import logging, json


logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

config = ConfigParser.ConfigParser()
config.read('config.cfg')
APP_KEY = config.get('Tweet', 'consumer_key')
APP_SECRET = config.get('Tweet', 'consumer_secret')
OAUTH_TOKEN = config.get('Tweet', 'access_key')
OAUTH_TOKEN_SECRET = config.get('Tweet', 'access_secret')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

orig_tweet_id = 483383384660385792 # sys.argv[1]

store = 'db/%s.json' % orig_tweet_id
if os.path.exists(store):
    memo = json.loads(open(store).read())
else:
    memo = {}

while True:
    try:
        #get retweets to a specific tweet.
        search_results = twitter.get_retweets(id=orig_tweet_id)
    except TwythonError as e:
        print e
    

    for tweet in search_results:

        logging.info("retweeted by @" + str(tweet['user']['screen_name']))
        if memo.has_key(tweet['user']['screen_name']):
            logging.info('already rewarded.')
            continue
        else:
            tweet_text= "@tipdoge tip @" + tweet[u'user'][u"screen_name"] + " 100 - Just testing the twitter API. Keep the Doge!"
            logging.info(tweet_text)
            twitter.update_status(status=tweet_text.encode('UTF-8'))
            memo[tweet['user']['screen_name']] = 1
            open(store,'w').write(json.dumps(memo))
            time.sleep(120)

    time.sleep(60)
