import requests
import config
from helpers import constants
from models.weather import Weather


class WeatherManager(object):
    url = f"http://api.weatherapi.com/v1/current.json"
    payload = {"key": config.weather_api_key}

    def __init__(self, city=None, lang=None):
        self.payload["q"] = constants.weather_city if not city else city
        self.payload["lang"] = constants.weather_lang if not lang else lang

    def request(self):
        weather_data = requests.get(url=self.url, params=self.payload).json()
        weather = Weather(weather_data)
        return weather
