from typing import Optional
from pydantic import BaseModel


class Location(BaseModel):
    """
    Data model for location.
    """
    city: str
    state: Optional[str] = None
    country: str = "US"
