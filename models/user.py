from pydantic import BaseModel


class User(BaseModel):
    """
    Data model for user.
    """
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """
    Data model for user saved to the database.
    """
    hashed_password: str
