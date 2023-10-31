from typing import Annotated
from datetime import date

from fastapi import Depends


def coordinates(lat: float, lon: float) -> (float, float):
    return lat, lon


CoordinatesDep = Annotated[tuple[float, float], Depends(coordinates)]


def date_range(
    start_date: date | None = None,
    end_date: date | None = None,
) -> (date, date):
    if start_date is None:
        start_date = date.min
    if end_date is None:
        end_date = date.max
    return start_date, end_date


DateRangeDep = Annotated[tuple[date, date], Depends(date_range)]
