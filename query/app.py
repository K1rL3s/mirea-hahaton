from dishka.integrations.faststream import FastStreamProvider, setup_dishka
from faststream import FastStream
from faststream.nats import NatsBroker

from di.container import make_container


async def create_app() -> FastStream:
    container = make_container(extra_providers=[FastStreamProvider()])

    broker = await container.get(NatsBroker)
    app = FastStream(broker)

    setup_dishka(container, app, auto_inject=True)

    return app


# async def scan_network(targets: list[str]):
#     scanner = nmap.PortScanner()
#     results = []
#     for target in targets:
#         scan_data = scanner.scan(hosts=target, arguments="-sV")
#         results.append(parse_scan_results(scan_data))
#     await save_to_database(results)
#
#
# async def parse_scan_results(scan_data):
#     # Логика разбора результатов nmap
#     ...
#
# async def save_to_database(results):
#     # Сохраняем результаты сканирования в базу через SQLAlchemy
#     ...
