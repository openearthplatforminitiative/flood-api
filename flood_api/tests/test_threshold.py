import geopandas as gpd
from fastapi.testclient import TestClient

from flood_api.__main__ import app
from flood_api.dependencies.flooddata import get_threshold_data
from flood_api.settings import settings
from flood_api.tests.synthetic_data import gdf_test_threshold

GLOFAS_ROI = settings.glofas_roi

app.dependency_overrides[get_threshold_data] = lambda: gdf_test_threshold

client = TestClient(app)


def get_threshold_response_code(params):
    response = client.get("/threshold", params=params)
    return response.status_code


def test_threshold_roi():
    min_lat = GLOFAS_ROI["min_lat"]
    max_lat = GLOFAS_ROI["max_lat"]
    min_lon = GLOFAS_ROI["min_lon"]
    max_lon = GLOFAS_ROI["max_lon"]
    eps = 1e-6
    expected_error_code = 404

    # Queried latitude is outside the ROI
    params = {"lat": min_lat - eps, "lon": (min_lon + max_lon) / 2}
    assert get_threshold_response_code(params) == expected_error_code

    # Queried latitude is outside the ROI
    # Being on the upper boundary implies
    # that the queried point is outside the ROI
    params = {"lat": max_lat, "lon": (min_lon + max_lon) / 2}
    assert get_threshold_response_code(params) == expected_error_code

    # Queried longitude is outside the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": min_lon - eps}
    assert get_threshold_response_code(params) == expected_error_code

    # Queried longitude is outside the ROI
    # Being on the upper boundary implies
    # that the queried point is outside the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": max_lon}
    assert get_threshold_response_code(params) == expected_error_code

    # Queried point is within the ROI
    # Being on the lower boundary implies
    # that the queried point is within the ROI
    params = {"lat": min_lat, "lon": (min_lon + max_lon) / 2}
    assert get_threshold_response_code(params) == 200

    # Queried point is within the ROI
    # Being on the lower boundary implies
    # that the queried point is within the ROI
    params = {"lat": (min_lat + max_lat) / 2, "lon": min_lon}
    assert get_threshold_response_code(params) == 200


def test_threshold_border_query():
    # Queried point is in the lower left
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.05}

    response = client.get("/threshold", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])

    # Assert that dataframe is not empty
    assert not gdf.empty

    # Queried point is in the lower right
    # corner of the grid cell
    params = {"lat": 6.2, "lon": 39.1}

    response = client.get("/threshold", params=params)
    data = response.json()

    assert response.status_code == 200

    # Convert the dictionary to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["queried_cell"]["features"])

    # Assert that dataframe is empty
    assert gdf.empty
