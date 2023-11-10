from datetime import timedelta, datetime
from typing import Annotated
import fastapi

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from auth.fake_user_db import fake_users_db
from auth.user_management import get_current_active_user, authenticate_user
from models.token import Token
from models.user import User


router = fastapi.APIRouter()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token with the given data and expiration time.
    :param data: dict of data to encode.
    :param expires_delta: timedelta of expiration time. Defaults to
    ACCESS_TOKEN_EXPIRE_MINUTES.
    :return: string of JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> dict:
    """
    Get a JWT token for the user. If the user does not exist or the
    password is incorrect, raise an exception.
    :param form_data: OAuth2PasswordRequestForm with username and password.
    :return: dict with JWT token.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Example endpoint to limit access to authenticated users.
    :param current_user: User instance, injected by Depends.
    :return: instance of User.
    """
    return current_user
