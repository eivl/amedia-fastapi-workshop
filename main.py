import fastapi
import uvicorn

from starlette.staticfiles import StaticFiles

from views import home


api = fastapi.FastAPI()
api.include_router(home.router)

api.mount(
    '/static',
    StaticFiles(directory='static'),
    name='static')




if __name__ == '__main__':
    uvicorn.run(api, port=8000, host='127.0.0.1')
