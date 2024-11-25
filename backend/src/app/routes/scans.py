from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Query
from pydantic import UUID4

from app.depends.scans import check_scan_request
from app.exceptions.scans import InvalidIP, InvalidIPCIDR, InvalidIPRange
from database.repos.scan_result import ScanResultRepo
from schemas.api.scan_api import LastScans, ScanRequest, ScanResponse, ScanTaskResponse
from services.scans.start import ScanStartService
from services.scans.task import ScanTaskService
from utils.ip_validate import convert_ip
from utils.nmap_generate_flags import generate_flags

MAX_IP_PER_TASK = 128

router = APIRouter()


@router.post("/scans/")
@inject
async def start_scan(
    scan_request: Annotated[ScanRequest, Depends(check_scan_request)],
    scan_start_service: FromDishka[ScanStartService],
) -> ScanResponse:
    ips = convert_ip(scan_request.ip)
    flags = generate_flags(scan_request)
    if ips is None:
        raise InvalidIP

    if isinstance(ips, (IPv4Address, IPv6Address)):
        task_id = await scan_start_service.start_one_ip(ips, flags)

    elif isinstance(ips, (IPv4Network, IPv6Network)):
        if ips.num_addresses > MAX_IP_PER_TASK:
            raise InvalidIPCIDR
        task_id = await scan_start_service.start_ip_network(ips, flags)

    elif isinstance(ips, tuple) and len(ips) == 2:
        left, right = int(ips[0]), int(ips[1])
        if left > right or right - left + 1 > MAX_IP_PER_TASK:
            raise InvalidIPRange
        task_id = await scan_start_service.start_ip_range(ips[0], ips[1], flags)

    elif isinstance(ips, list):
        if len(ips) > MAX_IP_PER_TASK:
            raise InvalidIPRange
        task_id = await scan_start_service.start_ip_list(ips, flags)

    else:
        raise InvalidIP

    return ScanResponse(task_id=task_id, command=("nmap " + flags + scan_request.ip))


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
