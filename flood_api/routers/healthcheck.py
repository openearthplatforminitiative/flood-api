from fastapi import APIRouter
from fastapi import Response
from healthcheck import HealthCheck
from flood_api.settings import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def liveness() -> dict[str, str]:
    return {"message": "Ok"}


@router.get("/ready", tags=["health"])
async def ready() -> Response:
    health = HealthCheck()

    health.add_section("version", settings.version)

    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)
