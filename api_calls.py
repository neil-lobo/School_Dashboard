import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import *
import requests
import json

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def callCalenderAPI():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    today_events = []

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start.split("T"), event['summary'], event["colorId"])
        event_date = start.split("T")[0].split("-")
        # print(event_date)

        dt = datetime.today()
        if (str(dt.year) == event_date[0] and str(dt.month) == event_date[1] and str(dt.day) == event_date[2]):
            # if (event_date[2] == '25'):
            print("added todays event")
            colour = None

            try:
                colour = event["colorId"]
            except:
                colour = '7'

            today_events.append(
                {"datetime": {"date": start.split("T")[0], "time": start.split("T")[1]}, "event": event['summary'],
                 "colour": colour})

        if not today_events:
            today_events = None
    return today_events


def callIpAPI():
    # ip api call max: unlimited
    ip_url = "https://api.ipify.org"
    ip = requests.get(ip_url).text
    return ip


def callLocatoinAPI(ip):
    # location api call max: 10,000 calls/month = 328 calls/day
    location_key = open("./API/ipstack_geolocation_key.txt", "r")
    key = location_key.read()
    location_key.close()

    latlong_url = "http://api.ipstack.com/{}?access_key={}".format(ip, key)
    latlong = json.loads(requests.get(latlong_url).text)
    return latlong


def callWeatherAPI(latlong):
    # latlong = {"latitude": 43.26, "longitude": -79.92}
    # weather api call max: 60 calls/hour = 1,440 calls/day
    weather_key = open("./API/openweathermap_key.txt", "r")
    key = weather_key.read()
    weather_key.close

    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}".format(
        latlong["latitude"], latlong["longitude"], key)
    current_weather = json.loads(requests.get(current_weather_url).text)
    weather_conditions = [{}]
    for i in range(len(current_weather["weather"])):
        weather_conditions[i]["main"] = current_weather["weather"][i]["main"]
        weather_conditions[i]["description"] = current_weather["weather"][i]["description"]
        weather_conditions[i]["icon"] = current_weather["weather"][i]["icon"]

    current_weather = {
        "condition": weather_conditions,
        "temperatures": {
            "temp": current_weather["main"]["temp"],
            "min": current_weather["main"]["temp_min"],
            "max": current_weather["main"]["temp_max"]
        }
    }

    return current_weather
