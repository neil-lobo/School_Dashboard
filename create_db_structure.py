from api_calls import *
from pymongo import MongoClient

mongo_connection_string = open("./API/mongo_connection_string.txt", "r")
cstring = mongo_connection_string.read()
mongo_connection_string.close()

cluster = MongoClient(cstring)
db = cluster["Dashboard"]
collection = db["Dashboard"]

data = {
    "_id": 0,
    "weather": None,
    "datetime": None,
    "events": None
}

collection.insert_one(data)

new_db_dt = {"year": 2000, "month": 1, "day": 1, "hour": 0, "minute": 0, "second": 0}
collection.find_one_and_update({"_id":0}, {"$set":{"datetime": new_db_dt}})

ip = callIpAPI()
location = callLocatoinAPI(ip)
weather = callWeatherAPI(location)
collection.find_one_and_update({"_id": 0}, {"$set": {"weather": weather}})

events = callCalenderAPI()
collection.find_one_and_update({"_id": 0}, {"$set": {"events": events}})
