from fastapi import APIRouter
from api.metrics.v1.cpu import cpu_router as cpu_v1_router
from api.metrics.v1.disk import disk_router as disk_v1_router

router = APIRouter()
router.include_router(cpu_v1_router, prefix="/metrics/v1/cpu")
router.include_router(disk_v1_router, prefix="/metrics/v1/disk")

__all__ = ["router"]