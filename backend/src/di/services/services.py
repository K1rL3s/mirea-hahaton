from dishka import Provider, Scope, provide
from faststream.nats import NatsBroker

from database.repos.scan_port import ScanPortsRepo
from database.repos.scan_result import ScanResultRepo
from services.scans.start import ScanStartService
from services.scans.task import ScanTaskService


class ServicesProvider(Provider):
    @provide(scope=Scope.APP)
    def scan_start(self, broker: NatsBroker) -> ScanStartService:
        return ScanStartService(broker)

    @provide(scope=Scope.REQUEST)
    def scan_task(
        self,
        scan_repo: ScanResultRepo,
        ports_repo: ScanPortsRepo,
    ) -> ScanTaskService:
        return ScanTaskService(scan_repo, ports_repo)
