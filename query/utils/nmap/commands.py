from schemas.scan_query import ScanIPSchema


def search_top_command(scan_ip: ScanIPSchema, cnt: int) -> str:
    return f"nmap --top-ports {cnt} -sS -T4 -A -v -oX {scan_ip.task_id}-{scan_ip.ip}.xml {scan_ip.ip}"
