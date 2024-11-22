from uuid import UUID as UUID4

from sqlalchemy import select

from database.models.open_port import OpenPort
from database.repos.base import BaseAlchemyRepo


class OpenPortsRepo(BaseAlchemyRepo):
    async def create(
        self,
        uuid: UUID4,
        ip: str,
        port: int,
        type: str | None,
        protocol: str | None,
        service: str | None,
        version: str | None,
    ) -> OpenPort:
        port = OpenPort(
            id=uuid,
            ip=ip,
            port=port,
            type=type,
            protocol=protocol,
            service=service,
            version=version,
        )
        self.session.add(port)
        await self.session.commit()
        return port

    async def get_by_ip_and_uuid(self, ip: str, uuid: UUID4) -> list[OpenPort]:
        query = select(OpenPort).where(OpenPort.ip == ip, OpenPort.id == uuid)
        ports = await self.session.scalars(query)
        return list(ports)

