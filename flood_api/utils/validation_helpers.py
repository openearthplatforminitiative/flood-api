from datetime import date

from fastapi import HTTPException

from flood_api.settings import settings

GLOFAS_ROI = settings.glofas_roi
INVALID_STATUS_CODE = 404


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
            status_code=INVALID_STATUS_CODE,
            detail="Queried coordinates are outside the region of interest",
        )


def validate_bounding_box(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> None:
    """
    Check if the given bounding box is within the region of interest (ROI).
    If not, raise an HTTPException with status code 404.

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
            status_code=INVALID_STATUS_CODE,
            detail="Queried bounding box is outside the region of interest",
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


def validate_generic_inputs(*args: tuple, possible_inputs_str: str) -> None:
    """
    Check if exaclty one of the given inputs is valid, i.e. not None.
    If not, raise an HTTPException with status code 404.

    Parameters:
    - args (tuple): The inputs to check.
    - possible_inputs_str (str): A string listing the possible inputs.

    Returns:
    None
    """
    valid_inputs_count = sum(map(bool, args))

    # Determine the appropriate error message
    if valid_inputs_count == 0:
        error_message = (
            "One of the following inputs must be provided: " + possible_inputs_str
        )
    elif valid_inputs_count > 1:
        error_message = (
            "Only one of the following inputs can be provided: " + possible_inputs_str
        )
    else:
        # If there is exactly one valid input, return without raising an exception
        return

    # Raise an HTTPException with the determined error message
    raise HTTPException(
        status_code=INVALID_STATUS_CODE,
        detail=error_message,
    )
