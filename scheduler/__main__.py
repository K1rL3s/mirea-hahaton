import asyncio
import contextlib
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer
from loguru import logger

from di.container import make_container
from scheduler.config import get_scheduler_config
from scheduler.tasks import include_tasks

# from scheduler.tasks.vullist import process_vulnerabilities


async def run_on_start(container: AsyncContainer) -> None:
    return
    # await process_vulnerabilities(container)


async def app() -> None:
    config = get_scheduler_config()
    container = make_container()

    scheduler = AsyncIOScheduler()
    include_tasks(scheduler, container, config)

    logger.info("Запуск on_start задач")
    await run_on_start(container)
    logger.info("Конец выполнения on_start задач")

    scheduler.start()
    logger.info("Запущен планировщик")

    try:
        while True:
            await asyncio.sleep(24 * 60 * 60)
    finally:
        scheduler.shutdown()
        await container.close()
        logger.info("Планировщик остановлен")


if __name__ == "__main__":
    with contextlib.suppress(ImportError):
        import uvloop as _uvloop

        asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(app())
