import uuid
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from faststream.nats import NatsBroker
from pydantic import UUID4

from app.errors.scans import InvalidIP, InvalidIPCIDR, InvalidIPRange
from database.repos.scan_port import ScanPortsRepo
from database.repos.scan_result import ScanResultRepo
from schemas.scan_api import (
    IpSchema,
    LastScans,
    PortSchema,
    PortsSchema,
    ScanRequest,
    ScanResponse,
    ScanTaskResponse,
)
from schemas.scan_query import ScanStartSchema
from utils.ip_validate import convert_ip


MAX_IP_PER_TASK = 128

router = APIRouter()


@router.post("/scans/")
@inject
async def start_scan(
    scan_request: ScanRequest,
    broker: FromDishka[NatsBroker],
) -> ScanResponse:
    ips = convert_ip(scan_request.ip)
    if ips is None:
        raise InvalidIP

    task_id = str(uuid.uuid4())

    if isinstance(ips, (IPv4Address, IPv6Address)):
        await broker.publish(
            ScanStartSchema(
                task_id=task_id,
                ips=[str(ips)],
                ipv6=isinstance(ips, IPv6Address),
            ),
            subject="scan-start",
        )
    elif isinstance(ips, (IPv4Network, IPv6Network)):
        if ips.num_addresses > MAX_IP_PER_TASK:
            raise InvalidIPCIDR
        await broker.publish(
            ScanStartSchema(
                task_id=task_id,
                ips=[str(ip) for ip in ips],
                ipv6=isinstance(ips, IPv6Network),
            ),
            subject="scan-start",
        )
    elif isinstance(ips, tuple) and len(ips) == 2:
        left, right = int(ips[0]), int(ips[1])
        ip_range: list[IPv4Address] = []

        if left > right or right - left + 1 > MAX_IP_PER_TASK:
            raise InvalidIPRange

        while left <= right:
            ip_range.append(IPv4Address(left))
            left += 1

        await broker.publish(
            ScanStartSchema(
                task_id=task_id,
                ips=[str(ip) for ip in ip_range],
                ipv6=False,
            ),
            subject="scan-start",
        )
    elif isinstance(ips, list):
        if len(ips) > MAX_IP_PER_TASK:
            raise InvalidIPRange

        await broker.publish(
            ScanStartSchema(
                task_id=task_id,
                ips=[str(ip) for ip in ips],
                ipv6=isinstance(ips[0], IPv6Address),
            ),
            subject="scan-start",
        )
    else:
        raise InvalidIP

    return ScanResponse(task_id=task_id)


@router.get("/scans/last/")
@inject
async def get_last_scan(
    limit: int = Query(default=10, ge=1, le=20),
    offset: int = Query(default=0, ge=0, le=10),
    scan_repo: FromDishka[ScanResultRepo] = None,
) -> list[LastScans]:
    return [
        LastScans(
            task_id=str(scan.id),
            ip=scan.ip,
            updated_at=scan.updated_at.timestamp(),
        )
        for scan in await scan_repo.get_last_scans(limit=limit, offset=offset)
    ]


@router.get("/scans/{task_id}/")
@inject
async def get_scan(
    task_id: UUID4,
    scan_repo: FromDishka[ScanResultRepo],
    ports_repo: FromDishka[ScanPortsRepo],
) -> ScanTaskResponse:
    scan_result = await scan_repo.get_by_uuid(uuid=task_id)
    data = {
        "task_id": task_id,
        "end": all(result.end for result in scan_result),
        "ips": [],
    }

    for result in scan_result:
        ports = await ports_repo.get_by_uuid_ip(task_id, result.ip)
        ports_schema = {"open": [], "closed": []}
        for port in ports:
            if port.status == "open":
                ports_schema["open"].append(PortSchema.model_validate(port))
            else:
                ports_schema["closed"].append(port.port)

        data["ips"].append(
            IpSchema(
                ip=result.ip,
                ptr=result.ptr_record,
                ports=PortsSchema.model_validate(ports_schema),
            ),
        )

    return ScanTaskResponse.model_validate(data)
