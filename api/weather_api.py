from typing import Optional, Literal
import fastapi
from fastapi import Depends

from models.location import Location
from models.validation_error import ValidationError
from services import openweather_service

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(
    loc: Location = Depends(),
    units: Literal["metric", "standard", "imperial"] = "metric",
) -> dict | fastapi.Response:
    """
    Get weather data for a city. Currently only one service provider is
    implemented, hence the lack of a provider parameter. If more
    providers are added, the provider parameter will be added and the
    units literal needs to be changed.
    :param loc: Data model for location.
    :param units: "metric", "standard", "imperial"
    :return: dict with weather data or fastapi.Response with error message.
    """
    try:
        report = await openweather_service.get_report(
            loc.city, loc.state, loc.country, units
        )
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    return report
