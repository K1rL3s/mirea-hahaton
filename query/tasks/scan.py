import asyncio

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.nats import NatsRouter
from faststream.nats.annotations import NatsBroker

from database.repos.scan_port import ScanPortsRepo
from database.repos.scan_result import ScanResultRepo
from query.utils.nmap import make_nmap_command, read_nmap_stream
from schemas.scan_query import (
    ScanIPSchema,
    ScanPortSchema,
    ScanResultSchema,
    ScanStartSchema,
)

MAX_WORKERS = 2**4  # 16, т.к. 2 гига 2 ядра и страшно очень

router = NatsRouter()


@router.subscriber(subject="scan-start", queue="workers", max_workers=MAX_WORKERS)
@inject
async def scan_start_handler(
    scan_start: ScanStartSchema,
    broker: NatsBroker,
    scan_repo: FromDishka[ScanResultRepo],
) -> None:
    for ip in scan_start.ips:
        await scan_repo.create(uuid=scan_start.task_id, ip=ip)
        await broker.publish(
            message=ScanIPSchema(
                task_id=scan_start.task_id,
                ip=ip,
                flags=scan_start.flags,
            ),
            subject="scan-ip",
        )


@router.subscriber(subject="scan-ip", queue="workers", max_workers=MAX_WORKERS)
async def scan_ip_handler(scan_ip: ScanIPSchema, broker: NatsBroker) -> None:
    process = await asyncio.create_subprocess_exec(
        *(make_nmap_command(scan_ip).split()),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await read_nmap_stream(process.stdout, broker, scan_ip)


@router.subscriber(subject="scan-ip-port", queue="workers", max_workers=MAX_WORKERS)
@inject
async def scan_ip_port_handler(
    scan_ip_port: ScanPortSchema,
    open_ports: FromDishka[ScanPortsRepo],
) -> None:
    await open_ports.create_or_update_from_scan_port_schema(scan_ip_port)


@router.subscriber(subject="scan-ip-final", queue="workers", max_workers=MAX_WORKERS)
@inject
async def scan_ip_final_handler(
    scan_ip_hostname: ScanResultSchema,
    scan_repo: FromDishka[ScanResultRepo],
) -> None:
    await scan_repo.update_from_scan_result_schema(scan_ip_hostname, end=True)
