import datetime
from typing import Optional, Tuple


__cache = {}
lifetime_in_hours = 1.0


def get_weather(city: str, state: Optional[str], country: str, units: str):
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
    key = create_key(city, state, country, units)
    data = {
        "time": datetime.datetime.now(),
        "value": value,
    }
    __cache[key] = data
    clean_out_data()


def create_key(city: str, state: str, country: str, units: str):
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
    for key, data in list(__cache.items()):
        dt = datetime.datetime.now() - data.get("time")
        if dt / datetime.timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]
