import tweepy
import json
import sys

consumer_key = "iFMsWWECY0qiKLVeUmw78I2G5"
consumer_secret = "J3j46WniFmegxt4mgT2N3tmPqDd7XX3lioZb5GOhl8goTlSQnO"
access_token = "1007227735968702464-RYn2pRHJHy6cyT15ozqNjGGlsyOAJF"
access_token_secret = "taerxqVYCkY2cM85CIrN4TVjEzKcdCBVtfmifb3uy7OBp"

AUS_GEO_CODE = [113.03, -39.06, 154.73, -12.28]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        json_str = str(status)
        with open("/Users/mayingming/Desktop/py4e/CCC_Ass2/result.json", "w") as file:
            json.dump(json_str, file)
        print(status)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the streammyStream.filter()
            return False
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True  # Don't kill the stream


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(locations=AUS_GEO_CODE)
