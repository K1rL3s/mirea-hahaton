import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from faststream.nats import NatsBroker

from schemas.scan_api import (
    PortSchema,
    PortsSchema,
    ScanRequest,
    ScanResponse,
    ScanTaskResponse,
    Vulnerability,
)
from schemas.scan_query import ScanStart
from app.socket import sio

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
    # Emit a Socket.IO event when the scan starts
    await sio.emit('scan_started', {'task_id': task_id})
    return ScanResponse(task_id=task_id)

@router.get("/scan/{task_id}")
@inject
async def get_scan(task_id: str) -> ScanTaskResponse:
    await sio.emit('scan_completed', {'task_id': task_id})
    return ScanTaskResponse(
        task_id=task_id,
        ptr="ptr string",
        ports=PortsSchema(
            closed=[1, 2, 3, 4, 5],
            open=[
                PortSchema(
                    port=22,
                    protocol="protocol",
                    service="service",
                    version="version",
                    vulnerabilities=[
                        Vulnerability(
                            title="title",
                            description="description",
                            severity="severity",
                        ),
                    ],
                ),
            ],
        ),
    )
