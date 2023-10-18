from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}
