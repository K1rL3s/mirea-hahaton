import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from faststream.nats import NatsBroker

from app.routes.randomizer import random_ips
from database.repos.scan_result import ScanResultRepo
from schemas.scan_api import LastScans, ScanRequest, ScanResponse, ScanTaskResponse
from schemas.scan_query import ScanStart

router = APIRouter()


@router.post("/scans/")
@inject
async def start_scan(
    scan_request: ScanRequest,
    broker: FromDishka[NatsBroker],
) -> ScanResponse:
    task_id = str(uuid.uuid4())
    await broker.publish(
        ScanStart(task_id=task_id, ips=scan_request.targets),
        subject="scan-start",
    )
    return ScanResponse(task_id=task_id)


@router.get("/scans/last/")
@inject
async def get_last_scan(
    limit: int = Query(default=10, ge=1, le=20),
    offset: int = Query(default=0, ge=0, le=10),
    scan_repo: FromDishka[ScanResultRepo] = None,
) -> list[LastScans]:
    return [
        LastScans(task_id=scan.id, ip=scan.ip, updated_at=scan.updated_at)
        for scan in await scan_repo.get_last_scans(limit=limit, offset=offset)
    ]


@router.get("/scans/{task_id}")
@inject
async def get_scan(task_id: str) -> ScanTaskResponse:
    return ScanTaskResponse(
        task_id=task_id,
        end=False,
        ips=random_ips(),
    )
