# The purpose of the app is to connect with instance 1 and receive user name from it
# harvest tweets via user timeline, then put the raw data to raw_result database
# and processed data to final_result database
# Author: Group 10

import socket
import tweepy
import pycouchdb
import preprocess

host = []
fname = 'hosts'
config = open(fname, 'r')
for line in config:
    host.append(line.strip())
config.close()
print(host[1])
print(host[4])

# Connect to the CouchDB database
while True:
    try:
        couch = pycouchdb.Server('http://admin:coconut@' + host[1] + ':5984/')
        # Connect to instance 1 according to IP address and port number
        obj = socket.socket()
        obj.connect((host[4], 5985))
        if obj is not None and couch is not None:
            break
    except:
        couch = None
        obj = None
try:
    raw_db = couch.database('ccc_ass_2')
except:
    raw_db = couch.create('ccc_ass_2')
try:
    db = couch.database('final_result')
except:
    db = couch.create('final_result')



# User2 App1 API token and keys
# Authentication information
consumer_key = "RaHCJytQzL28DoOg11vPm6OQt"
consumer_secret = "ByvDTH5y5tt7gcGb3wSBjlwjguwVPuBRlwa7xkJTYQdPcwwvhY"
access_token = "1127769015684718592-X8GZcq53QrPsDzak2uspMg0SevsK17"
access_token_secret = "fO7Sg7KBz22hL3zwJWNqbEajfFTU1YKN1SVqA01BPMa28"

# Access to the endpoint and input authentication information
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Keep logging the error messages for debug
log = 'log_client.log'
logfile = open(log, "a")

# Keep listening messages from instance 1 and collecting tweets
# via user timeline API for a given user name
# Save raw data to raw_result database
# Pre-process tweets and save them to final_result
while True:
    ret = str(obj.recv(1024), encoding="utf-8")
    print(ret)
    stuff = []
    try:
        stuff = api.user_timeline(screen_name=ret, count=1000, include_rts=True)
    except Exception as e:
        logfile.write(str(e) + "\n")
        logfile.write(ret + "\n")
    for timeline in stuff:
        try:
            raw_db.save(timeline._json)
        except Exception as e:
            logfile.write(str(e) + "\n")
        sjson = preprocess.transfer(timeline._json)
        if sjson:
            try:
                db.save(sjson)
            except Exception as e:
                logfile.write(str(e) + "\n")
                logfile.write(str(sjson) + "\n")
