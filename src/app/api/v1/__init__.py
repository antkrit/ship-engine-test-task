from fastapi import APIRouter

from .addresses import router as addresses_router
from .health import router as health_router
from .tasks import router as tasks_router

router = APIRouter(prefix="/v1")
router.include_router(health_router)
router.include_router(tasks_router)
router.include_router(addresses_router)
