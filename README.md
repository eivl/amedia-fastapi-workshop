# Amedia FastAPI Workshop

## Openweathermap api key
rename sample.env to .env and add your own key from
https://home.openweathermap.org/api_keys

##
```bash
poetry install

poetry run python main.py
# or
poetry run uvicorn main:app --reload
# or
poetry run ... # your webserver here. e.g. gunicorn
```
