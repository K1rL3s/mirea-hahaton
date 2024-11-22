from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.exceptions import AckMessage
from faststream.nats import NatsRouter
from faststream.nats.annotations import NatsBroker

from app.ws_manager import WebSocketManager
from schemas.scan_query import ScanIP, ScanPort, ScanStart


router = NatsRouter()


@router.subscriber(subject="scan-start")
async def scan_start_handler(scan_start: ScanStart, broker: NatsBroker) -> None:
    for ip in scan_start.ips:
        await broker.publish(
            message=ScanIP(task_id=scan_start.task_id, ip=ip),
            subject="scan-ip",
        )


@router.subscriber(subject="scan-ip")
async def scan_ip_handler(scan_ip: ScanIP, broker: NatsBroker) -> None:
    # TODO: сюда можно засунуть вызов nmap'а и публиковать результаты по портам
    for port in range(1, 100):
        await broker.publish(
            message=ScanPort(task_id=scan_ip.task_id, ip=scan_ip.ip, port=port),
            subject="scan-ip-port",
        )
