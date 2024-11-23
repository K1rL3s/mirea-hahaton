from fastapi import APIRouter

from schemas.locations_api import LocationsSchema

router = APIRouter()


@router.get("/locations/")
async def scan_locations() -> list[LocationsSchema]:
    return [LocationsSchema(ip="127.0.0.1", location="RTU MIREA")]
