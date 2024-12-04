from fastapi import APIRouter
from api.metrics.v1.cpu import cpu_router as cpu_v1_router
from api.metrics.v1.disk import disk_router as disk_v1_router
from api.metrics.v1.ram import ram_router as ram_v1_router

router = APIRouter()
router.include_router(cpu_v1_router, prefix="/metrics/v1/cpu")
router.include_router(disk_v1_router, prefix="/metrics/v1/disk")
router.include_router(ram_v1_router, prefix="/metrics/v1/ram")

_all_ = ["router"]