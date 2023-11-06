from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    uvicorn_port: int = 8080
    uvicorn_host: str = "0.0.0.0"
    uvicorn_reload: bool = True
    uvicorn_proxy_headers: bool = False
    flood_data_path_detailed: str = (
        "s3://openepi-public-data/processed_detailed_forecast.parquet/"
    )
    flood_data_path_summary: str = (
        "s3://openepi-public-data/processed_summary_forecast.parquet/"
    )
    api_root_path: str = "/"


settings = Settings()
