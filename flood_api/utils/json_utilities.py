import json
from datetime import date

import geopandas as gpd
import pandas as pd


def custom_date_handler(obj: object) -> str:
    """
    Custom date handler for converting dates to ISO format.

    Parameters:
    - obj (object): The object to convert.

    Returns:
    str: The ISO formatted date string.
    """
    if isinstance(obj, date) or isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def dataframe_to_geojson(
    df: gpd.GeoDataFrame, columns: list[str], sort_columns: list[str] | None = None
) -> dict:
    """
    Convert a GeoDataFrame to a GeoJSON.

    Parameters:
    - df (GeoDataFrame): The GeoDataFrame to convert.
    - columns (list): The columns to include in the GeoJSON.
    - sort_columns (list): The columns to sort by.

    Returns:
    dict: The GeoJSON.
    """
    # Check if the dataframe is empty. If it is, return an
    # empty GeoJSON where we only assume the geometry column
    # is present.
    if df.empty:
        return json.loads(df.to_json())

    # Sort the columns if a list of columns is provided
    if sort_columns is not None:
        df = df.sort_values(by=sort_columns)

    # Reset the index to make response cleaner
    df = df.reset_index(drop=True)

    # Serialize the dataframe as a string
    geojson_as_string = df[columns + ["geometry"]].to_json(default=custom_date_handler)

    # Use json library to convert from serialized string to json
    return json.loads(geojson_as_string)
