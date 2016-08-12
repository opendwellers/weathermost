from flask import Flask
from flask import Response
from datetime import datetime
import configparser 
import requests
import time
import json


app = Flask(__name__)
url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Montreal&APPID={key}&cnt=5".format

def init():
    """Initializes variables"""
    global url
    Config = configparser.ConfigParser()
    Config.read("configuration/config")
    Config.sections()

    config_api_key = Config.get('OpenWeather', 'api_key')
    url = url(key=config_api_key)


@app.route('/weather', methods=['POST'])
def get_weather():
    """Bot receives a /slash command
    TODO add option to choose city with /weather toronto
    """
    r = requests.get(url)
    payload_text = build_response_text(r.json())
    data = {'text' : payload_text}
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    return resp

def get_embedded_icon_url(icon_code, desc):
    """Returns a formatted markdown line to show the weather icon"""
    return '![desc](http://openweathermap.org/img/w/{code}.png "{desc}")'.format(code=icon_code, desc=desc)

def get_day_weather_line(day):
    """Return a markdown formatted line for a weather day"""
    day_weekday = datetime.fromtimestamp(day['dt']).strftime("%A")
    day_month = datetime.fromtimestamp(day['dt']).strftime("%b")
    day_day = datetime.fromtimestamp(day['dt']).strftime("%d")
    day_info_date = """{weekday}, {month}. {day_number}""".ljust(25).format(weekday=day_weekday, month=day_month, day_number=day_day)
    day_desc = day['weather'][0]['description']
    day_desc.ljust(50)
    day_temp_high = int(day['temp']['max'] - 273.15)
    day_temp_low = int(day['temp']['min'] - 273.15)
    day_icon = get_embedded_icon_url(day['weather'][0]['icon'], day_desc)
    return "| {day_info_date_param} | {desc_param}  {day_icon_param} | {day_temp_high_param} °C | {day_temp_low_param} °C  |\n".format(day_info_date_param=day_info_date, desc_param=day_desc, day_icon_param=day_icon, day_temp_high_param=day_temp_high, day_temp_low_param=day_temp_low)

def build_response_text(data):
    """Post formatted data to mattermost instance"""
    days = []
    payload_text = """
---
### Weather in Montreal, Quebec, for the next few days

| Day | Description | High | Low |
|:---------------------------|:------------------------------------|:--------|:--------|\n"""
    for day in data['list']:
        payload_text += get_day_weather_line(day)
    payload_text += "---"
    print(payload_text)

    return payload_text

if __name__ == '__main__':
    init()
    app.run(debug=True)

