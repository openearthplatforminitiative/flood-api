from flood_api.settings import settings
from flood_api.utils.geospatial_operations import get_grid_cell_bounds

GLOFAS_RESOLUTION = settings.glofas_resolution
GLOFAS_PRECISION = settings.glofas_precision


def test_get_grid_cell_bounds():
    lat = 0
    lon = 0
    expected_lat_bounds = (0.0, 0.05)
    expected_lon_bounds = (0.0, 0.05)

    # Test with default grid size and precision
    obtained_bounds = get_grid_cell_bounds(
        lat, lon, GLOFAS_RESOLUTION, GLOFAS_PRECISION
    )
    assert obtained_bounds == (*expected_lat_bounds, *expected_lon_bounds)

    lat = -5.81
    lon = 37.7501
    expected_lat_bounds = (-5.85, -5.8)
    expected_lon_bounds = (37.75, 37.8)

    # Test with default grid size and precision
    obtained_bounds = get_grid_cell_bounds(
        lat, lon, GLOFAS_RESOLUTION, GLOFAS_PRECISION
    )
    assert obtained_bounds == (*expected_lat_bounds, *expected_lon_bounds)

    lat = -5.8
    lon = 37.75
    expected_lat_bounds = (-5.8, -5.75)
    expected_lon_bounds = (37.75, 37.8)

    # Test with default grid size and precision
    obtained_bounds = get_grid_cell_bounds(
        lat, lon, GLOFAS_RESOLUTION, GLOFAS_PRECISION
    )
    assert obtained_bounds == (*expected_lat_bounds, *expected_lon_bounds)

    lat = 6.2
    lon = 39.05
    expected_lat_bounds = (6.2, 6.25)
    expected_lon_bounds = (39.05, 39.1)

    # Test with default grid size and precision
    obtained_bounds = get_grid_cell_bounds(
        lat, lon, GLOFAS_RESOLUTION, GLOFAS_PRECISION
    )
    assert obtained_bounds == (*expected_lat_bounds, *expected_lon_bounds)
