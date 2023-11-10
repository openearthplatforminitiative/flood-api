from datetime import date

import geopandas as gpd
import pandas as pd
from fastapi.testclient import TestClient

from flood_api.__main__ import app
from flood_api.dependencies.flooddata import get_detailed_data
from flood_api.settings import settings
from flood_api.tests.synthetic_data import gdf_test_detailed

GLOFAS_ROI = settings.glofas_roi

TOTAL_STEPS = 30

app.dependency_overrides[get_detailed_data] = lambda: gdf_test_detailed

client = TestClient(app)


def get_detailed_response_code(params):
    response = client.get("/detailed", params=params)
    return response.status_code


def test_detailed_roi():
    min_lat = GLOFAS_ROI["min_lat"]
    max_lat = GLOFAS_ROI["max_lat"]
    min_lon = GLOFAS_ROI["min_lon"]
    max_lon = GLOFAS_ROI["max_lon"]
    eps = 1e-6
    expected_error_code = 404

    # Queried latitude is outside the ROI
    params = {"lat": min_lat - eps, "lon": (min_lon + max_lon) / 2}
    assert get_detailed_response_code(params) == expected_error_code

    # Queried latitude is outside the ROI
    # Being on the upper boundary implies
    # that the queried point is outside the ROI
    params = {"lat": max_lat, "lon": (min_lon + max_lon) / 2}
    assert get_detailed_response_code(params) == expected_error_code

    # Queried longitude is outside the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": min_lon - eps}
    assert get_detailed_response_code(params) == expected_error_code

    # Queried longitude is outside the ROI
    # Being on the upper boundary implies
    # that the queried point is outside the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": max_lon}
    assert get_detailed_response_code(params) == expected_error_code

    # Queried point is within the ROI
    # Being on the lower boundary implies
    # that the queried point is within the ROI
    params = {"lat": min_lat, "lon": (min_lon + max_lon) / 2}
    assert get_detailed_response_code(params) == 200

    # Queried point is within the ROI
    # Being on the lower boundary implies
    # that the queried point is within the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": min_lon}
    assert get_detailed_response_code(params) == 200


def test_detailed_border_query():
    # Queried point is in the lower left
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.05}

    response = client.get("/detailed", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Queried point is in the lower right
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.1}

    response = client.get("/detailed", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])

    # Assert that dataframe is empty
    assert gdf.empty


def test_detailed_date_range():
    min_lat = GLOFAS_ROI["min_lat"]
    max_lat = GLOFAS_ROI["max_lat"]
    min_lon = GLOFAS_ROI["min_lon"]
    max_lon = GLOFAS_ROI["max_lon"]
    expected_error_code = 400

    # Start date is before the end date
    params = {
        "lat": (min_lat + max_lat) / 2,
        "lon": (min_lon + max_lon) / 2,
        "start_date": "2023-11-29",
        "end_date": "2023-12-01",
    }

    assert get_detailed_response_code(params) == 200

    # Start date is after the end date
    params = {
        "lat": (min_lat + max_lat) / 2,
        "lon": (min_lon + max_lon) / 2,
        "start_date": "2023-11-29",
        "end_date": "2023-11-28",
    }

    assert get_detailed_response_code(params) == expected_error_code

    # Start date and end date are the same
    params = {
        "lat": (min_lat + max_lat) / 2,
        "lon": (min_lon + max_lon) / 2,
        "start_date": "2023-11-29",
        "end_date": "2023-11-29",
    }

    assert get_detailed_response_code(params) == 200


def test_detailed_general():
    params = {
        "lat": 6.2,
        "lon": 39.05,
    }

    response = client.get("/detailed", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that row count is correct
    assert len(gdf) == TOTAL_STEPS

    # Assert that 'step' column is increasing
    assert gdf["step"].is_monotonic_increasing

    # Assert that 'geometry' and 'issued_on' are the same for all rows
    assert gdf["geometry"].nunique() == 1
    assert gdf["issued_on"].nunique() == 1


def test_detailed_neighbor():
    # Neighbors are included
    params = {"lat": 6.2, "lon": 39.05, "include_neighbors": "true"}

    response = client.get("/detailed", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf_neighbor = gpd.GeoDataFrame.from_features(data["neighboring_cells"]["features"])

    # Assert that dataframe is not empty
    assert not gdf_neighbor.empty

    # Assert that row count is correct
    assert len(gdf_neighbor) == TOTAL_STEPS

    # Assert that 'step' column is increasing
    assert gdf_neighbor["step"].is_monotonic_increasing

    # Assert that 'geometry' and 'issued_on' are the same for all rows
    assert gdf_neighbor["geometry"].nunique() == 1
    assert gdf_neighbor["issued_on"].nunique() == 1


def test_detailed_day_range():
    # Both start and end dates are specified
    params = {
        "lat": 6.2,
        "lon": 39.05,
        "start_date": "2023-11-29",
        "end_date": "2023-12-01",
        "include_neighbors": "true",
    }

    response = client.get("/detailed", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])
    gdf_neighbor = gpd.GeoDataFrame.from_features(data["neighboring_cells"]["features"])

    # Convert 'valid_for' column to date
    gdf["valid_for"] = pd.to_datetime(gdf["valid_for"]).dt.date
    gdf_neighbor["valid_for"] = pd.to_datetime(gdf_neighbor["valid_for"]).dt.date

    # Assert that dataframe is not empty
    assert not gdf.empty
    assert not gdf_neighbor.empty

    # Assert that 'step' column is increasing
    assert gdf["step"].is_monotonic_increasing
    assert gdf_neighbor["step"].is_monotonic_increasing

    print(gdf["valid_for"])

    # Assert that row count is correct
    assert len(gdf) == 3
    assert len(gdf_neighbor) == 3

    # Assert that 'geometry' and 'issued_on' are the same for all rows
    assert gdf["geometry"].nunique() == 1
    assert gdf["issued_on"].nunique() == 1
    assert gdf_neighbor["geometry"].nunique() == 1
    assert gdf_neighbor["issued_on"].nunique() == 1

    # Assert that 'valid_for' is within the specified range
    assert gdf["valid_for"].min() == date(2023, 11, 29)
    assert gdf["valid_for"].max() == date(2023, 12, 1)
    assert gdf_neighbor["valid_for"].min() == date(2023, 11, 29)
    assert gdf_neighbor["valid_for"].max() == date(2023, 12, 1)


def test_detailed_day_range_no_start():
    # We are testing the case where the end date is omitted
    params = {
        "lat": 6.2,
        "lon": 39.05,
        "start_date": "2023-11-29",
    }

    response = client.get("/detailed", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])

    # Convert 'valid_for' column to date
    gdf["valid_for"] = pd.to_datetime(gdf["valid_for"]).dt.date

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that 'step' column is increasing
    assert gdf["step"].is_monotonic_increasing

    # Assert that row count is correct
    assert len(gdf) == TOTAL_STEPS - gdf["step"].min() + 1

    # Assert that maximum step is correct
    assert gdf["step"].max() == TOTAL_STEPS

    # Assert that 'valid_for' is within the specified range
    assert gdf["valid_for"].min() == date(2023, 11, 29)
    assert gdf["valid_for"].max() == date(2023, 12, 9)


def test_detailed_day_range_no_end():
    # We are testing the case where the start date is omitted
    params = {
        "lat": 6.2,
        "lon": 39.05,
        "end_date": "2023-12-01",
    }

    response = client.get("/detailed", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])

    # Convert 'valid_for' column to date
    gdf["valid_for"] = pd.to_datetime(gdf["valid_for"]).dt.date

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that 'step' column is increasing
    assert gdf["step"].is_monotonic_increasing

    # Assert that row count is correct
    assert len(gdf) == gdf["step"].max()

    # Assert that minimum step is correct
    assert gdf["step"].min() == 1

    # Assert that 'valid_for' is within the specified range
    assert gdf["valid_for"].min() == date(2023, 11, 10)
    assert gdf["valid_for"].max() == date(2023, 12, 1)
