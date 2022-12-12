import requests
import os

from dotenv import load_dotenv

load_dotenv()

WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")

BASE_URL = "http://api.weatherapi.com/v1/current.json"

params = {
    "key": WEATHER_TOKEN,
    "q": "Puebla",
    "aqi": "no",
}

def get_weather_data():
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        region = data['location']['name']
        temp_c = data['current']['temp_c']
        return [region, temp_c]
    else:
        # Handle the error and return None
        print(f"An error occurred: {response.status_code}")
        return None
