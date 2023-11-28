import geopandas as gpd
from fastapi.testclient import TestClient

from flood_api.__main__ import app
from flood_api.dependencies.flooddata import get_summary_data
from flood_api.settings import settings
from flood_api.tests.synthetic_data import gdf_test_summary

GLOFAS_ROI = settings.glofas_roi

app.dependency_overrides[get_summary_data] = lambda: gdf_test_summary

client = TestClient(app)


def get_summary_response(params):
    return client.get("/summary", params=params)


def get_summary_response_code(params):
    return get_summary_response(params).status_code


def test_summary_arg_validity():
    expected_error_code = 404

    # Neither lat/lon nor bbox are provided
    params = {"include_neighbors": "true"}
    response = get_summary_response(params)

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
    response = get_summary_response(params)

    assert response.status_code == expected_error_code

    # Incomplete bbox is provided
    params = {
        "min_lat": 6.225,
        "max_lat": 6.25,
        "min_lon": 39.0,
    }
    response = get_summary_response(params)

    assert response.status_code == expected_error_code

    # Incomplete coordinates are provided
    params = {
        "lat": 6.2,
    }
    response = get_summary_response(params)

    assert response.status_code == expected_error_code


def test_summary_point_validity():
    min_lat = GLOFAS_ROI["min_lat"]
    max_lat = GLOFAS_ROI["max_lat"]
    min_lon = GLOFAS_ROI["min_lon"]
    max_lon = GLOFAS_ROI["max_lon"]
    eps = 1e-6
    expected_error_code = 404

    # Queried latitude is outside the ROI
    params = {"lat": min_lat - eps, "lon": (min_lon + max_lon) / 2}
    assert get_summary_response_code(params) == expected_error_code

    # Queried latitude is outside the ROI
    # Being on the upper boundary implies
    # that the queried point is outside the ROI
    params = {"lat": max_lat, "lon": (min_lon + max_lon) / 2}
    assert get_summary_response_code(params) == expected_error_code

    # Queried longitude is outside the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": min_lon - eps}
    assert get_summary_response_code(params) == expected_error_code

    # Queried longitude is outside the ROI
    # Being on the upper boundary implies
    # that the queried point is outside the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": max_lon}
    assert get_summary_response_code(params) == expected_error_code

    # Queried point is within the ROI
    # Being on the lower boundary implies
    # that the queried point is within the ROI
    params = {"lat": min_lat, "lon": (min_lon + max_lon) / 2}
    assert get_summary_response_code(params) == 200

    # Queried point is within the ROI
    # Being on the lower boundary implies
    # that the queried point is within the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": min_lon}
    assert get_summary_response_code(params) == 200


def test_summary_bbox_validity():
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
    assert get_summary_response_code(params) == expected_error_code

    # Queried maximum longitude is the same as the minimum longitude
    params = {
        "min_lat": 0.0,
        "max_lat": 10.0,
        "min_lon": 4.0,
        "max_lon": 4.0,
    }
    assert get_summary_response_code(params) == expected_error_code

    # Queried minimum latitude is outside the ROI
    params = {
        "min_lat": min_lat - eps,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_summary_response_code(params) == expected_error_code

    # Queried maximum latitude is outside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 2,
        "max_lat": max_lat + eps,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_summary_response_code(params) == expected_error_code

    # Queried minimum longitude is outside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": min_lon - eps,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_summary_response_code(params) == expected_error_code

    # Queried maximum longitude is outside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 2,
        "max_lon": max_lon + eps,
    }
    assert get_summary_response_code(params) == expected_error_code

    # Queried minimum latitude is inside the ROI
    params = {
        "min_lat": min_lat,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_summary_response_code(params) == 200

    # Queried maximum latitude is inside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 2,
        "max_lat": max_lat,
        "min_lon": (min_lon + max_lon) / 4,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_summary_response_code(params) == 200

    # Queried minimum longitude is inside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": min_lon,
        "max_lon": (min_lon + max_lon) / 2,
    }
    assert get_summary_response_code(params) == 200

    # Queried maximum longitude is inside the ROI
    params = {
        "min_lat": (min_lat + max_lat) / 4,
        "max_lat": (min_lat + max_lat) / 2,
        "min_lon": (min_lon + max_lon) / 2,
        "max_lon": max_lon,
    }
    assert get_summary_response_code(params) == 200


def test_summary_point_border_query():
    # Queried point is in the lower left
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.05}

    response = get_summary_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Queried point is in the lower right
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.1}

    response = get_summary_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is empty
    assert gdf.empty


def test_summary_point_neighbor():
    # Neighboring cells are included
    params = {"lat": 6.2, "lon": 39.05, "include_neighbors": "true"}

    response = get_summary_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf_neighbors = gpd.GeoDataFrame.from_features(
        data["neighboring_location"]["features"]
    )

    # Assert that dataframe is not empty
    assert not gdf_neighbors.empty


def test_summary_bbox_general():
    # Queried bounding box covers both cells in the test data
    params = {
        "min_lat": 6.225,
        "max_lat": 6.25,  # On the boundary between the two cells
        "min_lon": 39.0,
        "max_lon": 40.0,
    }

    response = get_summary_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that row count is correct
    assert len(gdf) == 2

    # Queried bounding box covers only one cell in the test data
    params = {
        "min_lat": 6.225,
        "max_lat": 6.24999,  # Just below the upper boundary
        "min_lon": 39.0,
        "max_lon": 40.0,
    }

    response = get_summary_response(params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_location"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Assert that row count is correct
    assert len(gdf) == 1
