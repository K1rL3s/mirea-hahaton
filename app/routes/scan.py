import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from faststream.nats import NatsBroker

from app.routes.randomizer import random_ips
from schemas.scan_api import ScanRequest, ScanResponse, ScanTaskResponse
from schemas.scan_query import ScanStart

router = APIRouter()


@router.post("/scan/")
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


@router.get("/scan/{task_id}")
@inject
async def get_scan(task_id: str) -> ScanTaskResponse:
    return ScanTaskResponse(
        task_id=task_id,
        end=False,
        ips=random_ips(),
    )
