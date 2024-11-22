from fastapi import APIRouter, Request
from domain.schemas.disk import GetDiskResponseSchema

disk_router = APIRouter()

@disk_router.get("/usage", response_model=GetDiskResponseSchema)
async def get_disk_usage(request: Request) -> GetDiskResponseSchema:
    """
    Route to get disk usage data.

    Args:
        request (Request): The incoming request.

    Returns:
        dict: Disk usage statistics.
    """
    disk_stats = request.app.state.monitortask.get_disk_usage()
    return GetDiskResponseSchema(**disk_stats)
