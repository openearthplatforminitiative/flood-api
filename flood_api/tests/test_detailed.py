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


def get_detailed_response(params):
    return client.get("/detailed", params=params)


def get_detailed_response_code(params):
    return get_detailed_response(params).status_code


def test_detailed_arg_validity():
    expected_error_code = 404

    # Neither lat/lon nor bbox are provided
    params = {"include_neighbors": "true"}
    response = get_detailed_response(params)

    assert response.status_code == expected_error_code

    # Both lat/lon and bbox are provided
    params = {
        "lat": 6.2,
        "lon": 39.05,
        "min_lat": 6.225,
        "max_lat": 6.25,
        "min_lon": 39.0,
        "max_lon": 40.0,
    }
    response = get_detailed_response(params)

    assert response.status_code == expected_error_code

    # Incomplete bbox is provided
    params = {
        "min_lat": 6.225,
        "max_lat": 6.25,
        "min_lon": 39.0,
    }
    response = get_detailed_response(params)

    assert response.status_code == expected_error_code

    # Incomplete coordinates are provided
    params = {
        "lat": 6.2,
    }
    response = get_detailed_response(params)

    assert response.status_code == expected_error_code

    # One of the coordinates is zero
    params = {
        "lon": 0.0,
        "lat": 6.2,
    }
    response = get_detailed_response(params)

    assert response.status_code == 200

    # One of the bounding box coordinates is zero
    params = {
        "min_lon": 0.0,
        "max_lon": 40.0,
        "min_lat": 6.225,
        "max_lat": 6.25,
    }
    response = get_detailed_response(params)

    assert response.status_code == 200


def test_detailed_point_validity():
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


def test_detailed_bbox_validity():
    min_lat = GLOFAS_ROI["min_lat"]
    max_lat = GLOFAS_ROI["max_lat"]
    min_lon = GLOFAS_ROI["min_lon"]
    max_lon = GLOFAS_ROI["max_lon"]
    eps = 1e-6
    expected_error_code = 404

    # Queried maximum latitude is smaller than the minimum latitude
    params = {
        "min_lat": 4.0,
        "max_lat": 3.0,
        "min_lon": 0.0,
        "max_lon": 10.0,
    }
    assert get_detailed_response_code(params) == expected_error_code

    # Queried maximum longitude is the same as the minimum longitude
    params = {
        "min_lat": 0.0,
        "max_lat": 10.0,
        "min_lon": 4.0,
        "max_lon": 4.0,
    }
    assert get_detailed_response_code(params) == expected_error_code

    # Queried minimum latitude is outside the ROI
    params = {
        "min_lat": min_lat - eps,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_detailed_response_code(params) == expected_error_code

    # Queried maximum latitude is outside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 2,
        "max_lat": max_lat + eps,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_detailed_response_code(params) == expected_error_code

    # Queried minimum longitude is outside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": min_lon - eps,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_detailed_response_code(params) == expected_error_code

    # Queried maximum longitude is outside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 2,
        "max_lon": max_lon + eps,
    }
    assert get_detailed_response_code(params) == expected_error_code

    # Queried minimum latitude is inside the ROI
    params = {
        "min_lat": min_lat,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_detailed_response_code(params) == 200

    # Queried maximum latitude is inside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 2,
        "max_lat": max_lat,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_detailed_response_code(params) == 200

    # Queried minimum longitude is inside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": min_lon,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_detailed_response_code(params) == 200

    # Queried maximum longitude is inside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 2,
        "max_lon": max_lon,
    }
    assert get_detailed_response_code(params) == 200


def test_detailed_point_border_query():
    # Queried point is in the lower left
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.05}

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Queried point is in the lower right
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.1}

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is empty
    assert gdf.empty


def test_detailed_point_date_range():
    min_lat = GLOFAS_ROI["min_lat"]
    max_lat = GLOFAS_ROI["max_lat"]
    min_lon = GLOFAS_ROI["min_lon"]
    max_lon = GLOFAS_ROI["max_lon"]
    expected_error_code = 404

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


def test_detailed_point_general():
    params = {
        "lat": 6.2,
        "lon": 39.05,
    }

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that row count is correct
    assert len(gdf) == TOTAL_STEPS

    # Assert that 'step' column is increasing
    assert gdf["step"].is_monotonic_increasing

    # Assert that 'geometry' and 'issued_on' are the same for all rows
    assert gdf["geometry"].nunique() == 1
    assert gdf["issued_on"].nunique() == 1


def test_detailed_point_neighbor():
    # Neighbors are included
    params = {"lat": 6.2, "lon": 39.05, "include_neighbors": "true"}

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf_neighbor = gpd.GeoDataFrame.from_features(
        data["neighboring_location"]["features"]
    )

    # Assert that dataframe is not empty
    assert not gdf_neighbor.empty

    # Assert that row count is correct
    assert len(gdf_neighbor) == TOTAL_STEPS

    # Assert that 'step' column is increasing
    assert gdf_neighbor["step"].is_monotonic_increasing

    # Assert that 'geometry' and 'issued_on' are the same for all rows
    assert gdf_neighbor["geometry"].nunique() == 1
    assert gdf_neighbor["issued_on"].nunique() == 1


def test_detailed_point_day_range():
    # Both start and end dates are specified
    params = {
        "lat": 6.2,
        "lon": 39.05,
        "start_date": "2023-11-29",
        "end_date": "2023-12-01",
        "include_neighbors": "true",
    }

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])
    gdf_neighbor = gpd.GeoDataFrame.from_features(
        data["neighboring_location"]["features"]
    )

    # Convert 'valid_for' column to date
    gdf["valid_for"] = pd.to_datetime(gdf["valid_for"]).dt.date
    gdf_neighbor["valid_for"] = pd.to_datetime(gdf_neighbor["valid_for"]).dt.date

    # Assert that dataframe is not empty
    assert not gdf.empty
    assert not gdf_neighbor.empty

    # Assert that 'step' column is increasing
    assert gdf["step"].is_monotonic_increasing
    assert gdf_neighbor["step"].is_monotonic_increasing

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


def test_detailed_point_day_range_no_start():
    # We are testing the case where the end date is omitted
    params = {
        "lat": 6.2,
        "lon": 39.05,
        "start_date": "2023-11-29",
    }

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

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


def test_detailed_point_day_range_no_end():
    # We are testing the case where the start date is omitted
    params = {
        "lat": 6.2,
        "lon": 39.05,
        "end_date": "2023-12-01",
    }

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

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


def test_detailed_bbox_general():
    # Queried bounding box covers both cells in the test data
    params = {
        "min_lat": 6.225,
        "max_lat": 6.25,  # On the boundary between the two cells
        "min_lon": 39.0,
        "max_lon": 40.0,
    }

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that row count is correct
    assert len(gdf) == TOTAL_STEPS * 2

    # Assert that the 'geometry' column has two unique values
    assert gdf["geometry"].nunique() == 2

    # Queried bounding box covers only one cell in the test data
    params = {
        "min_lat": 6.225,
        "max_lat": 6.24999,  # Just below the upper boundary
        "min_lon": 39.0,
        "max_lon": 40.0,
    }

    response = get_detailed_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that row count is correct
    assert len(gdf) == TOTAL_STEPS

    # Assert that 'step' column is increasing
    assert gdf["step"].is_monotonic_increasing

    # Assert that the 'geometry' column has one unique value
    assert gdf["geometry"].nunique() == 1
