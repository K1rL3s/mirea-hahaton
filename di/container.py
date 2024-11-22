from dishka import AsyncContainer, Provider, make_async_container

from .database.connection import DBProvider
from .nats.connection import NatsProvider
from .ws.manager import WSProvider


def make_container(extra_providers: list[Provider]) -> AsyncContainer:
    return make_async_container(
        DBProvider(),
        NatsProvider(),
        WSProvider(),
        *extra_providers,
    )
