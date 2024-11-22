from contextlib import asynccontextmanager

from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from app.routes import include_routers
from di.container import make_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    include_routers(app)

    container = make_container(extra_providers=[FastapiProvider()])
    setup_dishka(container, app)

    return app
