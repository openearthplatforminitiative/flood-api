import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from flood_api.dependencies.flooddata import fetch_flood_data, flood_data_fetcher
from flood_api.routers import flood, healthcheck
from flood_api.settings import settings


@asynccontextmanager
async def lifespan(flood_app: FastAPI):
    await fetch_flood_data(flood_app)
    asyncio.create_task(flood_data_fetcher(flood_app))
    yield


app = FastAPI(
    title="Flood API",
    lifespan=lifespan,
    version=settings.version,
    description=settings.api_description,
    root_path=settings.api_root_path,
)
app.include_router(flood.router)
app.include_router(healthcheck.router)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "flood_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
