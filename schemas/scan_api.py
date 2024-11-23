import datetime

from pydantic import Field

from schemas.base import BaseSchema


class ScanRequest(BaseSchema):
    ip: str


class ScanResponse(BaseSchema):
    task_id: str


class VulnerabilitySchema(BaseSchema):
    title: str | None = None
    description: str | None = None
    severity: str | None = None


class PortSchema(BaseSchema):
    port: int
    type: str | None = None
    protocol: str | None = None
    service: str | None = None
    version: str | None = None
    vulnerabilities: list[VulnerabilitySchema] = Field(default_factory=list)


class PortsSchema(BaseSchema):
    open: list[PortSchema]
    closed: list[int]


class IpSchema(BaseSchema):
    ip: str
    ptr: str
    ports: PortsSchema


class ScanTaskResponse(BaseSchema):
    task_id: str
    end: bool
    ips: list[IpSchema]


class LastScans(BaseSchema):
    task_id: str
    ip: str
    updated_at: datetime.datetime
