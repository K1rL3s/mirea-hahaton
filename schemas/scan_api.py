from schemas.base import BaseSchema


class ScanRequest(BaseSchema):
    targets: list[str]


class ScanResponse(BaseSchema):
    task_id: str
