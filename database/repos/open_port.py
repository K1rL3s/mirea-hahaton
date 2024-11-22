from uuid import UUID as UUID4

from database.models.open_port import OpenPort
from database.repos.base import BaseAlchemyRepo


class OpenPortsRepo(BaseAlchemyRepo):
    async def create(self, port: OpenPort) -> None:
        pass

    async def get_by_uuid(self, uuid: UUID4) -> list[OpenPort]:
        pass

    async def get_by_ip(self, ip: str) -> list[OpenPort]:
        pass
