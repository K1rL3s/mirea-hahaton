import asyncio
import contextlib
import sys
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import get_api_config
from app.routes import include_routers
from di.container import make_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    include_routers(app)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = make_container(extra_providers=[FastapiProvider()])
    setup_dishka(container, app)

    return app


def main() -> None:
    app = create_app()
    config = get_api_config()
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        uvicorn.run(app=app, host="0.0.0.0", port=config.port, workers=1)


if __name__ == "__main__":
    with contextlib.suppress(ImportError):
        import uvloop as _uvloop

        asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
