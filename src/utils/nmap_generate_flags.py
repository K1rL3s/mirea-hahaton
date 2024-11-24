from schemas.api.scan_api import ScanRequest
from utils.enums.nmap import PortRange


def generate_flags(scan_request: ScanRequest) -> str:
    flags = f"{scan_request.scan_type.value} "
    if scan_request.version_detection:
        flags += scan_request.version_detection.value + " "
    if scan_request.version_intensity_value:
        flags += f"--version-intensity {scan_request.version_intensity_value} "
    if scan_request.version_all:
        flags += "--version-all "
    if scan_request.host_discovery:
        flags += scan_request.host_discovery.value + " "
    if scan_request.port_range:
        flags += scan_request.port_range.value + " "
        if scan_request.port_range == PortRange.SPECIFIC:
            flags += scan_request.specific_range + " "
        if scan_request.port_range == PortRange.TOP_PORTS:
            flags += str(scan_request.top_range) + " "

    if scan_request.timing:
        flags += scan_request.timing.value + " "

    if scan_request.min_rate:
        flags += f"--min-rate {scan_request.min_rate} "
    if scan_request.max_rate:
        flags += f"--max-rate {scan_request.max_rate} "

    return flags
