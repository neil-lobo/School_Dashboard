from api_calls import *
from pymongo import MongoClient
import json
import time

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

mongo_connection_string = open("./API/mongo_connection_string.txt", "r")
cstring = mongo_connection_string.read()
mongo_connection_string.close()
cluster = MongoClient(cstring)
db = cluster["Dashboard"]
collection = db["Dashboard"]
delta_check = timedelta(minutes=10)
delta_calender_check = timedelta(minutes=1)
# delta_location_check = timedelta(minutes=60)


def main():
	ip = None
	location = None
	weather = None
	last_calender_update = datetime.today()

	while True:

		time.sleep(0.5)

		dt = datetime.today()
		db_dt = collection.find_one({"_id": 0})["datetime"]
		db_dt = datetime(year=db_dt["year"], month=db_dt["month"], day=db_dt["day"], hour=db_dt["hour"], minute=db_dt["minute"], second=db_dt["second"])

		if abs(dt - last_calender_update) > delta_calender_check:
			events = callCalenderAPI()
			collection.find_one_and_update({"_id": 0}, {"$set": {"events": events}})
			last_calender_update = dt
			print("EVENT DATABASE UPDATED!")

		if abs(dt - db_dt) > delta_check:
			ip = callIpAPI()
			location = callLocatoinAPI(ip)
			weather = callWeatherAPI(location)
			events = callCalenderAPI()

			new_db_dt = {"year": dt.year, "month": dt.month, "day": dt.day, "hour": dt.hour, "minute": dt.minute, "second": dt.second}

			collection.find_one_and_update({"_id": 0}, {"$set": {"weather": weather}})
			collection.find_one_and_update({"_id":0}, {"$set":{"datetime": new_db_dt}})
			collection.find_one_and_update({"_id": 0}, {"$set": {"events": events}})
			last_calender_update = dt

			print("DATABASE UPDATED!")
		
		print(abs(delta_check - abs(dt-db_dt)))


if __name__ == "__main__":
	main()