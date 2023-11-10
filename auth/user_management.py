from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from auth.constants import SECRET_KEY, ALGORITHM
from auth.context import oauth2_scheme
from auth.fake_user_db import fake_users_db
from auth.password import verify_password
from models.token import TokenData
from models.user import UserInDB, User


def get_user(db: dict, username: str) -> UserInDB:
    """
    Get a user from the database. The database is a dictionary with
    usernames as keys and user data as values.
    :param db: dict of users.
    :param username: string of username.
    :return: instance of UserInDB.
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db: dict, username: str, password: str) -> UserInDB | bool:
    """
    Authenticate a user. If the user exists and the password matches,
    return the user, otherwise return False.
    :param fake_db: dict of users.
    :param username: string of username.
    :param password: string of plaintext password.
    :return: instance of UserInDB or False
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """
    Get the current user from the JWT token. If the token is invalid,
    raise an exception. If the user does not exist in the token, raise
    an exception. If the user does not exist in the database, raise an
    exception.
    :param token: JWT token.
    :return: UserInDB instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Get the current active user. If the user is disabled, raise an
    exception.
    :param current_user: Dependency of current user.
    :return: User instance.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
