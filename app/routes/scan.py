import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from faststream.nats import NatsBroker

from schemas.scan_api import ScanRequest, ScanResponse
from schemas.scan_query import ScanInput

router = APIRouter()


@router.post("/scan/")
@inject
async def start_scan(
    scan_request: ScanRequest,
    broker: FromDishka[NatsBroker],
) -> ScanResponse:
    task_id = str(uuid.uuid4())
    scan = ScanInput(task_id=task_id, message=str(scan_request.targets))
    await broker.publish(scan, subject="scan-input")
    return ScanResponse(task_id=task_id)


@router.get("/results/{task_id}")
async def get_scan_results(task_id: str) -> str:
    return task_id
