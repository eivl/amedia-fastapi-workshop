import datetime
from typing import Optional, Tuple


__cache = {}
lifetime_in_hours = 1.0


def get_weather(
    city: str, state: Optional[str], country: str, units: str
) -> Optional[dict]:
    """
    Get weather data from cache. If the data is older than lifetime_in_hours,
    return None. If the data does not exist, return None. Otherwise, return
    the data.
    :param city: string of city name.
    :param state: optional string of state name as a two char abbreviation.
    :param country:  string of country name as a two char abbreviation.
    :param units: literal of "metric", "standard", or "imperial".
    :return: None or dict of weather data.
    """
    key = create_key(city, state, country, units)
    data = __cache.get(key)

    if not data:
        return None

    dt = datetime.datetime.now() - data["time"]
    if dt / datetime.timedelta(minutes=60) < lifetime_in_hours:
        return data["value"]

    del __cache[key]
    return None


def set_weather(city: str, state: str, country: str, units: str, value: dict):
    """
    Set weather data in cache. If the data already exists, overwrite it.
    clean out old data.
    :param city: string of city name.
    :param state: string of state name as a two char abbreviation.
    :param country: string of country name as a two char abbreviation.
    :param units: literal of "metric", "standard", or "imperial".
    :param value: dict with weather data.
    :return:
    """
    key = create_key(city, state, country, units)
    data = {
        "time": datetime.datetime.now(),
        "value": value,
    }
    __cache[key] = data
    clean_out_data()


def create_key(
    city: str, state: str, country: str, units: str
) -> Tuple[str, str, str, str]:
    """
    Create a key for the cache.
    :param city: string of city name.
    :param state: string of state name as a two char abbreviation.
    :param country: string of country name as a two char abbreviation.
    :param units: literal of "metric", "standard", or "imperial".
    :return: tuple of city, state, country, and units.
    """
    if not city or not country or not units:
        raise Exception("City, country and units are required.")

    if not state:
        state = ""

    return (
        city.strip().lower(),
        state.strip().lower(),
        country.strip().lower(),
        units.strip().lower(),
    )


def clean_out_data():
    """
    Clean out old data from the cache.
    """
    for key, data in list(__cache.items()):
        dt = datetime.datetime.now() - data.get("time")
        if dt / datetime.timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]
