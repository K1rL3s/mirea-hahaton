from fastapi import FastAPI

from .scans import router as scan_router
from .convert import router as convert_router


def include_routers(app: FastAPI) -> None:
    for router in (
        scan_router,
        convert_router,
    ):
        app.include_router(router)
