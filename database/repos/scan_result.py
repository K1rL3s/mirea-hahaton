from uuid import UUID as UUID4

import sqlalchemy
from sqlalchemy import select

from database.models.scan_result import ScanResultModel
from database.repos.base import BaseAlchemyRepo
from schemas.scan_query import ScanResultSchema


class ScanResultRepo(BaseAlchemyRepo):
    async def create(
        self,
        uuid: UUID4 | str,
        ip: str,
        ptr_record: str | None = None,
        severity: str | None = None,
    ) -> ScanResultModel:
        if isinstance(uuid, str):
            uuid = UUID4(uuid)
        scan = ScanResultModel(id=uuid, ip=ip, ptr_record=ptr_record, severity=severity)
        self.session.add(scan)
        await self.session.commit()
        return scan

    async def get_by_uuid(self, uuid: UUID4) -> list[ScanResultModel]:
        query = select(ScanResultModel).where(ScanResultModel.id == uuid)
        ips = await self.session.scalars(query)
        return list(ips)

    async def get_by_ip(self, ip: str) -> list[ScanResultModel]:
        query = select(ScanResultModel).where(ScanResultModel.ip == ip)
        ips = await self.session.scalars(query)
        return list(ips)

    async def get_by_ip_and_uuid(self, ip: str, uuid: UUID4) -> ScanResultModel | None:
        query = select(ScanResultModel).where(
            ScanResultModel.ip == ip,
            ScanResultModel.id == uuid,
        )
        return await self.session.scalar(query)

    async def get_last_scans(self, limit: int, offset: int) -> list[ScanResultModel]:
        query = select(ScanResultModel).order_by(ScanResultModel.updated_at.desc())
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await self.session.scalars(query)
        return list(result)

    async def update_from_scan_result_schema(
        self,
        scan_result_schema: ScanResultSchema,
    ) -> None:
        query = (
            sqlalchemy.update(ScanResultModel)
            .where(
                ScanResultModel.id == UUID4(scan_result_schema.task_id),
                ScanResultModel.ip == scan_result_schema.ip,
            )
            .values(
                ptr_record=scan_result_schema.ptr_record,
                severity=scan_result_schema.severity,
            )
        )

        await self.session.execute(query)
        await self.session.commit()
