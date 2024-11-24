import asyncio
import contextlib
import sys

from dishka.integrations.faststream import FastStreamProvider, setup_dishka
from faststream import FastStream
from faststream.nats import NatsBroker

from di.container import make_container
from query.config import NatsConfig


async def create_app() -> tuple[FastStream, int]:

    container = make_container(extra_providers=[FastStreamProvider()])
    config = await container.get(NatsConfig)
    broker = await container.get(NatsBroker)
    app = FastStream(broker)

    setup_dishka(container, app, auto_inject=True)

    return app, config.workers


async def main() -> None:
    app, workers = await create_app()
    await app.run(run_extra_options={"workers": str(workers)})


if __name__ == "__main__":
    with contextlib.suppress(ImportError):
        import uvloop as _uvloop

        asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
