import datetime

from pydantic import UUID4, Field

from schemas.base import BaseSchema
from utils.enums.nmap import (
    HostDiscovery,
    PortRange,
    ScanType,
    Timing,
    VersionDetection,
)


class ScanRequest(BaseSchema):
    ip: str
    scan_type: ScanType = Field(
        default=ScanType.SYN,
        description="Тип сканирования (например, SYN или TCP)",
    )
    version_detection: VersionDetection | None = Field(
        default=VersionDetection.VERSION,
        description="Флаги для определения версии служб",
    )
    version_intensity_value: int | None = Field(
        default=None,
        gt=0,
        lt=10,
        description="Интенсивность сканирования версии служб. Включает флаг --version-intensity",
    )
    version_all: bool | None = Field(
        default=False,
        description="Показывать все версии служб. Включает флаг --version-all.",
    )
    host_discovery: HostDiscovery | None = Field(
        default=None,
        description="Методы обнаружения хостов",
    )
    port_range: PortRange | None = Field(
        default=PortRange.TOP_PORTS,
        description="Диапазон портов для сканирования",
    )
    specific_range: str | None = Field(
        default=None,
        description="Диапазон специфичных портов для сканирования. Необходимо, когда используется -p",
    )
    top_range: int | None = Field(
        gt=0,
        default=100,
        description="Количество топ-портов для сканирования. Необходимо, когда используется --top-ports",
    )
    timing: Timing | None = Field(
        default=Timing.AGGRESSIVE,
        description="Уровень таймингов для сканирования. От этого параметра зависит время скнанирования",
    )
    min_rate: int | None = Field(
        gt=0,
        default=None,
        description="Минимальная скорость отправки пакетов package/sec",
    )
    max_rate: int | None = Field(
        gt=0,
        default=None,
        description="Максимальная скорость отправки пакетов package/sec",
    )


class ScanResponse(BaseSchema):
    task_id: UUID4
    command: str


class VulnerabilitySchema(BaseSchema):
    title: str | None = None
    description: str | None = None
    severity: str | None = None


class PortSchema(BaseSchema):
    port: int
    protocol: str | None = None
    status: str | None = None
    service: str | None = None
    version: str | None = None
    reason: str | None = None
    vulnerabilities: list[VulnerabilitySchema] = Field(default_factory=list)


class PortsSchema(BaseSchema):
    open: list[PortSchema]
    closed: list[int]


class IpSchema(BaseSchema):
    ip: str
    ptr: str | None = None
    end: bool
    ports: PortsSchema


class ScanTaskResponse(BaseSchema):
    task_id: UUID4
    end: bool
    ips: list[IpSchema]


class LastScans(BaseSchema):
    task_id: UUID4
    ip: str
    updated_at: datetime.datetime
