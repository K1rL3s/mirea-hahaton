from dishka import provide, Provider, Scope

from app.ws_manager import WebSocketManager


class WSProvider(Provider):
    @provide(scope=Scope.APP)
    def websocket_manager(self) -> WebSocketManager:
        return WebSocketManager()
