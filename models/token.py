from pydantic import BaseModel


class Token(BaseModel):
    """
    Data model for token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Data model for token data.
    """
    username: str | None = None
