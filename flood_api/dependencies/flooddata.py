import asyncio
import logging
from datetime import timezone
from typing import Annotated

import geopandas as gpd
import pandas as pd
from aiocron import crontab
from fastapi import Depends, FastAPI, Request
from shapely import wkt

from flood_api.models.detailed_types import DetailedProperties
from flood_api.models.summary_types import SummaryProperties
from flood_api.settings import settings

logger = logging.getLogger(__name__)


def fetch_parquet(path) -> gpd.GeoDataFrame:
    logger.info("Reloading data from %s", path)

    df = pd.read_parquet(
        path,
        engine="fastparquet",
        storage_options={"anon": True},
    )

    # Convert date fields to date objects
    date_fields = set(
        DetailedProperties.get_date_fields() + SummaryProperties.get_date_fields()
    )
    for col in date_fields:
        if col in df.columns and isinstance(df[col].iloc[0], pd.Timestamp):
            df[col] = pd.to_datetime(df[col]).dt.date

    # Convert WKT strings to geometry objects
    df["geometry"] = df["wkt"].apply(wkt.loads)

    gdf = gpd.GeoDataFrame(df, geometry="geometry").drop(columns="wkt")

    logger.info("Done reloading data from %s", path)

    return gdf


def get_summary_data(request: Request) -> gpd.GeoDataFrame | None:
    return request.app.summary_data


def get_detailed_data(request: Request) -> gpd.GeoDataFrame | None:
    return request.app.detailed_data


def get_threshold_data(request: Request) -> gpd.GeoDataFrame | None:
    return request.app.threshold_data


SummaryDataDep = Annotated[gpd.GeoDataFrame, Depends(get_summary_data)]
DetailedDataDep = Annotated[gpd.GeoDataFrame, Depends(get_detailed_data)]
ThresholdDataDep = Annotated[gpd.GeoDataFrame, Depends(get_threshold_data)]


async def flood_data_fetcher(app: FastAPI):
    logger.info("Flood data fetcher running")
    schedule = crontab("0 12 * * * *", tz=timezone.utc)
    while True:
        await schedule.next()
        await fetch_flood_data(app)


async def fetch_flood_data(app: FastAPI):
    loop = asyncio.get_event_loop()
    (
        app.summary_data,
        app.detailed_data,
        app.threshold_data,
    ) = await asyncio.gather(
        # loop.run_in_executor to prevents blocking the main thread
        loop.run_in_executor(None, fetch_parquet, settings.summary_data_path),
        loop.run_in_executor(None, fetch_parquet, settings.detailed_data_path),
        loop.run_in_executor(None, fetch_parquet, settings.threshold_data_path),
    )
