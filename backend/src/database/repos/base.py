from sqlalchemy.ext.asyncio import AsyncSession


class BaseAlchemyRepo:
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
