from contextlib import asynccontextmanager

from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import include_routers
from di.container import make_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, root_path="/api")
    include_routers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = make_container(extra_providers=[FastapiProvider()])
    setup_dishka(container, app)

    return app


app = create_app()
