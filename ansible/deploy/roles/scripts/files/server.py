# The purpose of the app is streaming tweets via twitter API within Australia area
# Then send the username to another instance to crawling tweets via user timeline
# Author: Group 10

import socket
import tweepy
import sys
import time


# Create socket and waiting for connection
sk = socket.socket()
sk.bind(("127.0.0.1", 5985))
sk.listen(5)
conn1, address1 = sk.accept()
conn2, address2 = sk.accept()
print(conn1, address1)
print(conn2, address2)

# User1 App1 API token and keys
# Authentication information
consumer_key = "ZRTsOoNV2NwOh2iZNwBhxzjrW"
consumer_secret = "7UEKPYpACap1Rc1aCw8WW3DdzJeAhva7xMwgkQUZ8ml37YVyMJ"
access_token = "1007227735968702464-ucauMgzZpffO6uZ3XeWZmmDrTD3vPz"
access_token_secret = "ZHOP1UpGvJsT1KJSUpaZSNizNcqzvjpolMAFuMn31Aryp"

# Access to the endpoint and input authentication information
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Geo code for Australia area
AUS_GEO_CODE = [113.03, -39.06, 154.73, -12.28]


# Streaming tweets via twitter API within Australia area
# Send the username to another instance for continuing collecting data
while True:

    class MyStreamListener(tweepy.StreamListener):

        count = True

        def on_status(self, status):
            sjson = status._json
            user = sjson["user"]["screen_name"]
            if MyStreamListener.count:
                conn1.sendall(bytes(user, encoding="utf-8"))
                MyStreamListener.count = False
            else:
                conn2.sendall(bytes(user, encoding="utf-8"))
                MyStreamListener.count = True

        def on_error(self, status_code):
            if status_code == 420:
                self.on_timeout()
            print(sys.stderr, 'Encountered error with status code:', status_code)
            return True  # Don't kill the stream

        def on_timeout(self):
            time.sleep(600)
            return  # Don't kill the stream


    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(locations=AUS_GEO_CODE)