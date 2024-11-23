import asyncio
import contextlib
import sys

from dishka.integrations.faststream import FastStreamProvider, setup_dishka
from faststream import FastStream
from faststream.nats import NatsBroker

from di.container import make_container


async def create_app() -> FastStream:
    container = make_container(extra_providers=[FastStreamProvider()])

    broker = await container.get(NatsBroker)
    app = FastStream(broker)

    setup_dishka(container, app, auto_inject=True)

    return app


async def main() -> None:
    app = await create_app()
    await app.run()


if __name__ == "__main__":
    with contextlib.suppress(ImportError):
        import uvloop as _uvloop

        asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
