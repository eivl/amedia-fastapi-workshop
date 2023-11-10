import fastapi
import uvicorn

from starlette.staticfiles import StaticFiles

from api import weather_api
from auth import user_token
from views import home


api = fastapi.FastAPI()


def configure_routing():
    """
    Configure routing and include routers.
    :return:
    """
    api.include_router(home.router)
    api.include_router(weather_api.router)
    api.include_router(user_token.router)

def configure():
    """
    Configure the application. Setup routing and mount static files.
    :return:
    """
    configure_routing()
    api.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host="127.0.0.1")
else:
    configure()
