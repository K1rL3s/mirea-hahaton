from app.schemas.base import BaseSchema


class ScanRequest(BaseSchema):
    targets: list[str]
