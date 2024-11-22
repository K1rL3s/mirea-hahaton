from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, close_all_sessions

from database.config import DBConfig, get_db_config
from database.connection import init_database


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def db_config(self) -> DBConfig:
        return get_db_config()

    @provide(scope=Scope.APP)
    async def sessionmaker(
        self,
        db_config: DBConfig,
    ) -> AsyncIterable[async_sessionmaker[AsyncSession]]:
        sessionmaker = await init_database(db_config)
        yield sessionmaker
        await close_all_sessions()

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session
