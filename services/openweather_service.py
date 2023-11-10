from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('OPEN_WEATHERMAP_API')

def get_report(city: str,
               state: Optional[str],
               country: str,
               units: str):
    if state:
        query = f'{city},{state},{country}'
    else:
        query = f'{city},{country}'


    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    url = f'{api_url}?q={query}&appid={API_KEY}?units={units}'
