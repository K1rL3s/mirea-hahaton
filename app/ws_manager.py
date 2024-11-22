import contextlib

from starlette.websockets import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, task_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[task_id] = websocket

    def disconnect(self, task_id: str) -> None:
        with contextlib.suppress(KeyError):
            del self.connections[task_id]

    def get_websocket(self, task_id: str) -> WebSocket | None:
        return self.connections.get(task_id)

    async def send_message(self, message: str, task_id: str) -> None:
        websocket = self.get_websocket(task_id)
        if websocket:
            await websocket.send_text(message)

