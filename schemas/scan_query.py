from schemas.base import BaseSchema


class ScanStart(BaseSchema):
    task_id: str
    ips: list[str]
    ipv6: bool = False


class ScanIP(BaseSchema):
    task_id: str
    ip: str
    ipv6: bool = False


class ScanPort(BaseSchema):
    task_id: str
    ip: str
    port: int
