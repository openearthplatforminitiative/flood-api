from fastapi import APIRouter

from flood_api.dependencies.flooddata import DetailedFloodDataDep
from flood_api.dependencies.queryparams import CoordinatesDep, DateRangeDep

router = APIRouter(prefix="/flood", tags=["flood"])


@router.get("/detailed")
async def detailed(
    data: DetailedFloodDataDep, coordinates: CoordinatesDep, date_range: DateRangeDep
):
    lat, lon = coordinates
    start_date, end_date = date_range
    return {
        "lat": lat,
        "lon": lon,
        "start_date": start_date,
        "end_date": end_date,
        "count": len(data),
    }
