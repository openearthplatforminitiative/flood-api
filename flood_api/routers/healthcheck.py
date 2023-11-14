import s3fs
from fastapi import APIRouter, Response
from healthcheck import HealthCheck

from flood_api.settings import settings

router = APIRouter(tags=["health"])


def summary_data_available():
    s3 = s3fs.S3FileSystem(anon=True)
    if s3.exists(settings.summary_data_path):
        return True, "Summary data available"
    else:
        return False, "Summary data not available"


def detailed_data_available():
    s3 = s3fs.S3FileSystem(anon=True)
    if s3.exists(settings.detailed_data_path):
        return True, "Detailed data available"
    else:
        return False, "Detailed data not available"


def threshold_data_available():
    s3 = s3fs.S3FileSystem(anon=True)
    if s3.exists(settings.threshold_data_path):
        return True, "Threshold data available"
    else:
        return False, "Threshold data not available"


health = HealthCheck()
health.add_section("version", settings.version)
health.add_check(summary_data_available)
health.add_check(detailed_data_available)
health.add_check(threshold_data_available)


@router.get(
    "/ready",
    summary="Check if this service is ready to receive requests",
    description="Returns a message describing the status of this service",
)
async def ready() -> Response:
    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)


@router.get(
    "/health",
    summary="Check if this service is alive",
    description="Returns a simple message to indicate that this service is alive",
)
def liveness() -> dict[str, str]:
    return {"message": "Ok"}
