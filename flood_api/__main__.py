from fastapi import FastAPI
from flood_api.settings import Settings
from flood_api.routers import healthcheck

settings = Settings()
app = FastAPI(title="Flood API", version=settings.version)
app.include_router(healthcheck.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "flood_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
