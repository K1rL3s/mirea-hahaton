from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from faststream.nats import NatsBroker

from query.config import NatsConfig, get_nats_config
from query.tasks import include_routers


class NatsProvider(Provider):
    @provide(scope=Scope.APP)
    def nats_config(self) -> NatsConfig:
        return get_nats_config()

    @provide(scope=Scope.APP)
    async def broker(
        self,
        nats_config: NatsConfig,
    ) -> AsyncIterable[NatsBroker]:
        broker = NatsBroker(str(nats_config.nats_url))
        include_routers(broker)
        await broker.connect()
        yield broker
        await broker.close()
