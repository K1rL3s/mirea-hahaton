from schemas.base import BaseSchema


class ScanInput(BaseSchema):
    task_id: str
    message: str


class ScanOutput(BaseSchema):
    task_id: str
    message: str
