from pydantic_settings import BaseSettings
from os import environ


class Settings(BaseSettings):
    version: str = "0.0.1"
    uvicorn_port: int = 8080
    uvicorn_host: str = "0.0.0.0"
    uvicorn_reload: bool = True
    uvicorn_proxy_headers: bool = False
    dagster_data_bucket: str = environ.get("dagster_data_bucket", "placeholder-bucket")
    detailed_data_path: str = (
        f"s3://{dagster_data_bucket}/flood/detailed_forecast_subarea/"
    )
    summary_data_path: str = (
        f"s3://{dagster_data_bucket}/flood/summary_forecast_subarea/"
    )
    threshold_data_path: str = (
        f"s3://{dagster_data_bucket}/flood/rp_combined_thresh_pq.parquet"
    )
    api_root_path: str = ""
    api_description: str = (
        "This is a RESTful service that provides accurate and up-to-date "
        "flood information for the geographic region bounded by the following "
        "coordinates: `min_lon=-18.0`, `min_lat=-6.0`, `max_lon=52.0`, `max_lat=17.0`."
        "<br/>The data are produced for the <a href='https://www.globalfloods.eu/'>Global "
        "Flood Awareness System</a> and sourced from the "
        "<a href='https://cds.climate.copernicus.eu/cdsapp#!/dataset/cems-glofas-forecast?tab=overview'>"
        "Copernicus Climate Data Store</a>. <br/>Please note that the datasets are licensed under "
        "the <a href='https://www.globalfloods.eu/terms-of-service/'>CEMS-FLOODS datasets licence</a>, "
        "which is not a standard open license. We use them in our pre-project to explore relevant data."
    )
    glofas_roi: dict = {
        "min_lat": -6.0,
        "max_lat": 17.0,
        "min_lon": -18.0,
        "max_lon": 52.0,
    }
    glofas_resolution: float = 0.05
    glofas_precision: int = 3
    api_domain: str = "localhost"

    @property
    def api_url(self):
        if self.api_domain == "localhost":
            return f"http://{self.api_domain}:{self.uvicorn_port}"
        else:
            return f"https://{self.api_domain}{self.api_root_path}"


settings = Settings()
