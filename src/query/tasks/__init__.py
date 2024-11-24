from faststream.nats import NatsBroker

from .scan import router as scan_router


def include_routers(broker: NatsBroker) -> None:
    broker.include_routers(
        scan_router,
    )
