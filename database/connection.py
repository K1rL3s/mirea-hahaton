from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from database.config import DBConfig

POOL_SIZE = 5
MAX_POOL_OVERFLOW = 10
CONNECT_TIMEOUT = 10


sessionmaker_kwargs = {
    "autoflush": False,
    "future": True,
    "expire_on_commit": False,
}


async def init_database(
    db_settings: DBConfig,
    **kwargs: Any,
) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(db_settings)

    # Проверка подключения к базе данных
    async with engine.begin():
        pass

    return async_sessionmaker(bind=engine, **{**sessionmaker_kwargs, **kwargs})


def create_engine(config: DBConfig) -> AsyncEngine:
    return create_async_engine(
        str(config.db_url),
        pool_size=POOL_SIZE,
        max_overflow=MAX_POOL_OVERFLOW,
        connect_args={"connect_timeout": CONNECT_TIMEOUT},
    )
