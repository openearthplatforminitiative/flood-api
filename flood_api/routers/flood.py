from fastapi import APIRouter

from flood_api.dependencies.flooddata import (
    DetailedDataDep,
    SummaryDataDep,
    ThresholdDataDep,
)
from flood_api.dependencies.queryparams import (
    BoundingBoxDep,
    CoordinatesDep,
    DateRangeDep,
    IncludeNeighborsDep,
)
from flood_api.models.detailed_types import DetailedProperties, DetailedResponseModel
from flood_api.models.summary_types import SummaryProperties, SummaryResponseModel
from flood_api.models.threshold_types import ThresholdProperties, ThresholdResponseModel
from flood_api.utils.geospatial_operations import get_data_for_bbox, get_data_for_point
from flood_api.utils.json_utilities import dataframe_to_geojson
from flood_api.utils.validation_helpers import (
    validate_bounding_box,
    validate_coordinates,
    validate_dates,
    validate_generic_inputs,
)

router = APIRouter(tags=["flood"])


@router.get(
    "/summary",
    summary="Get summary forecast for a location",
    description="Returns a summary forecast of the next 30 days either for the cell at the given coordinates or for the cells within the given bounding box",
)
async def summary(
    gdf: SummaryDataDep,
    coordinates: CoordinatesDep,
    bbox: BoundingBoxDep,
    include_neighbors: IncludeNeighborsDep,
) -> SummaryResponseModel:
    validate_generic_inputs(
        coordinates,
        bbox,
        possible_inputs_str="coordinates, bounding box",
    )

    if coordinates is not None:
        validate_coordinates(*coordinates)
        queried_location, neighboring_location = get_data_for_point(
            *coordinates,
            include_neighbors=include_neighbors,
            gdf=gdf,
        )

    elif bbox is not None:
        validate_bounding_box(*bbox)
        queried_location = get_data_for_bbox(
            bbox=bbox,
            gdf=gdf,
        )
        neighboring_location = None

    summary_cols = list(SummaryProperties.model_fields.keys())

    queried_location_geojson = dataframe_to_geojson(
        df=queried_location, columns=summary_cols
    )

    sort_columns = ["latitude", "longitude"]

    if neighboring_location is None:
        neighboring_location_geojson = None
    else:
        neighboring_location_geojson = dataframe_to_geojson(
            df=neighboring_location, columns=summary_cols, sort_columns=sort_columns
        )

    response = SummaryResponseModel(
        queried_location=queried_location_geojson,
        neighboring_location=neighboring_location_geojson,
    )

    return response


@router.get(
    "/detailed",
    summary="Get detailed forecast for a location",
    description="Returns a detailed forecast of the next 30 days either for the cell at the given coordinates or for the cells within the given bounding box",
)
async def detailed(
    gdf: DetailedDataDep,
    coordinates: CoordinatesDep,
    bbox: BoundingBoxDep,
    include_neighbors: IncludeNeighborsDep,
    date_range: DateRangeDep,
) -> DetailedResponseModel:
    validate_generic_inputs(
        coordinates,
        bbox,
        possible_inputs_str="coordinates, bounding box",
    )

    validate_dates(*date_range)

    if coordinates is not None:
        validate_coordinates(*coordinates)
        queried_location, neighboring_location = get_data_for_point(
            *coordinates,
            include_neighbors=include_neighbors,
            gdf=gdf,
            date_range=date_range,
        )

    elif bbox is not None:
        validate_bounding_box(*bbox)
        queried_location = get_data_for_bbox(
            bbox=bbox,
            gdf=gdf,
            date_range=date_range,
        )
        neighboring_location = None

    detailed_cols = list(DetailedProperties.model_fields.keys())

    sort_columns = ["latitude", "longitude", "step"]

    queried_location_geojson = dataframe_to_geojson(
        df=queried_location, columns=detailed_cols, sort_columns=sort_columns
    )

    if neighboring_location is None:
        neighboring_location_geojson = None
    else:
        neighboring_location_geojson = dataframe_to_geojson(
            df=neighboring_location, columns=detailed_cols, sort_columns=sort_columns
        )

    response = DetailedResponseModel(
        queried_location=queried_location_geojson,
        neighboring_location=neighboring_location_geojson,
    )

    return response


@router.get(
    "/threshold",
    summary="Get return period thresholds for a location",
    description="Returns the 2-, 5-, and 20-year return period thresholds either for the cell at the given coordinates or for the cells within the given bounding box",
)
async def threshold(
    gdf: ThresholdDataDep,
    coordinates: CoordinatesDep,
    bbox: BoundingBoxDep,
) -> ThresholdResponseModel:
    validate_generic_inputs(
        coordinates,
        bbox,
        possible_inputs_str="coordinates, bounding box",
    )

    if coordinates is not None:
        validate_coordinates(*coordinates)
        queried_location, _ = get_data_for_point(
            *coordinates,
            gdf=gdf,
        )

    elif bbox is not None:
        validate_bounding_box(*bbox)
        queried_location = get_data_for_bbox(
            bbox=bbox,
            gdf=gdf,
        )

    threshold_cols = list(ThresholdProperties.model_fields.keys())

    queried_location_geojson = dataframe_to_geojson(
        df=queried_location,
        columns=threshold_cols,
    )

    response = ThresholdResponseModel(
        queried_location=queried_location_geojson,
    )

    return response
