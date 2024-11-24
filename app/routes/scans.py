from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from pydantic import UUID4

from app.exceptions.scans import InvalidIP, InvalidIPCIDR, InvalidIPRange
from database.repos.scan_result import ScanResultRepo
from schemas.scan_api import LastScans, ScanRequest, ScanResponse, ScanTaskResponse
from services.scan_start import ScanStartService
from services.scan_task import ScanTaskService
from utils.ip_validate import convert_ip

MAX_IP_PER_TASK = 128

router = APIRouter()


@router.post("/scans/")
@inject
async def start_scan(
    scan_request: ScanRequest,
    scan_start_service: FromDishka[ScanStartService],
) -> ScanResponse:
    ips = convert_ip(scan_request.ip)
    if ips is None:
        raise InvalidIP

    if isinstance(ips, (IPv4Address, IPv6Address)):
        task_id = await scan_start_service.start_one_ip(ips)

    elif isinstance(ips, (IPv4Network, IPv6Network)):
        if ips.num_addresses > MAX_IP_PER_TASK:
            raise InvalidIPCIDR
        task_id = await scan_start_service.start_ip_network(ips)

    elif isinstance(ips, tuple) and len(ips) == 2:
        left, right = int(ips[0]), int(ips[1])
        if left > right or right - left + 1 > MAX_IP_PER_TASK:
            raise InvalidIPRange
        task_id = await scan_start_service.start_ip_range(ips[0], ips[1])

    elif isinstance(ips, list):
        if len(ips) > MAX_IP_PER_TASK:
            raise InvalidIPRange
        task_id = await scan_start_service.start_ip_list(ips)

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
        LastScans(task_id=str(scan.id), ip=scan.ip, updated_at=scan.updated_at)
        for scan in await scan_repo.get_last_scans(limit=limit, offset=offset)
    ]


@router.get("/scans/{task_id}/")
@inject
async def get_scan(
    task_id: UUID4,
    scan_task_service: FromDishka[ScanTaskService],
) -> ScanTaskResponse:
    data = await scan_task_service.response(task_id)
    return ScanTaskResponse.model_validate(data)
