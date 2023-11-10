from typing import Optional


def get_report(city: str,
               state: Optional[str],
               country: str,
               units: str):
    if state:
        query = f'{city},{state},{country}'
    else:
        query = f'{city},{country}'

    api_key = '123'

    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    url = f'{api_url}?q={query}&appid={api_key}?units={units}'
