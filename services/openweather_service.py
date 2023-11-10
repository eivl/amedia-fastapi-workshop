from typing import Optional
from dotenv import load_dotenv
import os
import httpx

from infrastructure import weather_cache
from models.validation_error import ValidationError


load_dotenv()

API_KEY = os.environ.get('OPEN_WEATHERMAP_API')

async def get_report(city: str,
               state: Optional[str],
               country: str,
               units: str):
    try:
        city, state, country, units = validate_units(
            city, state, country, units
        )
    except ValidationError as ve:
        raise ValidationError(error_msg=ve.error_msg, status_code=ve.status_code)

    if forecast := weather_cache.get_weather(city, state, country, units):
        return forecast

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

    weather_cache.set_weather(city, state, country, units, forecast)

    return forecast


def validate_units(city: str,
                   state: Optional[str],
                   country: Optional[str],
                   units: str):

    if not country:
        country = 'us'
    else:
        country = country.strip().lower()

    if len(country) != 2:
        raise ValidationError(
            status_code=400,
            error_msg=f'Invalid country code. It must be a two letter abbreviation.'
        )

    city = city.strip().lower()

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        raise ValidationError(
            status_code=400,
            error_msg=f'Invalid state code. It must be a two letter abbreviation.'
        )

    if units:
        units = units.strip().lower()

    valid_units = 'standard', 'metric', 'imperial'
    if units not in valid_units:
        raise ValidationError(
            status_code=400,
            error_msg=f'Invalid unit.'
        )

    return city, state, country, units
