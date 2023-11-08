from flood_api.settings import settings
GLOFAS_ROI = settings.glofas_roi

def point_within_roi(
    latitude: float, 
    longitude: float
) -> bool:
    """
    Check if the given point is within the region of interest (ROI).

    Parameters:
    - latitude (float): The latitude of the point.
    - longitude (float): The longitude of the point.

    Returns:
    bool: True if the point is within the ROI, False otherwise.
    """
    return (GLOFAS_ROI["min_lat"] <= latitude < GLOFAS_ROI["max_lat"]
            and GLOFAS_ROI["min_lon"] <= longitude < GLOFAS_ROI["max_lon"])