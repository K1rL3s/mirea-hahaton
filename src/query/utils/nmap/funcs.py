from schemas.query.scan_query import ScanIPSchema


def make_nmap_command(scan_ip: ScanIPSchema) -> str:
    if scan_ip.flags:
        result = f"nmap {scan_ip.flags} -v -oX {scan_ip.task_id}-{scan_ip.ip}.xml {scan_ip.ip}"
    else:
        result = f"nmap -v -oX {scan_ip.task_id}-{scan_ip.ip}.xml {scan_ip.ip}"

    print(result)
    return result
