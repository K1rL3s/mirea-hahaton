from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from database.repos.open_port import OpenPortsRepo
from database.repos.scan_result import ScanResultRepo


class ReposProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def open_ports(self, session: AsyncSession) -> OpenPortsRepo:
        return OpenPortsRepo(session)

    @provide(scope=Scope.REQUEST)
    def scan_results(self, session: AsyncSession) -> ScanResultRepo:
        return ScanResultRepo(session)
