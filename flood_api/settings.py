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
    api_description: str = 'This is a RESTful service that provides accurate and up-to-date flood information for the geographic region bounded by the following coordinates: min_lon=-18.0, min_lat=-6.0, max_lon=52.0, max_lat=17.0. <br/>The data are sourced from <a href="https://cds.climate.copernicus.eu/cdsapp#!/dataset/cems-glofas-forecast?tab=overview">https://cds.climate.copernicus.eu/cdsapp#!/dataset/cems-glofas-forecast?tab=overview</a>. <br/>The data are freely available for use under the <a href="https://cds.climate.copernicus.eu/api/v2/terms/static/cems-floods.pdf">CEMS-FLOODS datasets licence</a>.'
    glofas_roi: dict = {
        "min_lat": -6.0,
        "max_lat": 17.0,
        "min_lon": -18.0,
        "max_lon": 52.0,
    }
    glofas_resolution: float = 0.05
    glofas_precision: int = 3
    out_of_bounds_query_status_code: int = 404
    invalid_query_status_code: int = 400


settings = Settings()
