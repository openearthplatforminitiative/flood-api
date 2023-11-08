from typing import Annotated
from datetime import date

from fastapi import Depends, Query


def coordinates(
    lon: Annotated[
        float,
        Query(description="Longitude of the coordinate to retrieve data for"),
    ],
    lat: Annotated[
        float,
        Query(description="Latitude of the coordinate to retrieve data for"),
    ],
) -> (float, float):
    return lon, lat


CoordinatesDep = Annotated[tuple[float, float], Depends(coordinates)]


def date_range(
    start_date: Annotated[
        date | None,
        Query(
            description="Inclusive lower bound for the range of dates to return data for. If omitted the date range "
            "will not have a lower bound"
        ),
    ] = None,
    end_date: Annotated[
        date | None,
        Query(
            description="Inclusive upper bound for the range of dates to return data for. If omitted the date range "
            "will not have an upper bound"
        ),
    ] = None,
) -> (date, date):
    if start_date is None:
        start_date = date.min
    if end_date is None:
        end_date = date.max
    return start_date, end_date


DateRangeDep = Annotated[tuple[date, date], Depends(date_range)]
