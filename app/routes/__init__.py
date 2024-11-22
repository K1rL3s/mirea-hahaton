from fastapi import FastAPI

from .scan import router as scan_router
from .ws import api_router as api_ws_router
from .ws import nats_router as nats_ws_router


def include_routers(app: FastAPI) -> None:
    for router in (
        scan_router,
        api_ws_router,
        nats_ws_router,
    ):
        app.include_router(router)
