from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from database.repos.scan_port import ScanPortsRepo
from database.repos.scan_result import ScanResultRepo
from database.repos.vuls import VulsRepo


class ReposProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def open_ports(self, session: AsyncSession) -> ScanPortsRepo:
        return ScanPortsRepo(session)

    @provide(scope=Scope.REQUEST)
    def scan_results(self, session: AsyncSession) -> ScanResultRepo:
        return ScanResultRepo(session)

    @provide(scope=Scope.REQUEST)
    def vuls(self, session: AsyncSession) -> VulsRepo:
        return VulsRepo(session)
