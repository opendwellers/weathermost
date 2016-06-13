from flask import Flask
from datetime import datetime
import configparser 
import requests
import time
import json


app = Flask(__name__)
url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Montreal&APPID={key}".format
mattermost_url = ""

def init():
   global url
   global mattermost_url
   Config = configparser.ConfigParser()
   Config.read("configuration/config")
   Config.sections()

   config_api_key = Config.get('OpenWeather', 'api_key')
   url = url(key=config_api_key)

   mattermost_url = Config.get('Mattermost', 'url')


class Weather(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

@app.route('/weather', methods=['POST'])
def get_weather():
    r = requests.get(url)
    post_mattermost(r.json())
    return

def get_embedded_icon_url(icon_code, desc):
    return '![desc](http://openweathermap.org/img/w/{code}.png) "{desc}"'.format(code=icon_code, desc=desc)

def get_day_weather_line(day):
    """Return a markdown formatted line for a weather day"""
    day_weekday = datetime.fromtimestamp(day['dt']/1000).strftime("%A")
    day_month = datetime.fromtimestamp(day['dt']/1000).strftime("%b")
    day_day = datetime.fromtimestamp(day['dt']/1000).strftime("%d")
    day_info_date = """{weekday}, {month}. {day_number}""".ljust(25).format(weekday=day_weekday, month=day_month, day_number=day_day)
    #print(day_info_date)
    day_desc = day['weather'][0]['description']
    day_desc.ljust(50)
    #print(day_desc)
    day_temp_high = int(day['temp']['max'] - 273.15)
    #print(day_temp_high)
    day_temp_low = int(day['temp']['min'] - 273.15)
    #print(day_temp_low)
    day_icon = get_embedded_icon_url(day['weather'][0]['icon'], day_desc)
    return "| {day_info_date_param} | {desc_param} | {day_temp_high_param} °C | {day_temp_low_param} °C ".format(day_info_date_param=day_info_date, desc_param=day_desc, day_temp_high_param=day_temp_high, day_temp_low_param=day_temp_low)


def post_mattermost(data):
    days = []
    for day in data['list']:
        print(get_day_weather_line(day))

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

    requests.post(mattermost_url, data=json.dumps(payload), verify=False)

if __name__ == '__main__':
    init()
    app.run(debug=True)

