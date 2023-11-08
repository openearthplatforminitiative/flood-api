from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from flood_api.dependencies.flooddata import (DetailedDataDep,
                                              SummaryDataDep,
                                              ThresholdDataDep)
from flood_api.dependencies.queryparams import (CoordinatesDep, 
                                                DateRangeDep,
                                                IncludeNeighborsDep)
from flood_api.utils.geospatial_operations import get_data_for_point
from flood_api.utils.json_utilities import (dataframe_to_geojson, 
                                            custom_date_handler)
from flood_api.utils.validation_helpers import point_within_roi

router = APIRouter(tags=["flood"])

@router.get("/summary", response_class=JSONResponse)
async def summary(
    gdf: SummaryDataDep,
    coordinates: CoordinatesDep,
    include_neighbors: IncludeNeighborsDep,
):
    longitude, latitude = coordinates

    # Check if the queried point is within the ROI
    if not point_within_roi(latitude=latitude, longitude=longitude):
        raise HTTPException(status_code=400, detail="Queried coordinates are outside the region of interest")

    queried_cell, neighboring_cells = get_data_for_point(latitude=latitude, longitude=longitude, 
                                                         include_neighbors=include_neighbors, gdf=gdf)

    summary_cols = [
        "time", "peak_step", "peak_day", "peak_timing", "max_median_dis", 
        "min_median_dis", "control_dis", "max_max_dis", "min_min_dis", "tendency",
        "max_p_above_20y", "max_p_above_5y", "max_p_above_2y", "intensity"
    ]

    queried_cell_geojson = dataframe_to_geojson(
        df=queried_cell, columns=summary_cols, date_handler=custom_date_handler)
    
    sort_columns = ["latitude", "longitude"]

    neighboring_cells_geojson = dataframe_to_geojson(
        df=neighboring_cells, columns=summary_cols, 
        date_handler=custom_date_handler, sort_columns=sort_columns)

    return {
        "queried_cell": queried_cell_geojson,
        "neighboring_cells": neighboring_cells_geojson
    }

@router.get("/detailed", response_class=JSONResponse)
async def detailed(
    gdf: DetailedDataDep,
    coordinates: CoordinatesDep,
    include_neighbors: IncludeNeighborsDep,
    date_range: DateRangeDep
):
    longitude, latitude = coordinates

    # Check if the queried point is within the ROI
    if not point_within_roi(latitude=latitude, longitude=longitude):
        raise HTTPException(status_code=400, detail="Queried coordinates are outside the region of interest")

    queried_cell, neighboring_cells = get_data_for_point(
        latitude=latitude, 
        longitude=longitude, 
        include_neighbors=include_neighbors, 
        gdf=gdf,
        date_range=date_range
    )

    detailed_cols = [
        "time", "valid_time", "step", "p_above_2y", "p_above_5y", 
        "p_above_20y", "min_dis", "Q1_dis", "median_dis", "Q3_dis", "max_dis"
    ]

    sort_columns = ["latitude", "longitude", "step"]

    queried_cell_geojson = dataframe_to_geojson(
        df=queried_cell, columns=detailed_cols, 
        date_handler=custom_date_handler, sort_columns=sort_columns)

    neighboring_cells_geojson = dataframe_to_geojson(
        df=neighboring_cells, columns=detailed_cols, 
        date_handler=custom_date_handler, sort_columns=sort_columns)

    return {
        "queried_cell": queried_cell_geojson,
        "neighboring_cells": neighboring_cells_geojson
    }

@router.get("/threshold", response_class=JSONResponse)
async def threshold(
    gdf: ThresholdDataDep,
    coordinates: CoordinatesDep,
):  
    longitude, latitude = coordinates

    # Check if the queried point is within the ROI
    if not point_within_roi(latitude=latitude, longitude=longitude):
        raise HTTPException(status_code=400, detail="Queried coordinates are outside the region of interest")

    queried_cell, _ = get_data_for_point(
        latitude=latitude, 
        longitude=longitude, 
        include_neighbors=False, 
        gdf=gdf,
        date_range=None
    )

    threshold_cols = [
        "2y_threshold", "5y_threshold", "20y_threshold"
    ]

    queried_cell_geojson = dataframe_to_geojson(
        df=queried_cell, 
        columns=threshold_cols, 
        date_handler=None, 
        sort_columns=None
    )

    return {
        "queried_cell": queried_cell_geojson,
    }
