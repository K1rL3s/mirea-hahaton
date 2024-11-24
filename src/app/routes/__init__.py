from fastapi import FastAPI

from .convert import router as convert_router
from .locations import router as locations_router
from .scans import router as scan_router


def include_routers(app: FastAPI) -> None:
    for router in (
        scan_router,
        convert_router,
        locations_router,
    ):
        app.include_router(router)
