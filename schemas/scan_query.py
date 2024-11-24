from schemas.base import BaseSchema


class ScanStartSchema(BaseSchema):
    task_id: str
    ips: list[str]
    ipv6: bool = False
    flags: str | None = None


class ScanIPSchema(BaseSchema):
    task_id: str
    ip: str
    ipv6: bool = False
    flags: str | None = None


class ScanPortSchema(BaseSchema):
    task_id: str
    ip: str
    port: int
    protocol: str
    state: str | None = None
    service: str | None = None
    version: str | None = None
    reason: str | None = None


class ScanResultSchema(BaseSchema):
    task_id: str
    ip: str
    ptr_record: str | None = None
    severity: str | None = None
