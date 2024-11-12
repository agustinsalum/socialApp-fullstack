
import requests

def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # To get the temperature in degrees Celsius
    }
    response = requests.get(base_url, params=params)
    # response.url (Print the request URL)
    # response.status_code (Print the response status code)
    # response.json() (Print the response content)
    if response.status_code == 200:
        return response.json()
    else:
        return None