from schemas.base import BaseSchema


class ConvertedSchema(BaseSchema):
    ip_or_domain: list[str]
