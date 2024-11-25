import uuid
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

from faststream.nats import NatsBroker

from schemas.query.scan_query import ScanStartSchema

SUBJECT = "scan-start"


class ScanStartService:
    def __init__(self, broker: NatsBroker) -> None:
        self.broker = broker

    @staticmethod
    def generate_task_id() -> uuid.UUID:
        return uuid.uuid4()

    async def start_one_ip(
        self,
        ip: IPv4Address | IPv6Address,
        flags: str | None = None,
    ) -> uuid.UUID:
        task_id = self.generate_task_id()
        await self.broker.publish(
            ScanStartSchema(
                task_id=str(task_id),
                ips=[str(ip)],
                ipv6=isinstance(ip, IPv6Address),
                flags=flags,
            ),
            subject=SUBJECT,
        )
        return task_id

    async def start_ip_network(
        self,
        ip_network: IPv4Network | IPv6Network,
        flags: str | None = None,
    ) -> uuid.UUID:
        task_id = self.generate_task_id()
        await self.broker.publish(
            ScanStartSchema(
                task_id=str(task_id),
                ips=[str(ip) for ip in ip_network],
                ipv6=isinstance(ip_network, IPv6Network),
                flags=flags,
            ),
            subject=SUBJECT,
        )
        return task_id

    async def start_ip_range(
        self,
        left: IPv4Address,
        right: IPv4Address,
        flags: str | None = None,
    ) -> uuid.UUID:
        task_id = self.generate_task_id()

        left, right = int(left), int(right)
        ip_range: list[IPv4Address] | list[IPv6Address] = []
        while left <= right:
            ip_range.append(IPv4Address(left))
            left += 1

        await self.broker.publish(
            ScanStartSchema(
                task_id=str(task_id),
                ips=[str(ip) for ip in ip_range],
                ipv6=False,
                flags=flags,
            ),
            subject=SUBJECT,
        )

        return task_id

    async def start_ip_list(
        self,
        ip_list: list[IPv4Address] | list[IPv6Address],
        flags: str | None = None,
    ) -> uuid.UUID:
        task_id = self.generate_task_id()

        await self.broker.publish(
            ScanStartSchema(
                task_id=str(task_id),
                ips=[str(ip) for ip in ip_list],
                ipv6=isinstance(ip_list[0], IPv6Address),
                flags=flags,
            ),
            subject=SUBJECT,
        )

        return task_id
