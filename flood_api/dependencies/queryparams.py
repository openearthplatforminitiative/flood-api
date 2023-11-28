from datetime import date
from typing import Annotated, Optional

from fastapi import Depends, Query


def coordinates(
    lon: Annotated[
        float | None,
        Query(description="Longitude of the coordinate to retrieve data for"),
    ] = None,
    lat: Annotated[
        float | None,
        Query(description="Latitude of the coordinate to retrieve data for"),
    ] = None,
) -> Optional[tuple[float, float]]:
    if all([lat, lon]):
        return (lat, lon)
    return None


CoordinatesDep = Annotated[Optional[tuple[float, float]], Depends(coordinates)]


def bounding_box(
    min_lat: Annotated[
        float | None,
        Query(
            description="Minimum latitude of the bounding box to retrieve data for",
        ),
    ] = None,
    max_lat: Annotated[
        float | None,
        Query(
            description="Maximum latitude of the bounding box to retrieve data for",
        ),
    ] = None,
    min_lon: Annotated[
        float | None,
        Query(
            description="Minimum longitude of the bounding box to retrieve data for",
        ),
    ] = None,
    max_lon: Annotated[
        float | None,
        Query(
            description="Maximum longitude of the bounding box to retrieve data for",
        ),
    ] = None,
) -> Optional[tuple[float, float, float, float]]:
    if all([min_lat, max_lat, min_lon, max_lon]):
        return (min_lat, max_lat, min_lon, max_lon)
    return None


BoundingBoxDep = Annotated[
    Optional[tuple[float, float, float, float]], Depends(bounding_box)
]


def include_neighbors(
    include_neighbors: Annotated[
        bool,
        Query(
            description="Whether or not to include neighboring cells in the response"
        ),
    ] = False
) -> bool:
    return include_neighbors


IncludeNeighborsDep = Annotated[bool, Depends(include_neighbors)]


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
