from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer

from scheduler.config import SchedulerConfig

from .vullist import process_vulnerabilities


def include_tasks(
    scheduler: AsyncIOScheduler,
    container: AsyncContainer,
    config: SchedulerConfig,
) -> None:
    scheduler.add_job(
        process_vulnerabilities,
        trigger="cron",
        args=[container],
        hour=f"*/{config.delay}",
    )
