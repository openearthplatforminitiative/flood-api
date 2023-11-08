from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    uvicorn_port: int = 8080
    uvicorn_host: str = "0.0.0.0"
    uvicorn_reload: bool = True
    uvicorn_proxy_headers: bool = False
    detailed_data_path: str = "s3://databricks-data-openepi/glofas/processed/newest/processed_detailed_forecast.parquet/"
    summary_data_path: str = "s3://databricks-data-openepi/glofas/processed/newest/processed_summary_forecast.parquet/"
    threshold_data_path: str = "s3://databricks-data-openepi/glofas/auxiliary-data/processed_thresholds.parquet/"
    api_root_path: str = "/"


settings = Settings()
