from datetime import date

from fastapi import HTTPException

from flood_api.settings import settings

GLOFAS_ROI = settings.glofas_roi
OUT_OF_BOUNDS_STATUS_CODE = settings.out_of_bounds_query_status_code
INVALID_STATUS_CODE = settings.invalid_query_status_code


def validate_coordinates(latitude: float, longitude: float) -> None:
    """
    Check if the given point is within the region of interest (ROI).
    If not, raise an HTTPException with status code 404.

    Parameters:
    - latitude (float): The latitude of the point.
    - longitude (float): The longitude of the point.

    Returns:
    None
    """
    point_within_roi = (
        GLOFAS_ROI["min_lat"] <= latitude < GLOFAS_ROI["max_lat"]
        and GLOFAS_ROI["min_lon"] <= longitude < GLOFAS_ROI["max_lon"]
    )

    if not point_within_roi:
        raise HTTPException(
            status_code=OUT_OF_BOUNDS_STATUS_CODE,
            detail="Queried coordinates are outside the region of interest",
        )


def validate_bounding_box(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> None:
    """
    Check if the given bounding box is valid (i.e. min < max) and within the
    the region of interest (ROI). If the bounding box is invalid, raise an
    HTTPException with status code 400. If the bounding box is outside the ROI,
    raise an HTTPException with status code 404.

    Parameters:
    - min_lat (float): The minimum latitude of the bounding box.
    - max_lat (float): The maximum latitude of the bounding box.
    - min_lon (float): The minimum longitude of the bounding box.
    - max_lon (float): The maximum longitude of the bounding box.

    Returns:
    None
    """
    bounding_box_is_valid = min_lat < max_lat and min_lon < max_lon

    if not bounding_box_is_valid:
        raise HTTPException(
            status_code=INVALID_STATUS_CODE,
            detail="Invalid bounding box",
        )

    bounding_box_within_roi = (
        GLOFAS_ROI["min_lat"] <= min_lat < max_lat <= GLOFAS_ROI["max_lat"]
        and GLOFAS_ROI["min_lon"] <= min_lon < max_lon <= GLOFAS_ROI["max_lon"]
    )

    if not bounding_box_within_roi:
        raise HTTPException(
            status_code=OUT_OF_BOUNDS_STATUS_CODE,
            detail="Queried bounding box is not within the region of interest",
        )


def validate_dates(start_date: date, end_date: date) -> None:
    """
    Check if the given date range is valid.
    If not, raise an HTTPException with status code 400.

    Parameters:
    - start_date (date): The start date of the date range.
    - end_date (date): The end date of the date range.

    Returns:
    None
    """
    date_range_is_valid = start_date <= end_date

    if not date_range_is_valid:
        raise HTTPException(
            status_code=INVALID_STATUS_CODE, detail="Invalid date range"
        )
