from api_calls import *

from flask import Flask, redirect, url_for, render_template, request, session, flash
from pymongo import MongoClient


app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

mongo_connection_string = open("./API/mongo_connection_string.txt", "r")
cstring = mongo_connection_string.read()
mongo_connection_string.close()
cluster = MongoClient(cstring)
db = cluster["Dashboard"]
collection = db["Dashboard"]
delta_check = timedelta(minutes=15)


def kelvin_to_celsius(num):
	return int(num - 273.15)


def format_temperatures(weather):

	temps = {
		"temp": kelvin_to_celsius(weather["temperatures"]["temp"]),
		"min": kelvin_to_celsius(weather["temperatures"]["min"]),
		"max": kelvin_to_celsius(weather["temperatures"]["max"])
	}
	return temps


@app.route("/")
def home():

	weather = collection.find_one({"_id":0})["weather"]
	events = collection.find_one({"_id":0})["events"]

	if events:
		for event in events:
			if event["colour"] == '1':
				event["colour"] ="#7986cb" #lavender
			elif event["colour"] == '2':
				event["colour"] ="#33b679" #sage
			elif event["colour"] == '3':
				event["colour"] ="#8e24aa" #grape
			elif event["colour"] == '4':
				event["colour"] ="#e67c73" #flamingo
			elif event["colour"] == '5':
				event["colour"] ="#f6bf26" #banana
			elif event["colour"] == '6':
				event["colour"] ="#f4511e" #tangerine
			elif event["colour"] == '7':
				event["colour"] ="#039be5" #peacock
			elif event["colour"] == '8':
				event["colour"] ="#616161" #graphite
			elif event["colour"] == '9':
				event["colour"] ="#3f51b5" #blueberry
			elif event["colour"] == '10':
				event["colour"] ="#0b8043" #basil
			elif event["colour"] == '11':
				event["colour"] ="#d50000" #tomato

	return render_template("index.html", temperatures=format_temperatures(weather), conditions=weather["condition"], events=events)


if __name__ == "__main__":
	print("SERVER START!")
	app.run(debug=False, host="localhost", port=80)
	print("SERVER CLOSED!")
