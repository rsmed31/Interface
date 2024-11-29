# FILE: src/api/metrics/v1/ram.py
from fastapi import APIRouter, Request, HTTPException
from domain.schemas.ram import GetRamResponseSchema

ram_router = APIRouter()

@ram_router.get("/usage", response_model=GetRamResponseSchema)
async def get_ram_usage(request: Request) -> GetRamResponseSchema:
    """Route to get RAM usage data."""
    try:
        ram_stats = request.app.state.monitortask.get_ram_usage()
        if not ram_stats:
            raise HTTPException(status_code=500, detail="RAM stats not available")
        return GetRamResponseSchema(**ram_stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))