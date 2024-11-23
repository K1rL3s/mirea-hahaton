import random
import string

from schemas.scan_api import IpSchema, PortSchema, PortsSchema, VulnerabilitySchema


def random_ip() -> str:
    return (
        f"{random.randint(1, 255)}.{random.randint(1, 255)}."
        f"{random.randint(1, 255)}.{random.randint(1, 255)}"
    )


def random_port() -> int:
    return random.randint(1, 65535)


def random_str() -> str:
    return "".join(random.choices(string.ascii_letters, k=random.randint(8, 32)))


def random_closed_ports() -> list[int]:
    return [random_port() for _ in range(random.randint(1, 16))]


def random_vulnerability() -> VulnerabilitySchema:
    return VulnerabilitySchema(
        title=random_str(),
        description=random_str(),
        severity=random_str(),
    )


def random_open_port() -> PortSchema:
    return PortSchema(
        port=random_port(),
        type=random_str(),
        protocol=random_str(),
        service=random_str(),
        version=random_str(),
        vulnerabilities=[
            VulnerabilitySchema(
                title=random_str(),
                description=random_str(),
                severity=random_str(),
            ),
        ],
    )


def random_ip_schema() -> IpSchema:
    return IpSchema(
        ip=random_ip(),
        ptr=random_str(),
        ports=PortsSchema(
            closed=random_closed_ports(),
            open=[random_open_port() for _ in range(random.randint(1, 16))],
        ),
    )


def random_ips() -> list[IpSchema]:
    return [random_ip_schema() for _ in range(random.randint(1, 16))]
