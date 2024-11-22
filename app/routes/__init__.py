from fastapi import FastAPI

from .scan import router as scan_router


def include_routers(app: FastAPI) -> None:
    app.include_router(scan_router)
