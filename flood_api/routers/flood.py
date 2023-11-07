from fastapi import APIRouter

from flood_api.dependencies.flooddata import DetailedFloodDataDep
from flood_api.dependencies.queryparams import CoordinatesDep, DateRangeDep

router = APIRouter(tags=["flood"])


@router.get("/detailed")
async def detailed(
    data: DetailedFloodDataDep, coordinates: CoordinatesDep, date_range: DateRangeDep
):
    lon, lat = coordinates
    start_date, end_date = date_range
    return {
        "lon": lon,
        "lat": lat,
        "start_date": start_date,
        "end_date": end_date,
        "count": len(data),
    }
