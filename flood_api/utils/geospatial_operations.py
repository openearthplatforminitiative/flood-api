from datetime import date, timedelta
from decimal import Decimal, getcontext
from math import floor

import geopandas as gpd
from pandas import Timestamp
from shapely.geometry import Polygon

# Set the precision high enough to handle the arithmetic correctly
# API users should not need more than 9 decimal places of precision
getcontext().prec = 9

from flood_api.settings import settings

GLOFAS_RESOLUTION = settings.glofas_resolution
GLOFAS_PRECISION = settings.glofas_precision


def get_grid_cell_bounds(
    latitude: float,
    longitude: float,
    grid_size: float = GLOFAS_RESOLUTION,
    precision: int = GLOFAS_PRECISION,
) -> tuple[float, float, float, float]:
    """
    Given a latitude and longitude, find the bounding box of the grid cell
    it falls into.

    The function identifies the grid cell based on the following logic:
    - If the provided point is on the boundary between two cells, the function
      will assign the point to the cell to its east (right, for longitude) or
      north (above, for latitude).
    - For example, for a grid_size of 0.05:
      * An input latitude of -5.8 and longitude of 37.75 would result in a
        bounding box from latitude -5.8 to -5.75 and longitude 37.75 to 37.8.
      * An input latitude of -5.81 and longitude of 37.7501 would result in a
        bounding box from latitude -5.85 to -5.8 and longitude 37.75 to 37.8.

    Parameters:
    - latitude (float): The latitude of the point.
    - longitude (float): The longitude of the point.
    - grid_size (float, optional): The size of each grid cell. Defaults to 0.05.
    - precision (int, optional): Number of decimal places to round to. Defaults to 3.

    Returns:
    tuple: Bounding box of the grid cell as (min_latitude, max_latitude, min_longitude, max_longitude).
    """
    # Convert to Decimal for precise arithmetic
    # Without this, the results can be incorrect
    latitude = Decimal(str(latitude))
    longitude = Decimal(str(longitude))
    grid_size = Decimal(str(grid_size))

    # Calculate lower boundaries using precise decimal division and multiplication
    min_lon_cell = floor(longitude / grid_size) * grid_size
    min_lat_cell = floor(latitude / grid_size) * grid_size

    # Calculate the upper boundaries
    max_lon_cell = min_lon_cell + grid_size
    max_lat_cell = min_lat_cell + grid_size

    # Round the results
    return (
        float(round(min_lat_cell, precision)),
        float(round(max_lat_cell, precision)),
        float(round(min_lon_cell, precision)),
        float(round(max_lon_cell, precision)),
    )


def create_polygon_from_bounds(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    buffer: float = 0.0,
    precision: int = GLOFAS_PRECISION,
) -> Polygon:
    """
    Given the bounds (min_lat, max_lat, min_lon, max_lon),
    return a Polygon.

    Parameters:
    - min_lat (float): The minimum latitude of the polygon.
    - max_lat (float): The maximum latitude of the polygon.
    - min_lon (float): The minimum longitude of the polygon.
    - max_lon (float): The maximum longitude of the polygon.
    - buffer (float, optional): The buffer to add to the polygon. Defaults to 0.
    - precision (int, optional): Number of decimal places to round to. Defaults to 3.

    Returns:
    Polygon: The polygon defined by the bounds.
    """
    # Define the four corners of the polygon
    bottom_left = (
        round(min_lon - buffer, precision),
        round(min_lat - buffer, precision),
    )
    bottom_right = (
        round(max_lon + buffer, precision),
        round(min_lat - buffer, precision),
    )
    top_right = (round(max_lon + buffer, precision), round(max_lat + buffer, precision))
    top_left = (round(min_lon - buffer, precision), round(max_lat + buffer, precision))

    # Create and return the polygon
    return Polygon([bottom_left, top_left, top_right, bottom_right, bottom_left])


def get_data_for_point(
    latitude: float,
    longitude: float,
    gdf: gpd.GeoDataFrame,
    include_neighbors: bool = False,
    date_range: tuple[date, date] = None,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Given a latitude and longitude, return the data for the grid cell
    it falls into. Optionally, include the data for neighboring cells.
    A date range can also be provided to filter the data, yielding only
    the data within the date range (inclusive). If no date range is provided,
    data for all dates will be returned.

    The function identifies the grid cell based on the following logic:
    - If the provided point is on the boundary between two cells, the function
      will assign the point to the cell to its east (right, for longitude) or
      north (above, for latitude).
    - For example, for a grid_size of 0.05:
        * An input latitude of -5.8 and longitude of 37.75 would result in a
            bounding box from latitude -5.8 to -5.75 and longitude 37.75 to 37.8.
        * An input latitude of -5.81 and longitude of 37.7501 would result in a
            bounding box from latitude -5.85 to -5.8 and longitude 37.75 to 37.8.

    Parameters:
    - latitude (float): The latitude of the point.
    - longitude (float): The longitude of the point.
    - gdf (GeoDataFrame): The GeoDataFrame to query.
    - include_neighbors (bool): Whether to include neighboring cells. Defaults to False.
    - date_range (tuple, optional): The date range to query (inclusive). Defaults to None.

    Returns:
    tuple: The primary cell and neighbors as GeoDataFrames.
    """
    # Get the bounds for the queryed cell
    cell_bounds = get_grid_cell_bounds(
        latitude=latitude,
        longitude=longitude,
        grid_size=GLOFAS_RESOLUTION,
        precision=GLOFAS_PRECISION,
    )

    # Get the deflated geometry to find primary cell
    reduced_geometry = create_polygon_from_bounds(
        *cell_bounds, buffer=-GLOFAS_RESOLUTION / 2, precision=GLOFAS_PRECISION
    )

    neighbors_only_df = gpd.GeoDataFrame(geometry=[])

    if date_range is not None:
        # Filter the dataframe for the date range
        gdf = gdf[gdf["valid_for"].between(*date_range)]

    if include_neighbors:
        # Get the inflated geometry to find primary cell and neighbors
        expanded_geometry = create_polygon_from_bounds(
            *cell_bounds, buffer=GLOFAS_RESOLUTION / 2, precision=GLOFAS_PRECISION
        )

        # Query the main dataframe for possible matches
        # We use the expanded geometry to get the primary
        # cell and neighbors
        possible_matches_index = gdf.sindex.query(
            expanded_geometry, predicate="intersects"
        )
        all_cells_df = gdf.iloc[possible_matches_index]

        # Define mask for distinguishing between primary cell and neighbors
        primary_cell_mask = all_cells_df["geometry"].intersects(reduced_geometry)

        # Define primary cell and neighbors dataframes
        primary_cell_df = all_cells_df[primary_cell_mask]
        neighbors_only_df = all_cells_df[~primary_cell_mask]

    else:
        # Query the main dataframe for possible matches
        # This is the same as the expanded geometry,
        # but we use the reduced geometry to get only the primary cell
        possible_matches_index = gdf.sindex.query(
            reduced_geometry, predicate="intersects"
        )
        primary_cell_df = gdf.iloc[possible_matches_index]

    return primary_cell_df, neighbors_only_df
