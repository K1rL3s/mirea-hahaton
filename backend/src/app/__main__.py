import asyncio
import contextlib
import sys

import uvicorn

from app.config import get_api_config


def main() -> None:
    config = get_api_config()
    uvicorn.run(
        app="app.app:app",
        host="0.0.0.0",
        port=config.port,
        workers=config.workers,
    )


if __name__ == "__main__":
    with contextlib.suppress(ImportError):
        import uvloop as _uvloop

        asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        main()
