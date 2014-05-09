import urllib
import json

class TipdogeApi:
    def __init__(self,apikey):
        self.server = "http://tipdoge.info/api/?q="
        self.apikey = apikey

    def getBalance(self,twitterId):
        # Set up the arguments for the REST call.
        args = ({
            'apikey': self.apikey,
            'id': twitterId
        })
        # Make the request and verify success.
        url = self.server + 'getbalance&' + urllib.urlencode(args)
        print url
        s = urllib.urlopen(url).read()
        print s
        return json.loads(s)
                    
    def getAmountTippedToUser(self,twitterId):
        # Set up the arguments for the REST call.
        args = ({
            'apikey': self.apikey,
            'id': twitterId
        })
        # Make the request and verify success.
        url = self.server + 'getAmountTippedToUser&' + urllib.urlencode(args)
        s = urllib.urlopen(url).read()
        return json.loads(s)

