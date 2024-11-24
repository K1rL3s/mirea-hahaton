from uuid import UUID as UUID4

import sqlalchemy

from database.models.scan_port import ScanPortModel
from database.repos.base import BaseAlchemyRepo
from schemas.query.scan_query import ScanPortSchema


class ScanPortsRepo(BaseAlchemyRepo):
    async def create(
        self,
        uuid: UUID4,
        ip: str,
        port: int,
        protocol: str,
        status: str | None,
        service: str | None,
        version: str | None,
        reason: str | None,
    ) -> ScanPortModel:
        port = ScanPortModel(
            id=uuid,
            ip=ip,
            port=port,
            protocol=protocol,
            status=status,
            service=service,
            version=version,
            reason=reason,
        )
        self.session.add(port)
        await self.session.commit()
        return port

    async def get_by_uuid_ip(
        self,
        uuid: UUID4,
        ip: str,
    ) -> list[ScanPortModel]:
        query = sqlalchemy.select(ScanPortModel).where(
            ScanPortModel.ip == ip,
            ScanPortModel.id == uuid,
        )
        return list(await self.session.scalars(query))

    async def get_by_uuid_ip_port(
        self,
        uuid: UUID4,
        ip: str,
        port: int,
    ) -> ScanPortModel | None:
        query = sqlalchemy.select(ScanPortModel).where(
            ScanPortModel.ip == ip,
            ScanPortModel.id == uuid,
            ScanPortModel.port == port,
        )
        return await self.session.scalar(query)

    async def create_or_update_from_scan_port_schema(
        self,
        scan_port_schema: ScanPortSchema,
    ) -> None:
        port = await self.get_by_uuid_ip_port(
            UUID4(scan_port_schema.task_id),
            scan_port_schema.ip,
            scan_port_schema.port,
        )
        if port:
            query = (
                sqlalchemy.update(ScanPortModel)
                .where(
                    ScanPortModel.ip == scan_port_schema.ip,
                    ScanPortModel.id == UUID4(scan_port_schema.task_id),
                    ScanPortModel.port == scan_port_schema.port,
                )
                .values(
                    status=scan_port_schema.state,
                    service=scan_port_schema.service,
                    version=scan_port_schema.version,
                    reason=scan_port_schema.reason,
                )
            )
            await self.session.execute(query)
        else:
            port = ScanPortModel(
                id=UUID4(scan_port_schema.task_id),
                ip=scan_port_schema.ip,
                port=scan_port_schema.port,
                protocol=scan_port_schema.protocol,
                status=scan_port_schema.state,
                service=scan_port_schema.service,
                version=scan_port_schema.version,
                reason=scan_port_schema.reason,
            )
            self.session.add(port)

        await self.session.commit()
