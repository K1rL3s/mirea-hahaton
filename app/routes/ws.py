import asyncio
from typing import Any

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from faststream.nats.fastapi import NatsRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.ws_manager import WebSocketManager
from schemas.scan_query import ScanPort


api_router = APIRouter()
nats_router = NatsRouter("nats://nats:4222")


@api_router.websocket("/scan/{task_id}")
@inject
async def ws_scan_results(
    websocket: WebSocket,
    task_id: str,
    connection_manager: FromDishka[WebSocketManager],
) -> Any:
    await connection_manager.connect(task_id, websocket)

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        connection_manager.disconnect(task_id)
        # TODO: добавить отмену всех задач с таск_ид если клиент отключился


@nats_router.subscriber(subject="scan-ip-port")
@inject
async def scan_ip_port_handler(
    scan_ip_port: ScanPort,
    websocket_manager: FromDishka[WebSocketManager],
) -> None:
    print(scan_ip_port)
    await websocket_manager.send_message(str(scan_ip_port), scan_ip_port.task_id)
