from datetime import datetime, timedelta
from typing import Annotated

import fastapi
import uvicorn
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from starlette.staticfiles import StaticFiles

from auth.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from auth.context import oauth2_scheme, pwd_context
from auth.fake_user_db import fake_users_db
from auth.password import verify_password, get_password_hash

from api import weather_api
from auth.user_management import authenticate_user, get_current_active_user
from views import home

from models.user import User, UserInDB
from models.token import Token, TokenData

api = fastapi.FastAPI()


def configure_routing():
    api.include_router(home.router)
    api.include_router(weather_api.router)
    api.mount(
        '/static',
        StaticFiles(directory='static'),
        name='static')


def configure():
    configure_routing()


if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()
