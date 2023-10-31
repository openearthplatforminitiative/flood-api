import asyncio
from datetime import timezone
from typing import Annotated

import geopandas as gpd
import pandas as pd
from aiocron import crontab
from fastapi import FastAPI, Request, Depends
from shapely import wkt

from flood_api.settings import settings


def fetch_parquet(path) -> gpd.GeoDataFrame:
    print(f"Reloading data from {path}")

    df = pd.read_parquet(
        path,
        engine="fastparquet",
        storage_options={"anon": True},
    )

    # Convert WKT strings to geometry objects
    df["geometry"] = df["wkt"].apply(wkt.loads)

    gdf = gpd.GeoDataFrame(df, geometry="geometry").drop(columns="wkt")

    print(f"Done reloading data from {path}")

    return gdf


def get_summary_data(request: Request) -> gpd.GeoDataFrame | None:
    return request.app.flood_data_summary


def get_detailed_data(request: Request) -> gpd.GeoDataFrame | None:
    return request.app.flood_data_detailed


SummaryFloodDataDep = Annotated[gpd.GeoDataFrame, Depends(get_summary_data)]
DetailedFloodDataDep = Annotated[gpd.GeoDataFrame, Depends(get_detailed_data)]


async def flood_data_fetcher(app: FastAPI):
    print("Flood data fetcher running")
    schedule = crontab("0 12 * * * *", tz=timezone.utc)
    while True:
        await schedule.next()
        await fetch_flood_data(app)


async def fetch_flood_data(app: FastAPI):
    loop = asyncio.get_event_loop()
    (
        app.flood_data_summary,
        app.flood_data_detailed,
    ) = await asyncio.gather(
        # loop.run_in_executor to prevents blocking the main thread
        loop.run_in_executor(None, fetch_parquet, settings.flood_data_path_summary),
        loop.run_in_executor(None, fetch_parquet, settings.flood_data_path_detailed),
    )
