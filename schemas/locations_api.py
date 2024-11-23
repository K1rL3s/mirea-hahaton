from schemas.base import BaseSchema


class LocationsSchema(BaseSchema):
    ip: str
    location: str
