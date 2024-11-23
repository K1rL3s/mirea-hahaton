from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query

from schemas.convert_api import ConvertedSchema
from utils.tool_cy import ip_to_domain


router = APIRouter()


@router.get("/convert/")
@inject
async def convert_ip_or_domain(
    ip_or_domain: str = Query(...),
) -> ConvertedSchema:
    ip_or_domain = ip_or_domain.strip().strip("/").lstrip("https://").lstrip("http://")
    return ConvertedSchema(ip_or_domain=await ip_to_domain(ip_or_domain))
