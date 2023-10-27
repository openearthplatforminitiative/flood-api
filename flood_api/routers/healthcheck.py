from fastapi import APIRouter, Depends
from fastapi import Response
from healthcheck import HealthCheck
from sqlalchemy import text
from sqlalchemy.orm import Session

from flood_api.db import database
from flood_api.settings import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def liveness() -> dict[str, str]:
    return {"message": "Ok"}


@router.get("/ready", tags=["health"])
async def ready(session: Session = Depends(database.get_session)) -> Response:
    def database_version() -> (bool, str):
        try:
            version = session.execute(text("SELECT version()")).scalar()
            return True, version
        except Exception as e:
            print(e)
            return False, "Not Available"

    def postgis_version() -> (bool, str):
        try:
            version = session.execute(text("SELECT PostGIS_Version()")).scalar()
            return True, version
        except Exception as e:
            print(e)
            return False, "Not Available"

    health = HealthCheck()

    health.add_section("version", settings.version)
    health.add_check(database_version)
    health.add_check(postgis_version)

    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)
