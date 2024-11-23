from uuid import UUID as UUID4

from sqlalchemy import select

from database.models.scan_result import ScanResult
from database.repos.base import BaseAlchemyRepo


class ScanResultRepo(BaseAlchemyRepo):
    async def create(
        self,
        uuid: UUID4,
        ip: str,
        ptr_record: str,
        severity: str,
    ) -> ScanResult:
        scan = ScanResult(id=uuid, ip=ip, ptr_record=ptr_record, severity=severity)
        self.session.add(scan)
        await self.session.commit()
        return scan

    async def get_by_uuid(self, uuid: UUID4) -> list[ScanResult]:
        query = select(ScanResult).where(ScanResult.id == uuid)
        ips = await self.session.scalars(query)
        return list(ips)

    async def get_by_ip(self, ip: str) -> list[ScanResult]:
        query = select(ScanResult).where(ScanResult.ip == ip)
        ips = await self.session.scalars(query)
        return list(ips)

    async def get_by_ip_and_uuid(self, ip: str, uuid: UUID4) -> ScanResult | None:
        query = select(ScanResult).where(ScanResult.ip == ip, ScanResult.id == uuid)
        return await self.session.scalar(query)

    async def get_last_scans(self, limit: int, offset: int) -> list[ScanResult]:
        query = select(ScanResult).order_by(ScanResult.updated_at.desc())
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await self.session.scalars(query)
        return list(result)
