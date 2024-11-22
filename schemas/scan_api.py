from schemas.base import BaseSchema


class ScanRequest(BaseSchema):
    targets: list[str]


class ScanResponse(BaseSchema):
    task_id: str


class Vulnerability(BaseSchema):
    title: str | None = None
    description: str | None = None
    severity: str | None = None


class PortSchema(BaseSchema):
    port: int
    protocol: str | None = None
    service: str | None = None
    version: str | None = None
    vulnerabilities: list[Vulnerability] = None


class PortsSchema(BaseSchema):
    open: list[PortSchema]
    closed: list[int]


class ScanTaskResponse(BaseSchema):
    task_id: str
    ptr: str
    ports: PortsSchema
