from typing import Optional
from dotenv import load_dotenv
import os
import httpx

from models.validation_error import ValidationError

load_dotenv()

API_KEY = os.environ.get('OPEN_WEATHERMAP_API')

async def get_report(city: str,
               state: Optional[str],
               country: str,
               units: str):
    if state:
        query = f'{city},{state},{country}'
    else:
        query = f'{city},{country}'


    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    url = f'{api_url}?q={query}&appid={API_KEY}&units={units}'

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
        if response.status_code != httpx.codes.OK:
            raise ValidationError(response.text, status_code=response.status_code)

    data = response.json()
    forecast = data['main']

    return forecast
