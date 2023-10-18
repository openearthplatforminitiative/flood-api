from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.1.0"
    uvicorn_port: int = 8080
    uvicorn_host: str = "0.0.0.0"
    uvicorn_reload: bool = True
    uvicorn_proxy_headers: bool = False
