from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseAlchemyRepo(ABC):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
