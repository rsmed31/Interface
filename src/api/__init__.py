from fastapi import APIRouter
from api.metrics.v1.cpu import cpu_router as cpu_v1_router
from api.metrics.v1.disk import disk_router as disk_v1_router
from api.metrics.v1.log import log_router as log_v1_router
from api.metrics.v1.ram import ram_router as ram_v1_router
from api.metrics.v1.user import user_router as user_v1_router


router = APIRouter()
router.include_router(cpu_v1_router, prefix="/metrics/v1/cpu")
router.include_router(disk_v1_router, prefix="/metrics/v1/disk")
router.include_router(log_v1_router, prefix="/metrics/v1/log")
router.include_router(ram_v1_router, prefix="/metrics/v1/ram")
router.include_router(user_v1_router, prefix="/metrics/v1/users")


__all__ = ["router"]
