from schemas.base import BaseSchema


class ScanStart(BaseSchema):
    task_id: str
    ips: list[str]


class ScanIP(BaseSchema):
    task_id: str
    ip: str


class ScanPort(BaseSchema):
    task_id: str
    ip: str
    port: int
