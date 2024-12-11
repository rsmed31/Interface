from fastapi import APIRouter, Request, HTTPException
from domain.schemas.disk import GetDiskResponseSchema

disk_router = APIRouter()

@disk_router.get("/usage", response_model=GetDiskResponseSchema)
async def get_disk_usage(request: Request) -> GetDiskResponseSchema:
    """Route to get disk usage data."""
    try:
        disk_stats = request.app.state.monitortask.get_disk_usage()
        if not disk_stats:
            raise HTTPException(status_code=500, detail="Disk stats not available")
        return GetDiskResponseSchema(**disk_stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e