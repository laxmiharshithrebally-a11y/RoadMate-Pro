"""
Weather Module — RoadMate Pro
Fetches live weather data for cities using OpenWeatherMap API.
Falls back to realistic mock data if API key is not set.
"""

import requests
import os

# Set your free API key here OR set environment variable WEATHER_API_KEY
# Get free key at: https://openweathermap.org/api (takes 2 mins, free tier = 1000 calls/day)
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'demo')

# ── MOCK DATA for demo / when no API key ────────────────────────────────────
MOCK_WEATHER = {
    'hyderabad':         {'temp': 32, 'feels_like': 35, 'description': 'Partly Cloudy',   'humidity': 55, 'wind': 3.2, 'icon': '02d'},
    'mumbai':            {'temp': 30, 'feels_like': 34, 'description': 'Humid & Hazy',     'humidity': 78, 'wind': 4.5, 'icon': '50d'},
    'delhi':             {'temp': 28, 'feels_like': 30, 'description': 'Clear Sky',         'humidity': 42, 'wind': 2.8, 'icon': '01d'},
    'bangalore':         {'temp': 24, 'feels_like': 25, 'description': 'Pleasant & Clear',  'humidity': 60, 'wind': 2.1, 'icon': '01d'},
    'chennai':           {'temp': 34, 'feels_like': 38, 'description': 'Hot & Sunny',       'humidity': 70, 'wind': 5.0, 'icon': '01d'},
    'kolkata':           {'temp': 33, 'feels_like': 36, 'description': 'Mostly Cloudy',     'humidity': 72, 'wind': 3.6, 'icon': '04d'},
    'jaipur':            {'temp': 35, 'feels_like': 38, 'description': 'Sunny & Dry',       'humidity': 30, 'wind': 2.5, 'icon': '01d'},
    'ahmedabad':         {'temp': 36, 'feels_like': 39, 'description': 'Very Hot',          'humidity': 35, 'wind': 3.0, 'icon': '01d'},
    'pune':              {'temp': 27, 'feels_like': 29, 'description': 'Partly Cloudy',     'humidity': 58, 'wind': 2.3, 'icon': '02d'},
    'goa':               {'temp': 29, 'feels_like': 32, 'description': 'Breezy & Sunny',   'humidity': 75, 'wind': 6.0, 'icon': '02d'},
    'shimla':            {'temp': 14, 'feels_like': 12, 'description': 'Cool & Misty',      'humidity': 80, 'wind': 4.0, 'icon': '50d'},
    'manali':            {'temp': 10, 'feels_like':  8, 'description': 'Cold & Clear',      'humidity': 65, 'wind': 3.5, 'icon': '01d'},
    'srinagar':          {'temp': 16, 'feels_like': 14, 'description': 'Cool & Pleasant',   'humidity': 70, 'wind': 2.8, 'icon': '03d'},
    'kochi':             {'temp': 28, 'feels_like': 31, 'description': 'Warm & Humid',      'humidity': 82, 'wind': 4.2, 'icon': '04d'},
    'varanasi':          {'temp': 30, 'feels_like': 33, 'description': 'Warm & Sunny',      'humidity': 50, 'wind': 2.6, 'icon': '01d'},
    'agra':              {'temp': 31, 'feels_like': 34, 'description': 'Hot & Sunny',       'humidity': 45, 'wind': 2.9, 'icon': '01d'},
    'amritsar':          {'temp': 26, 'feels_like': 27, 'description': 'Mild & Clear',      'humidity': 48, 'wind': 3.1, 'icon': '01d'},
    'chandigarh':        {'temp': 25, 'feels_like': 26, 'description': 'Clear Sky',         'humidity': 50, 'wind': 2.4, 'icon': '01d'},
    'mysore':            {'temp': 25, 'feels_like': 26, 'description': 'Pleasant',          'humidity': 62, 'wind': 1.8, 'icon': '02d'},
    'udaipur':           {'temp': 33, 'feels_like': 35, 'description': 'Hot & Dry',         'humidity': 28, 'wind': 2.7, 'icon': '01d'},
    'thiruvananthapuram':{'temp': 30, 'feels_like': 33, 'description': 'Warm & Coastal',    'humidity': 78, 'wind': 5.5, 'icon': '04d'},
    'bhubaneswar':       {'temp': 33, 'feels_like': 36, 'description': 'Hot & Humid',       'humidity': 68, 'wind': 3.4, 'icon': '01d'},
    'guwahati':          {'temp': 29, 'feels_like': 31, 'description': 'Partly Cloudy',     'humidity': 74, 'wind': 2.9, 'icon': '03d'},
    'default':           {'temp': 28, 'feels_like': 30, 'description': 'Partly Cloudy',     'humidity': 55, 'wind': 3.0, 'icon': '02d'},
}

def get_weather(city: str) -> dict:
    city_key = city.strip().lower()

    # ── Try real API if key is set ───────────────────────────────────────────
    if WEATHER_API_KEY and WEATHER_API_KEY != 'demo':
        try:
            url  = (f"https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city},IN&appid={WEATHER_API_KEY}&units=metric&timeout=5")
            resp = requests.get(url, timeout=5).json()
            if resp.get('cod') == 200:
                return {
                    'city':        city.title(),
                    'temp':        round(resp['main']['temp']),
                    'feels_like':  round(resp['main']['feels_like']),
                    'description': resp['weather'][0]['description'].title(),
                    'humidity':    resp['main']['humidity'],
                    'wind':        resp['wind']['speed'],
                    'icon':        resp['weather'][0]['icon'],
                    'live':        True,
                }
        except Exception:
            pass  # Fall through to mock data

    # ── Return mock/demo data ────────────────────────────────────────────────
    data = MOCK_WEATHER.get(city_key, MOCK_WEATHER['default']).copy()
    data['city'] = city.title()
    data['live'] = False
    return data
