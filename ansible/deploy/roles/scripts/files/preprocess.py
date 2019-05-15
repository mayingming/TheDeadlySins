# The app is using for pre-processing twitter data filtering metadata,
# preserving useful data and adding features for every tweet
# Author: Group 10

from shapely.geometry import shape, Point
import re
import json

# Key tokens used for analyze
token_list = [" eat", "drink", "food", "money", "greedy", "luxury", "much more", "desire", "eager", " ate", "income"]

# cities.json contains the geometry of 75 cities in VIC
with open('cities.json') as f:
    js = json.load(f)

# Keep logging the error messages for debug
log = 'log_pre_process.log'
logfile = open(log, "a")


# The function is used to check if the given geocode is located
# in the given cities in cities.json
def get_city(point):
    userpoint = Point(point[0],point[1])
    for city in js:
        polygon = shape(js[city]['geometries'][0])
        if polygon.contains(userpoint):
            return city


# The function is used to find if there are key tokens in the text field
# If any of the tokens exists, then the exist returns True
def preprocess(text):
    exist = False
    tokens = {}
    for token in token_list:
        occurences = re.findall(token, text)
        if len(occurences)>0:
            tokens.update({token: True})
            exist = True
        else:
            tokens.update({token: False})
    return tokens, exist


# The function is used to get the langtitude and latitude from the tweet
# If tweet have only the bounding box, we calculate the centre of it and then put it in the geo.
def get_location(line):
    geo = []
    try:
        if 'geo' in line and line['geo'] is not None and 'coordinates' in line['geo'] \
                and line['geo']['coordinates'] is not None:
            x = line['geo']['coordinates'][0]
            y = line['geo']['coordinates'][1]
            geo = [x, y]
        elif 'bounding_box' in line['place'] and'coordinates' in line['place']['bounding_box']:
            x = (line['place']['bounding_box']['coordinates'][0][0][0]+line['place']['bounding_box']['coordinates'][0][2][0])/2
            y = (line['place']['bounding_box']['coordinates'][0][0][1]+line['place']['bounding_box']['coordinates'][0][1][1])/2
            geo = [x, y]
    except Exception as e:
        logfile.write(str(e) + "\n")
    return geo


# If the tweet does not have geo location, return False since we are not
# going to use it for analyze
# If the tweet has geo location, we return reformatted tweet for future analze
def transfer(sjson):
    point = get_location(sjson)
    if len(point) == 0:
        return False
    twitter = {}
    twitter.update({"geo": get_location(sjson)})
    twitter.update({"_id": sjson["id_str"]})
    twitter.update({"text": sjson["text"]})
    token, exist = preprocess(sjson["text"])
    twitter.update({"feature": token})
    twitter.update({"location": get_city(point)})
    twitter.update({"exist": exist})
    return twitter
