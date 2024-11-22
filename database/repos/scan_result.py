from uuid import UUID as UUID4

from database.models.scan_result import ScanResult
from database.repos.base import BaseAlchemyRepo


class ScanResultRepo(BaseAlchemyRepo):
    async def create(self, port: ScanResult) -> None:
        pass

    async def get_by_uuid(self, uuid: UUID4) -> ScanResult | None:
        pass

    async def get_by_ip(self, ip: str) -> ScanResult | None:
        pass
