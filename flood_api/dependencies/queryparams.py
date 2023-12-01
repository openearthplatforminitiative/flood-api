from datetime import date
from typing import Annotated, Optional, Union

from fastapi import Depends, HTTPException, Query

from flood_api.settings import settings
from flood_api.utils.validation_helpers import (
    validate_bounding_box,
    validate_coordinates,
    validate_dates,
)

INVALID_STATUS_CODE = settings.invalid_query_status_code

# Define a union type for the dependency
LocationQuery = Union[tuple[float, float], tuple[float, float, float, float]]


def location_query_dependency(
    lon: Annotated[float | None, Query(description="Longitude")] = None,
    lat: Annotated[float | None, Query(description="Latitude")] = None,
    min_lon: Annotated[float | None, Query(description="Minimum longitude")] = None,
    max_lon: Annotated[float | None, Query(description="Maximum longitude")] = None,
    min_lat: Annotated[float | None, Query(description="Minimum latitude")] = None,
    max_lat: Annotated[float | None, Query(description="Maximum latitude")] = None,
) -> LocationQuery:
    coordinates = (lat, lon) if None not in (lat, lon) else None
    bbox = (
        (min_lat, max_lat, min_lon, max_lon)
        if None not in (min_lat, max_lat, min_lon, max_lon)
        else None
    )
    if not (coordinates or bbox):
        raise HTTPException(
            status_code=INVALID_STATUS_CODE,
            detail="Either coordinates or bounding box must be provided.",
        )
    if coordinates and bbox:
        raise HTTPException(
            status_code=INVALID_STATUS_CODE,
            detail="Only coordinates or bounding box can be provided, not both.",
        )
    if coordinates:
        validate_coordinates(*coordinates)
        return coordinates
    else:  # bbox is not None
        validate_bounding_box(*bbox)
        return bbox


LocationQueryDep = Annotated[
    Optional[LocationQuery], Depends(location_query_dependency)
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
    validate_dates(start_date, end_date)
    return start_date, end_date


DateRangeDep = Annotated[tuple[date, date], Depends(date_range)]
