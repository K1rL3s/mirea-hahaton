from fastapi import APIRouter

from schemas.api.locations_api import LocationsSchema

router = APIRouter()


@router.get("/locations/")
async def scan_locations() -> list[LocationsSchema]:
    return [
        LocationsSchema(ip="127.0.0.1", location="RTU MIREA"),
        LocationsSchema(ip="28.10.2007.0", location="Techno Коворк"),
    ]
