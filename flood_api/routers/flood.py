from fastapi import APIRouter

from flood_api.dependencies.flooddata import (
    DetailedDataDep,
    SummaryDataDep,
    ThresholdDataDep,
)
from flood_api.dependencies.queryparams import (
    DateRangeDep,
    IncludeNeighborsDep,
    LocationQueryDep,
)
from flood_api.models.detailed_types import DetailedProperties, DetailedResponseModel
from flood_api.models.summary_types import SummaryProperties, SummaryResponseModel
from flood_api.models.threshold_types import ThresholdProperties, ThresholdResponseModel
from flood_api.utils.geospatial_operations import get_data_for_bbox, get_data_for_point
from flood_api.utils.json_utilities import dataframe_to_geojson

router = APIRouter(tags=["flood"])


@router.get(
    "/summary",
    summary="Get summary forecast for a location",
    description=(
        "Returns a summary forecast of the next 30 days either for the cell "
        "at the given coordinates or for the cells within the given bounding box"
    ),
)
async def summary(
    gdf: SummaryDataDep,
    location_query: LocationQueryDep,
    include_neighbors: IncludeNeighborsDep,
) -> SummaryResponseModel:
    match location_query:
        case lat, lon:
            queried_location, neighboring_location = get_data_for_point(
                latitude=lat,
                longitude=lon,
                include_neighbors=include_neighbors,
                gdf=gdf,
            )
        case min_lat, max_lat, min_lon, max_lon:
            queried_location = get_data_for_bbox(
                bbox=location_query,
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
    description=(
        "Returns a detailed forecast of the next 30 days either for the cell "
        "at the given coordinates or for the cells within the given bounding box"
    ),
)
async def detailed(
    gdf: DetailedDataDep,
    location_query: LocationQueryDep,
    include_neighbors: IncludeNeighborsDep,
    date_range: DateRangeDep,
) -> DetailedResponseModel:
    match location_query:
        case lat, lon:
            queried_location, neighboring_location = get_data_for_point(
                latitude=lat,
                longitude=lon,
                include_neighbors=include_neighbors,
                gdf=gdf,
                date_range=date_range,
            )
        case min_lat, max_lat, min_lon, max_lon:
            queried_location = get_data_for_bbox(
                bbox=location_query,
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
    description=(
        "Returns the 2-, 5-, and 20-year return period thresholds either for the cell "
        "at the given coordinates or for the cells within the given bounding box"
    ),
)
async def threshold(
    gdf: ThresholdDataDep, location_query: LocationQueryDep
) -> ThresholdResponseModel:
    match location_query:
        case lat, lon:
            queried_location, _ = get_data_for_point(
                longitude=lon, latitude=lat, gdf=gdf
            )
        case min_lat, max_lat, min_lon, max_lon:
            queried_location = get_data_for_bbox(bbox=location_query, gdf=gdf)

    threshold_cols = list(ThresholdProperties.model_fields.keys())
    queried_location_geojson = dataframe_to_geojson(
        df=queried_location, columns=threshold_cols
    )
    response = ThresholdResponseModel(queried_location=queried_location_geojson)
    return response
