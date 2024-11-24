from schemas.query.scan_query import ScanIPSchema
from utils.paths import xml_template


def make_nmap_command(scan_ip: ScanIPSchema) -> str:
    xml_path = xml_template(f'{scan_ip.task_id}-{scan_ip.ip}.xml')
    if scan_ip.flags:
        result = f"nmap {scan_ip.flags} -v -oX {xml_path} {scan_ip.ip}"
    else:
        result = f"nmap -v -oX {xml_path} {scan_ip.ip}"

    print(result)
    return result
