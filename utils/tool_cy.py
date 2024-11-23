import aiohttp


async def ip_to_domain(ip: str) -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.tool.cy/{ip}") as response:
            data = await response.json(encoding="utf-8")
            domains = data.get("dns", {}).get("entries", [])
            return [domain.get("value") for domain in domains if domain.get("value")]
