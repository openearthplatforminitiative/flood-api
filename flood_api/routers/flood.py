from fastapi import APIRouter
from fastapi.responses import JSONResponse

from flood_api.dependencies.flooddata import (DetailedDataDep,
                                              SummaryDataDep,
                                              ThresholdDataDep)
from flood_api.dependencies.queryparams import (CoordinatesDep, 
                                                DateRangeDep,
                                                IncludeNeighborsDep)
from flood_api.utils.geospatial_operations import get_data_for_point
from flood_api.utils.json_utilities import dataframe_to_geojson
from flood_api.utils.validation_helpers import (validate_coordinates,
                                                validate_dates)
from flood_api.dependencies.models import (SummaryResponseModel,
                                           SummaryProperties,
                                           DetailedResponseModel,
                                           DetailedProperties,
                                           ThresholdResponseModel,
                                           ThresholdProperties)

router = APIRouter(tags=["flood"])

@router.get("/summary", response_model=SummaryResponseModel, response_class=JSONResponse)
async def summary(
    gdf: SummaryDataDep,
    coordinates: CoordinatesDep,
    include_neighbors: IncludeNeighborsDep,
) -> SummaryResponseModel:
    longitude, latitude = coordinates

    # Validate the inputs
    validate_coordinates(latitude=latitude, longitude=longitude)

    queried_cell, neighboring_cells = get_data_for_point(
        latitude=latitude, 
        longitude=longitude, 
        include_neighbors=include_neighbors, 
        gdf=gdf
    )

    summary_cols = list(SummaryProperties.model_fields.keys())


    queried_cell_geojson = dataframe_to_geojson(
        df=queried_cell, 
        columns=summary_cols
    )
    
    sort_columns = ["latitude", "longitude"]

    neighboring_cells_geojson = dataframe_to_geojson(
        df=neighboring_cells, 
        columns=summary_cols,
        sort_columns=sort_columns
    )
    
    response = SummaryResponseModel(
        queried_cell=queried_cell_geojson,
        neighboring_cells=neighboring_cells_geojson
    )

    return response

@router.get("/detailed", response_model=DetailedResponseModel, response_class=JSONResponse)
async def detailed(
    gdf: DetailedDataDep,
    coordinates: CoordinatesDep,
    include_neighbors: IncludeNeighborsDep,
    date_range: DateRangeDep
) -> DetailedResponseModel:
    longitude, latitude = coordinates

    # Validate the inputs
    validate_coordinates(latitude=latitude, longitude=longitude)
    validate_dates(*date_range)

    queried_cell, neighboring_cells = get_data_for_point(
        latitude=latitude, 
        longitude=longitude, 
        include_neighbors=include_neighbors, 
        gdf=gdf,
        date_range=date_range
    )

    detailed_cols = list(DetailedProperties.model_fields.keys())

    sort_columns = ["latitude", "longitude", "step"]

    queried_cell_geojson = dataframe_to_geojson(
        df=queried_cell, 
        columns=detailed_cols,
        sort_columns=sort_columns
    )

    neighboring_cells_geojson = dataframe_to_geojson(
        df=neighboring_cells, 
        columns=detailed_cols, 
        sort_columns=sort_columns
    )
    
    response = DetailedResponseModel(
        queried_cell=queried_cell_geojson,
        neighboring_cells=neighboring_cells_geojson
    )

    return response

@router.get("/threshold", response_model=ThresholdResponseModel, response_class=JSONResponse)
async def threshold(
    gdf: ThresholdDataDep,
    coordinates: CoordinatesDep,
) -> ThresholdResponseModel:  
    longitude, latitude = coordinates

    # Validate the inputs
    validate_coordinates(latitude=latitude, longitude=longitude)

    queried_cell, _ = get_data_for_point(
        latitude=latitude, 
        longitude=longitude, 
        gdf=gdf,
    )

    threshold_cols = list(ThresholdProperties.model_fields.keys())

    queried_cell_geojson = dataframe_to_geojson(
        df=queried_cell, 
        columns=threshold_cols, 
    )

    response = ThresholdResponseModel(
        queried_cell=queried_cell_geojson,
    )

    return response