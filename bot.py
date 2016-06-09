from flask import Flask
from datetime import datetime
import requests
import time
import json


app = Flask(__name__)
api_key = '2b36c7eb96dc4b60c8788a693c2b3cc0'
url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=Montreal&APPID={api_key}'.format(api_key=api_key)


class Weather(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

@app.route('/weather', methods=['POST'])
def get_weather():
    r = requests.get(url)
    post_mattermost(r.json())
    return

def post_mattermost(data):
    days = []
    for day in data['list']:
        day_weekday = datetime.fromtimestamp(day['dt']/1000).strftime("%A")
        day_month = datetime.fromtimestamp(day['dt']/1000).strftime("%b")
        day_day = datetime.fromtimestamp(day['dt']/1000).strftime("%d")
        day_info_date = """{weekday}, {month}. {day_number}""".ljust(25).format(weekday=day_weekday, month=day_month, day_number=day_day)
        print(day_info_date)
        day_desc = day['weather'][0]['description']
        print(day_desc)
        day_temp_high = int(day['temp']['max'] - 273.15)
        print(day_temp_high)
        day_temp_low = int(day['temp']['min'] - 273.15)
        print(day_temp_low)
        days.append
        print(day['dt'])

    payload = {"response_type": "in_channel", "text": """
               ---
               #### Weather in Montreal, Quebec for the next few days

               | Day                 | Description                      | High   | Low    |
               |:--------------------|:---------------------------------|:-------|:-------|
               | Monday, Feb. 15     | Cloudy with a chance of flurries | 3 °C   | -12 °C |
               | Tuesday, Feb. 16    | Sunny                            | 4 °C   | -8 °C  |
               | Wednesday, Feb. 17  | Partly cloudly                   | 4 °C   | -14 °C |
               | Thursday, Feb. 18   | Cloudy with a chance of rain     | 2 °C   | -13 °C |
               | Friday, Feb. 19     | Overcast                         | 5 °C   | -7 °C  |
               | Saturday, Feb. 20   | Sunny with cloudy patches        | 7 °C   | -4 °C  |
               | Sunday, Feb. 21     | Partly cloudy                    | 6 °C   | -9 °C  |
               ---
               """}

    requests.post(mattermostUrl, data=json.dumps(payload), verify=False)

if __name__ == '__main__':
    app.run(debug=True)

