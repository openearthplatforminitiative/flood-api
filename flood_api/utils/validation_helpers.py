from datetime import date

from fastapi import HTTPException

from flood_api.settings import settings

GLOFAS_ROI = settings.glofas_roi


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
            status_code=404,
            detail="Queried coordinates are outside the region of interest",
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
    date_range_valid = start_date <= end_date

    if not date_range_valid:
        raise HTTPException(status_code=400, detail="Invalid date range")
