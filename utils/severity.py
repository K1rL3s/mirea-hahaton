import aiohttp


async def check_vulnerabilities(software: str, version: str):
    nvd_url = (
        f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={software} {version}"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(nvd_url) as response:
            if response.status == 200:
                data = await response.json()
                vulnerabilities = data.get("result", {}).get("CVE_Items", [])
                return [
                    {
                        "cve_id": vuln["cve"]["CVE_data_meta"]["ID"],
                        "severity": vuln["impact"]["baseMetricV3"]["cvssV3"][
                            "baseSeverity"
                        ],
                    }
                    for vuln in vulnerabilities
                ]
    return []
